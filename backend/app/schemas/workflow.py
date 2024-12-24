from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class WorkflowBase(BaseModel):
    name: str = Field(..., description="Name of the workflow")
    description: Optional[str] = Field(None, description="Description of the workflow")
    global_config: Optional[Dict[str, Any]] = Field(None, description="Global configuration for the workflow")

class WorkflowCreate(WorkflowBase):
    pass

class WorkflowUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Name of the workflow")
    description: Optional[str] = Field(None, description="Description of the workflow")
    global_config: Optional[Dict[str, Any]] = Field(None, description="Global configuration for the workflow")
    current_version_id: Optional[str] = Field(None, description="ID of the current version")

class WorkflowResponse(WorkflowBase):
    id: str = Field(..., description="Unique identifier for the workflow")
    current_version_id: Optional[str] = Field(None, description="ID of the current version")
    created_at: datetime = Field(..., description="Timestamp when the workflow was created")
    updated_at: datetime = Field(..., description="Timestamp when the workflow was last updated")

    class Config:
        orm_mode = True

class WorkflowVersionBase(BaseModel):
    version: str = Field(..., description="Version string (e.g., '1.0.0')")
    description: Optional[str] = Field(None, description="Description of this version")
    data: Dict[str, Any] = Field(..., description="Complete workflow state data")

class WorkflowVersionCreate(WorkflowVersionBase):
    set_as_current: bool = Field(
        False,
        description="Whether to set this version as the current version"
    )

class WorkflowVersionResponse(WorkflowVersionBase):
    id: str = Field(..., description="Unique identifier for the version")
    workflow_id: str = Field(..., description="ID of the parent workflow")
    created_at: datetime = Field(..., description="Timestamp when the version was created")

    class Config:
        orm_mode = True
