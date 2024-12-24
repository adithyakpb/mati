from sqlalchemy.orm import Session
from ..models.base import NodeType
from ..core.registry import NODE_TYPE_SPECS
import json

def register_node_types(db: Session):
    """Register initial node types in the database"""
    
    for type_id, spec in NODE_TYPE_SPECS.items():
        # Check if node type already exists
        existing = db.query(NodeType).filter(
            NodeType.name == spec["name"],
            NodeType.version == spec["version"]
        ).first()
        
        if not existing:
            node_type = NodeType(
                name=spec["name"],
                category=spec["category"],
                description=spec["description"],
                version=spec["version"],
                input_ports=spec["input_ports"],
                output_ports=spec["output_ports"],
                config_schema=spec["config_schema"]
            )
            db.add(node_type)
            print(f"Registered node type: {spec['name']} v{spec['version']}")
    
    db.commit()
