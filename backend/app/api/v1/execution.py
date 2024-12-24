from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

from ...db.session import get_db
from ...models.base import Workflow, WorkflowRun, WorkflowVersion
from ...schemas.execution import (
    WorkflowRunCreate,
    WorkflowRunResponse,
    WorkflowRunUpdate,
    WorkflowRunState
)
from ...core.engine import WorkflowEngine

router = APIRouter()

@router.post("/workflows/{workflow_id}/execute", response_model=WorkflowRunResponse)
async def execute_workflow(
    workflow_id: str,
    run_config: WorkflowRunCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Start execution of a workflow"""
    # Get workflow and version
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    version_id = run_config.version_id or workflow.current_version_id
    if version_id is None:
        raise HTTPException(
            status_code=400,
            detail="No version specified and workflow has no current version"
        )
    
    version = db.query(WorkflowVersion).filter(WorkflowVersion.id == version_id).first()
    if version is None:
        raise HTTPException(status_code=404, detail="Workflow version not found")
    
    # Create run record
    run = WorkflowRun(
        id=str(uuid.uuid4()),
        workflow_id=workflow_id,
        version_id=version_id,
        status="queued",
        start_time=datetime.utcnow(),
        logs=[],
        results={},
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    
    # Start execution in background
    engine = WorkflowEngine()
    background_tasks.add_task(
        engine.execute_workflow,
        workflow_data=version.data,
        run_id=run.id,
        db=db
    )
    
    return run

@router.get("/workflows/{workflow_id}/runs", response_model=list[WorkflowRunResponse])
def list_workflow_runs(
    workflow_id: str,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all runs of a workflow with optional status filter"""
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    query = db.query(WorkflowRun).filter(WorkflowRun.workflow_id == workflow_id)
    if status:
        query = query.filter(WorkflowRun.status == status)
    
    runs = query.order_by(WorkflowRun.start_time.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    return runs

@router.get("/runs/{run_id}", response_model=WorkflowRunResponse)
def get_run(run_id: str, db: Session = Depends(get_db)):
    """Get details of a specific workflow run"""
    run = db.query(WorkflowRun).filter(WorkflowRun.id == run_id).first()
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return run

@router.post("/runs/{run_id}/cancel")
async def cancel_run(run_id: str, db: Session = Depends(get_db)):
    """Cancel a running workflow execution"""
    run = db.query(WorkflowRun).filter(WorkflowRun.id == run_id).first()
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    
    if run.status not in ["queued", "running"]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel run with status: {run.status}"
        )
    
    engine = WorkflowEngine()
    await engine.cancel_workflow(run_id)
    
    run.status = "cancelled"
    run.end_time = datetime.utcnow()
    db.commit()
    
    return {"message": "Run cancelled successfully"}

@router.get("/runs/{run_id}/state", response_model=WorkflowRunState)
def get_run_state(run_id: str, db: Session = Depends(get_db)):
    """Get the current state of a workflow run"""
    run = db.query(WorkflowRun).filter(WorkflowRun.id == run_id).first()
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    
    return WorkflowRunState(
        run_id=run.id,
        status=run.status,
        progress=run.results.get("progress", 0),
        current_node=run.results.get("current_node"),
        node_states=run.results.get("node_states", {}),
        error=run.error
    )

@router.get("/runs/{run_id}/logs")
def get_run_logs(
    run_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get logs from a workflow run"""
    run = db.query(WorkflowRun).filter(WorkflowRun.id == run_id).first()
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    
    logs = run.logs[skip:skip + limit] if run.logs else []
    return {
        "run_id": run_id,
        "total_logs": len(run.logs) if run.logs else 0,
        "logs": logs
    }

@router.get("/runs/{run_id}/results")
def get_run_results(run_id: str, db: Session = Depends(get_db)):
    """Get the results of a completed workflow run"""
    run = db.query(WorkflowRun).filter(WorkflowRun.id == run_id).first()
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    
    if run.status != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Run is not completed. Current status: {run.status}"
        )
    
    return {
        "run_id": run_id,
        "results": run.results.get("node_results", {})
    }
