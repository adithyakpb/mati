from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uuid

from ...db.session import get_db
from ...models.base import Workflow, WorkflowVersion
from ...schemas.workflow import (
    WorkflowCreate,
    WorkflowUpdate,
    WorkflowResponse,
    WorkflowVersionCreate,
    WorkflowVersionResponse
)

router = APIRouter()

@router.post("/workflows", response_model=WorkflowResponse)
def create_workflow(workflow: WorkflowCreate, db: Session = Depends(get_db)):
    """Create a new workflow"""
    db_workflow = Workflow(
        id=str(uuid.uuid4()),
        name=workflow.name,
        description=workflow.description,
        global_config=workflow.global_config,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_workflow)
    db.commit()
    db.refresh(db_workflow)
    return db_workflow

@router.get("/workflows", response_model=List[WorkflowResponse])
def list_workflows(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all workflows with pagination"""
    workflows = db.query(Workflow).offset(skip).limit(limit).all()
    return workflows

@router.get("/workflows/{workflow_id}", response_model=WorkflowResponse)
def get_workflow(workflow_id: str, db: Session = Depends(get_db)):
    """Get a specific workflow by ID"""
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow

@router.put("/workflows/{workflow_id}", response_model=WorkflowResponse)
def update_workflow(
    workflow_id: str,
    workflow_update: WorkflowUpdate,
    db: Session = Depends(get_db)
):
    """Update a workflow"""
    db_workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if db_workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    for field, value in workflow_update.dict(exclude_unset=True).items():
        setattr(db_workflow, field, value)
    
    db_workflow.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_workflow)
    return db_workflow

@router.delete("/workflows/{workflow_id}")
def delete_workflow(workflow_id: str, db: Session = Depends(get_db)):
    """Delete a workflow"""
    db_workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if db_workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    db.delete(db_workflow)
    db.commit()
    return {"message": "Workflow deleted successfully"}

@router.post("/workflows/{workflow_id}/versions", response_model=WorkflowVersionResponse)
def create_workflow_version(
    workflow_id: str,
    version: WorkflowVersionCreate,
    db: Session = Depends(get_db)
):
    """Create a new version of a workflow"""
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    db_version = WorkflowVersion(
        id=str(uuid.uuid4()),
        workflow_id=workflow_id,
        version=version.version,
        description=version.description,
        data=version.data,
        created_at=datetime.utcnow()
    )
    db.add(db_version)
    
    # Update workflow's current version if requested
    if version.set_as_current:
        workflow.current_version_id = db_version.id
        workflow.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_version)
    return db_version

@router.get("/workflows/{workflow_id}/versions", response_model=List[WorkflowVersionResponse])
def list_workflow_versions(
    workflow_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all versions of a workflow"""
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    versions = db.query(WorkflowVersion)\
        .filter(WorkflowVersion.workflow_id == workflow_id)\
        .offset(skip)\
        .limit(limit)\
        .all()
    return versions
