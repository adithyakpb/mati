from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Float, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class NodeType(Base):
    __tablename__ = "node_types"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String)
    version = Column(String, nullable=False)
    input_ports = Column(JSON, nullable=False)
    output_ports = Column(JSON, nullable=False)
    config_schema = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Node(Base):
    __tablename__ = "nodes"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    workflow_id = Column(String, ForeignKey('workflows.id'), nullable=False)
    type = Column(String, ForeignKey('node_types.id'), nullable=False)
    name = Column(String, nullable=False)
    config = Column(JSON)
    position_x = Column(Float, default=0)
    position_y = Column(Float, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    workflow = relationship("Workflow", back_populates="nodes")
    node_type = relationship("NodeType")

class Connection(Base):
    __tablename__ = "connections"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    workflow_id = Column(String, ForeignKey('workflows.id'), nullable=False)
    name = Column(String)
    source_node = Column(String, ForeignKey('nodes.id'), nullable=False)
    source_port = Column(String, nullable=False)
    target_node = Column(String, ForeignKey('nodes.id'), nullable=False)
    target_port = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    workflow = relationship("Workflow", back_populates="connections")

class WorkflowVersion(Base):
    __tablename__ = "workflow_versions"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    workflow_id = Column(String, ForeignKey('workflows.id'), nullable=False)
    version = Column(String, nullable=False)
    description = Column(String)
    data = Column(JSON, nullable=False)  # Stores complete workflow state
    created_at = Column(DateTime, default=datetime.utcnow)
    
    workflow = relationship("Workflow", back_populates="versions")

class Workflow(Base):
    __tablename__ = "workflows"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    description = Column(String)
    current_version_id = Column(String, ForeignKey('workflow_versions.id'), nullable=True)
    global_config = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    nodes = relationship("Node", back_populates="workflow", cascade="all, delete-orphan")
    connections = relationship("Connection", back_populates="workflow", cascade="all, delete-orphan")
    versions = relationship("WorkflowVersion", back_populates="workflow", cascade="all, delete-orphan")
    current_version = relationship("WorkflowVersion", foreign_keys=[current_version_id])

class WorkflowRun(Base):
    __tablename__ = "workflow_runs"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    workflow_id = Column(String, ForeignKey('workflows.id'), nullable=False)
    version_id = Column(String, ForeignKey('workflow_versions.id'), nullable=False)
    status = Column(String, nullable=False)  # 'running', 'completed', 'failed'
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    logs = Column(JSON)  # Stores execution logs
    results = Column(JSON)  # Stores node results
    error = Column(String)  # Stores error message if failed
    
    workflow = relationship("Workflow")
    version = relationship("WorkflowVersion")
