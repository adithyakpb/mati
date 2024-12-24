from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class PortSchema(BaseModel):
    name: str = Field(..., description="Name of the port")
    data_type: str = Field(..., description="Data type that this port accepts/produces")
    description: Optional[str] = Field(None, description="Description of the port")
    required: bool = Field(True, description="Whether this port is required")
    default_value: Optional[Any] = Field(None, description="Default value for this port")

class NodeTypeBase(BaseModel):
    name: str = Field(..., description="Name of the node type")
    category: str = Field(..., description="Category this node type belongs to (e.g., 'AI', 'Data', 'IO')")
    description: Optional[str] = Field(None, description="Description of what this node type does")
    version: str = Field(..., description="Version of this node type")
    input_ports: List[Dict[str, Any]] = Field(
        ...,
        description="List of input ports and their specifications"
    )
    output_ports: List[Dict[str, Any]] = Field(
        ...,
        description="List of output ports and their specifications"
    )
    config_schema: Optional[Dict[str, Any]] = Field(
        None,
        description="JSON Schema for node configuration"
    )

class NodeTypeCreate(NodeTypeBase):
    pass

class NodeTypeUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Name of the node type")
    category: Optional[str] = Field(None, description="Category this node type belongs to")
    description: Optional[str] = Field(None, description="Description of what this node type does")
    version: Optional[str] = Field(None, description="Version of this node type")
    input_ports: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="List of input ports and their specifications"
    )
    output_ports: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="List of output ports and their specifications"
    )
    config_schema: Optional[Dict[str, Any]] = Field(
        None,
        description="JSON Schema for node configuration"
    )

class NodeTypeResponse(NodeTypeBase):
    id: str = Field(..., description="Unique identifier for the node type")
    created_at: datetime = Field(..., description="Timestamp when the node type was created")
    updated_at: datetime = Field(..., description="Timestamp when the node type was last updated")

    class Config:
        orm_mode = True

# Example port schema:
"""
{
    "name": "text_input",
    "data_type": "string",
    "description": "Input text to be processed",
    "required": true,
    "default_value": null
}
"""

# Example config schema:
"""
{
    "type": "object",
    "properties": {
        "model": {
            "type": "string",
            "enum": ["gpt-3.5-turbo", "gpt-4"],
            "description": "The model to use for text generation"
        },
        "temperature": {
            "type": "number",
            "minimum": 0,
            "maximum": 2,
            "default": 0.7,
            "description": "Controls randomness in the output"
        }
    },
    "required": ["model"]
}
"""
