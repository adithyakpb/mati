from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class WorkflowRunCreate(BaseModel):
    version_id: Optional[str] = Field(
        None,
        description="ID of the workflow version to run. If not provided, uses workflow's current version"
    )
    config: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional configuration overrides for this run"
    )

class WorkflowRunUpdate(BaseModel):
    status: str = Field(..., description="New status for the run")
    progress: Optional[float] = Field(None, description="Progress percentage (0-100)")
    current_node: Optional[str] = Field(None, description="ID of the currently executing node")
    error: Optional[str] = Field(None, description="Error message if run failed")

class NodeState(BaseModel):
    status: str = Field(..., description="Status of the node (pending/running/completed/failed)")
    started_at: Optional[datetime] = Field(None, description="When node execution started")
    completed_at: Optional[datetime] = Field(None, description="When node execution completed")
    error: Optional[str] = Field(None, description="Error message if node failed")
    inputs: Optional[Dict[str, Any]] = Field(None, description="Input values received by the node")
    outputs: Optional[Dict[str, Any]] = Field(None, description="Output values produced by the node")
    metrics: Optional[Dict[str, Any]] = Field(None, description="Performance metrics for the node")

class WorkflowRunState(BaseModel):
    run_id: str = Field(..., description="ID of the workflow run")
    status: str = Field(..., description="Current status of the run")
    progress: float = Field(..., description="Overall progress percentage (0-100)")
    current_node: Optional[str] = Field(None, description="ID of the currently executing node")
    node_states: Dict[str, NodeState] = Field(
        default_factory=dict,
        description="States of all nodes in the workflow"
    )
    error: Optional[str] = Field(None, description="Error message if run failed")

class LogEntry(BaseModel):
    timestamp: datetime = Field(..., description="When the log entry was created")
    level: str = Field(..., description="Log level (info/warning/error)")
    node_id: Optional[str] = Field(None, description="ID of the node that generated this log")
    message: str = Field(..., description="Log message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional structured data")

class WorkflowRunResponse(BaseModel):
    id: str = Field(..., description="Unique identifier for the run")
    workflow_id: str = Field(..., description="ID of the workflow being run")
    version_id: str = Field(..., description="ID of the workflow version being run")
    status: str = Field(..., description="Current status of the run")
    start_time: datetime = Field(..., description="When the run started")
    end_time: Optional[datetime] = Field(None, description="When the run completed")
    logs: List[LogEntry] = Field(default_factory=list, description="Execution logs")
    results: Dict[str, Any] = Field(
        default_factory=dict,
        description="Results and metrics from the run"
    )
    error: Optional[str] = Field(None, description="Error message if run failed")

    class Config:
        orm_mode = True

# Example node state:
"""
{
    "status": "completed",
    "started_at": "2024-01-09T12:00:00Z",
    "completed_at": "2024-01-09T12:00:05Z",
    "inputs": {
        "text": "Hello, world!"
    },
    "outputs": {
        "tokens": 3,
        "embedding": [0.1, 0.2, 0.3]
    },
    "metrics": {
        "processing_time": 0.5,
        "memory_used": 1024
    }
}
"""

# Example log entry:
"""
{
    "timestamp": "2024-01-09T12:00:00Z",
    "level": "info",
    "node_id": "text-gen-1",
    "message": "Generated response with 150 tokens",
    "details": {
        "prompt_tokens": 50,
        "completion_tokens": 100,
        "model": "gpt-3.5-turbo"
    }
}
"""
