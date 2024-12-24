from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uuid

from ...db.session import get_db
from ...models.base import NodeType
from ...schemas.node_type import (
    NodeTypeCreate,
    NodeTypeUpdate,
    NodeTypeResponse
)

router = APIRouter()

@router.post("/node-types", response_model=NodeTypeResponse)
def create_node_type(node_type: NodeTypeCreate, db: Session = Depends(get_db)):
    """Create a new node type"""
    db_node_type = NodeType(
        id=str(uuid.uuid4()),
        name=node_type.name,
        category=node_type.category,
        description=node_type.description,
        version=node_type.version,
        input_ports=node_type.input_ports,
        output_ports=node_type.output_ports,
        config_schema=node_type.config_schema,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_node_type)
    db.commit()
    db.refresh(db_node_type)
    return db_node_type

@router.get("/node-types", response_model=List[NodeTypeResponse])
def list_node_types(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all node types with optional category filter"""
    query = db.query(NodeType)
    if category:
        query = query.filter(NodeType.category == category)
    node_types = query.offset(skip).limit(limit).all()
    return node_types

@router.get("/node-types/{node_type_id}", response_model=NodeTypeResponse)
def get_node_type(node_type_id: str, db: Session = Depends(get_db)):
    """Get a specific node type by ID"""
    node_type = db.query(NodeType).filter(NodeType.id == node_type_id).first()
    if node_type is None:
        raise HTTPException(status_code=404, detail="Node type not found")
    return node_type

@router.put("/node-types/{node_type_id}", response_model=NodeTypeResponse)
def update_node_type(
    node_type_id: str,
    node_type_update: NodeTypeUpdate,
    db: Session = Depends(get_db)
):
    """Update a node type"""
    db_node_type = db.query(NodeType).filter(NodeType.id == node_type_id).first()
    if db_node_type is None:
        raise HTTPException(status_code=404, detail="Node type not found")
    
    update_data = node_type_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_node_type, field, value)
    
    db_node_type.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_node_type)
    return db_node_type

@router.delete("/node-types/{node_type_id}")
def delete_node_type(node_type_id: str, db: Session = Depends(get_db)):
    """Delete a node type"""
    db_node_type = db.query(NodeType).filter(NodeType.id == node_type_id).first()
    if db_node_type is None:
        raise HTTPException(status_code=404, detail="Node type not found")
    
    # Check if node type is in use
    if db.query(NodeType).filter(NodeType.type == node_type_id).first():
        raise HTTPException(
            status_code=400,
            detail="Cannot delete node type that is in use by existing nodes"
        )
    
    db.delete(db_node_type)
    db.commit()
    return {"message": "Node type deleted successfully"}

@router.get("/node-types/category/{category}", response_model=List[NodeTypeResponse])
def get_node_types_by_category(
    category: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all node types in a specific category"""
    node_types = db.query(NodeType)\
        .filter(NodeType.category == category)\
        .offset(skip)\
        .limit(limit)\
        .all()
    return node_types
