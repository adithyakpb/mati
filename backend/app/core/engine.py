from typing import Dict, Any, Optional, Set
from datetime import datetime
import asyncio
import logging
from sqlalchemy.orm import Session

from .node import NodeRunner
from .registry import node_registry
from ..models.base import WorkflowRun, Node

logger = logging.getLogger(__name__)

class WorkflowEngine:
    """Handles the execution of workflow graphs"""
    
    def __init__(self):
        self._active_runs: Dict[str, asyncio.Task] = {}
        self._cancel_events: Dict[str, asyncio.Event] = {}
    
    async def execute_workflow(
        self,
        workflow_data: Dict[str, Any],
        run_id: str,
        db: Session
    ):
        """Execute a workflow version"""
        try:
            # Initialize run state
            run = db.query(WorkflowRun).filter(WorkflowRun.id == run_id).first()
            if not run:
                logger.error(f"Run {run_id} not found")
                return
            
            run.status = "running"
            run.results = {
                "progress": 0,
                "node_states": {},
                "node_results": {}
            }
            db.commit()
            
            # Create cancel event
            self._cancel_events[run_id] = asyncio.Event()
            
            # Build execution graph
            nodes = workflow_data.get("nodes", {})
            connections = workflow_data.get("connections", {})
            execution_order = self._determine_execution_order(nodes, connections)
            
            # Execute nodes in order
            total_nodes = len(execution_order)
            completed_nodes = 0
            
            for node_id in execution_order:
                if self._cancel_events[run_id].is_set():
                    logger.info(f"Run {run_id} cancelled")
                    break
                
                node_data = nodes[node_id]
                node_type = node_data["type"]
                
                # Get node runner
                if node_type not in node_registry:
                    raise ValueError(f"Unknown node type: {node_type}")
                runner = node_registry[node_type]()
                
                # Prepare inputs
                inputs = self._gather_inputs(node_id, nodes, connections, run.results["node_results"])
                
                # Update state
                run.results["current_node"] = node_id
                run.results["node_states"][node_id] = {
                    "status": "running",
                    "started_at": datetime.utcnow().isoformat(),
                }
                db.commit()
                
                try:
                    # Execute node
                    outputs = await runner.execute(
                        inputs=inputs,
                        config=node_data.get("config", {}),
                        context={"run_id": run_id}
                    )
                    
                    # Store results
                    run.results["node_results"][node_id] = outputs
                    run.results["node_states"][node_id].update({
                        "status": "completed",
                        "completed_at": datetime.utcnow().isoformat(),
                        "inputs": inputs,
                        "outputs": outputs
                    })
                    
                except Exception as e:
                    logger.exception(f"Error executing node {node_id}")
                    run.status = "failed"
                    run.error = str(e)
                    run.results["node_states"][node_id].update({
                        "status": "failed",
                        "error": str(e),
                        "completed_at": datetime.utcnow().isoformat()
                    })
                    db.commit()
                    return
                
                # Update progress
                completed_nodes += 1
                run.results["progress"] = (completed_nodes / total_nodes) * 100
                db.commit()
            
            # Finalize run
            run.status = "completed" if not self._cancel_events[run_id].is_set() else "cancelled"
            run.end_time = datetime.utcnow()
            db.commit()
            
        except Exception as e:
            logger.exception(f"Error executing workflow run {run_id}")
            run.status = "failed"
            run.error = str(e)
            run.end_time = datetime.utcnow()
            db.commit()
            
        finally:
            # Cleanup
            self._cancel_events.pop(run_id, None)
            self._active_runs.pop(run_id, None)
    
    def _determine_execution_order(
        self,
        nodes: Dict[str, Any],
        connections: Dict[str, Any]
    ) -> list[str]:
        """Determine the order in which nodes should be executed"""
        # Build dependency graph
        dependencies: Dict[str, Set[str]] = {node_id: set() for node_id in nodes}
        for conn in connections.values():
            target_node = conn["target_node"]
            source_node = conn["source_node"]
            dependencies[target_node].add(source_node)
        
        # Topological sort
        execution_order = []
        visited = set()
        temp_visited = set()
        
        def visit(node_id: str):
            if node_id in temp_visited:
                raise ValueError("Workflow contains cycles")
            if node_id in visited:
                return
            
            temp_visited.add(node_id)
            for dep in dependencies[node_id]:
                visit(dep)
            temp_visited.remove(node_id)
            visited.add(node_id)
            execution_order.append(node_id)
        
        for node_id in nodes:
            if node_id not in visited:
                visit(node_id)
        
        return execution_order
    
    def _gather_inputs(
        self,
        node_id: str,
        nodes: Dict[str, Any],
        connections: Dict[str, Any],
        results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Gather input values for a node from its incoming connections"""
        inputs = {}
        
        # Find incoming connections
        incoming = {
            conn["target_port"]: conn
            for conn in connections.values()
            if conn["target_node"] == node_id
        }
        
        # Get node type's input port definitions
        node_data = nodes[node_id]
        input_ports = node_data.get("input_ports", {})
        
        # Gather values for each input port
        for port_name, port_data in input_ports.items():
            if port_name in incoming:
                # Get value from connected node's output
                conn = incoming[port_name]
                source_results = results.get(conn["source_node"])
                if source_results:
                    inputs[port_name] = source_results.get(conn["source_port"])
            elif "default_value" in port_data:
                # Use default value
                inputs[port_name] = port_data["default_value"]
            elif port_data.get("required", True):
                raise ValueError(
                    f"No value provided for required input port '{port_name}' "
                    f"on node {node_id}"
                )
        
        return inputs
    
    async def cancel_workflow(self, run_id: str):
        """Cancel a running workflow"""
        if run_id in self._cancel_events:
            self._cancel_events[run_id].set()
            if run_id in self._active_runs:
                await self._active_runs[run_id]
