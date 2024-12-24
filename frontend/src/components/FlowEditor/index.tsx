import React, { useState, useCallback, useRef } from 'react';
import ReactFlow, {
  Node,
  Edge,
  Controls,
  Background,
  Connection,
  addEdge,
  NodeChange,
  EdgeChange,
  ConnectionMode,
  OnNodesChange,
  OnEdgesChange,
  OnConnect,
  ReactFlowInstance,
  applyNodeChanges,
  applyEdgeChanges,
  PanOnScrollMode,
  MiniMap,
  NodeTypes,
} from 'reactflow';
import 'reactflow/dist/style.css';

import GenericNode from './nodes/GenericNode';
import { nodeDefinitions } from '../../config/nodeDefinitions';
import NodeProperties from './NodeProperties';
import Toolbar from './Toolbar';

// Map all node types to the generic component
const nodeTypes: NodeTypes = {
  textGeneration: GenericNode,
  speechToText: GenericNode,
  textToSpeech: GenericNode,
  imageGeneration: GenericNode,
};

// Initialize with empty state
const initialNodes: Node[] = [];
const initialEdges: Edge[] = [];

// Debug helper for node operations
const debugNode = (prefix: string, node: Node) => {
  console.log(`[FlowEditor] ${prefix}:`, {
    id: node.id,
    type: node.type,
    position: node.position,
    data: node.data
  });
};

export default function FlowEditor() {
  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  const [reactFlowInstance, setReactFlowInstance] = useState<ReactFlowInstance | null>(null);
  const [nodes, setNodes] = useState<Node[]>(initialNodes);
  const [edges, setEdges] = useState<Edge[]>(initialEdges);
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);
  const [mounted, setMounted] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);
  const [connectionStartHandle, setConnectionStartHandle] = useState<Element | null>(null);

  const onNodesChange: OnNodesChange = useCallback(
    (changes: NodeChange[]) => {
      setNodes((nds) => {
        // Handle node selection
        changes.forEach((change) => {
          if ('selected' in change && change.type === 'select') {
            const node = nds.find((n) => n.id === change.id);
            setSelectedNode(change.selected && node ? node : null);
          }
        });

        // Apply ReactFlow's changes directly
        return applyNodeChanges(changes, nds);
      });
    },
    []
  );

  const onEdgesChange: OnEdgesChange = useCallback(
    (changes: EdgeChange[]) => {
      setEdges((eds) => applyEdgeChanges(changes, eds));
    },
    []
  );

  const onConnect: OnConnect = useCallback(
    (connection: Connection) => {
      // Validate connection here if needed
      setEdges((eds) => addEdge(connection, eds));
    },
    [setEdges]
  );

  const onNodePropertyChange = useCallback(
    (nodeId: string, propertyKey: string, value: unknown) => {
      setNodes((nds) =>
        nds.map((node) => {
          if (node.id === nodeId) {
            return {
              ...node,
              data: {
                ...node.data,
                configuration: {
                  ...node.data.configuration,
                  [propertyKey]: value,
                }
              },
            };
          }
          return node;
        })
      );
    },
    []
  );

  // Helper function to get default configuration for a node type
  const getDefaultConfiguration = (nodeType: string) => {
    const nodeDef = nodeDefinitions[nodeType];
    if (!nodeDef) return {};

    const config: Record<string, unknown> = {};
    const properties = nodeDef.configSchema.properties || {};
    
    Object.entries(properties).forEach(([key, schema]) => {
      if (schema.enum && schema.enum.length > 0) {
        config[key] = schema.enum[0];
      } else if (schema.type === 'number' && schema.minimum !== undefined) {
        config[key] = schema.minimum;
      } else if (schema.type === 'string') {
        config[key] = '';
      } else if (schema.type === 'boolean') {
        config[key] = false;
      }
    });

    return config;
  };

  const onAddNode = useCallback(
    (type: string, isDblClick?: boolean) => {
      console.log('[FlowEditor] Adding node of type:', type);
      console.log('[FlowEditor] Available types:', Object.keys(nodeTypes));

      // Check if node type exists in definitions
      if (!nodeDefinitions[type]) {
        console.error(`[FlowEditor] Invalid node type: ${type}`);
        return;
      }

      if (!reactFlowInstance) {
        console.warn('[FlowEditor] ReactFlow instance not initialized, using fallback position');
        const newNode: Node = {
          id: `${type}-${nodes.length + 1}`,
          type,
          position: { x: 100, y: 100 },
          data: {
            nodeType: nodeDefinitions[type],
            configuration: getDefaultConfiguration(type)
          },
        };
        debugNode('Creating node (fallback)', newNode);
        setNodes((nds) => {
          const updatedNodes = nds.concat(newNode);
          console.log('[FlowEditor] Updated nodes:', updatedNodes);
          return updatedNodes;
        });
        return;
      }

      // Get the wrapper element's dimensions
      const wrapper = reactFlowWrapper.current;
      if (!wrapper) {
        console.warn('[FlowEditor] Wrapper element not found');
        return;
      }

      const rect = wrapper.getBoundingClientRect();
      console.log('[FlowEditor] Wrapper dimensions:', rect);

      // Calculate position based on click type
      const position = isDblClick
        ? reactFlowInstance.screenToFlowPosition({
            x: rect.width / 2,
            y: rect.height / 2 + 100, // Offset from center
          })
        : reactFlowInstance.project({
            x: rect.width / 2,
            y: rect.height / 2,
          });

      const newNode: Node = {
        id: `${type}-${nodes.length + 1}`,
        type,
        position,
        data: {
          nodeType: nodeDefinitions[type],
          configuration: getDefaultConfiguration(type)
        },
      };

      debugNode('Creating node', newNode);
      setNodes((nds) => {
        const updatedNodes = nds.concat(newNode);
        console.log('[FlowEditor] Updated nodes:', updatedNodes);
        return updatedNodes;
      });
    },
    [reactFlowInstance, nodes.length]
  );

  const onInit = useCallback((instance: ReactFlowInstance) => {
    console.log('ReactFlow initialized');
    console.log('Available node types:', Object.keys(nodeTypes));
    setReactFlowInstance(instance);
  }, []);

  // Debug log whenever nodes change
  React.useEffect(() => {
    console.log('Current nodes:', nodes);
  }, [nodes]);

  // Only render on client-side to avoid hydration issues
  React.useEffect(() => {
    setMounted(true);
  }, []);

  const content = mounted ? (
    <div style={{ width: '100vw', height: '100vh', display: 'flex' }} ref={reactFlowWrapper}>
      <div style={{ flex: 1, height: '100%', position: 'relative' }}>
        <Toolbar onAddNode={onAddNode} />
        <ReactFlow
          onInit={onInit}
          defaultViewport={{ x: 0, y: 0, zoom: 0.5 }}
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          nodeTypes={nodeTypes}
          connectionMode={ConnectionMode.Strict}
          fitView
          fitViewOptions={{ maxZoom: 0.8 }}
          snapToGrid={false}
          draggable={true}
          panOnDrag={true}
          selectionOnDrag={false}
          selectNodesOnDrag={false}
          connectOnClick={false}
          elevateEdgesOnSelect={true}
          connectionRadius={50}
          onlyRenderVisibleElements={false}
          deleteKeyCode="Delete"
          multiSelectionKeyCode="Shift"
          minZoom={0.1}
          maxZoom={4}
          defaultEdgeOptions={{
            type: 'smoothstep',
            animated: true,
            style: { strokeWidth: 3, stroke: '#3b82f6' }
          }}
          connectionLineStyle={{
            strokeWidth: 3,
            stroke: '#3b82f6',
          }}
          connectionLineComponent={({ connectionLineStyle, fromX, fromY, toX, toY }) => (
            <g>
              <path
                fill="none"
                strokeWidth={3}
                stroke="#3b82f6"
                d={`M${fromX},${fromY} C ${fromX + Math.abs(toX - fromX) / 2},${fromY} ${toX - Math.abs(toX - fromX) / 2},${toY} ${toX},${toY}`}
                style={{
                  ...connectionLineStyle,
                  filter: 'drop-shadow(0 0 8px rgba(59, 130, 246, 0.5))',
                }}
                className="animated"
              />
            </g>
          )}
          onConnectStart={(event, { handleType, nodeId }) => {
            setIsConnecting(true);
            
            // Store the starting handle element
            if (event.target instanceof Element) {
              event.target.classList.add('connecting');
              setConnectionStartHandle(event.target);
            }

            // Add mousemove event listener for connection preview and node highlighting
            const onMouseMove = (e: MouseEvent) => {
              if (!isConnecting) return;

              // Update connection line
              const connectionLine = document.querySelector('.react-flow__connection-path');
              if (connectionLine) {
                const svg = connectionLine.closest('svg');
                const viewport = connectionLine.closest('.react-flow__viewport');
                
                if (svg instanceof SVGSVGElement && viewport instanceof SVGGElement) {
                  const svgPoint = svg.createSVGPoint();
                  svgPoint.x = e.clientX;
                  svgPoint.y = e.clientY;
                  
                  const ctm = viewport.getCTM();
                  if (ctm) {
                    const transformed = svgPoint.matrixTransform(ctm.inverse());
                    const sourceHandle = connectionStartHandle;
                    if (sourceHandle) {
                      const sourceRect = sourceHandle.getBoundingClientRect();
                      const sourcePoint = svg.createSVGPoint();
                      sourcePoint.x = sourceRect.left + sourceRect.width / 2;
                      sourcePoint.y = sourceRect.top + sourceRect.height / 2;
                      const sourceTransformed = sourcePoint.matrixTransform(ctm.inverse());

                      // Create a smooth bezier curve
                      const dx = Math.abs(transformed.x - sourceTransformed.x);
                      const controlPoint1X = sourceTransformed.x + dx * 0.5;
                      const controlPoint2X = transformed.x - dx * 0.5;

                      connectionLine.setAttribute(
                        'd',
                        `M ${sourceTransformed.x},${sourceTransformed.y} C ${controlPoint1X},${sourceTransformed.y} ${controlPoint2X},${transformed.y} ${transformed.x},${transformed.y}`
                      );
                    }
                  }
                }
              }

              // Handle node and port highlighting
              const nodes = document.querySelectorAll('.react-flow__node');
              nodes.forEach(node => {
                if (node.getAttribute('data-id') !== nodeId) {
                  const nodeRect = node.getBoundingClientRect();
                  const isOverNode = 
                    e.clientX >= nodeRect.left &&
                    e.clientX <= nodeRect.right &&
                    e.clientY >= nodeRect.top &&
                    e.clientY <= nodeRect.bottom;

                  // Handle port highlighting
                  const handles = node.querySelectorAll('.react-flow__handle');
                  handles.forEach(handle => {
                    if (handle !== connectionStartHandle) {
                      const handleRect = handle.getBoundingClientRect();
                      const isNearHandle = 
                        e.clientX >= handleRect.left - 20 &&
                        e.clientX <= handleRect.right + 20 &&
                        e.clientY >= handleRect.top - 20 &&
                        e.clientY <= handleRect.bottom + 20;

                      // Validate connection based on handle types
                      const isValidTarget = (
                        (handleType === 'source' && handle.classList.contains('react-flow__handle-left')) ||
                        (handleType === 'target' && handle.classList.contains('react-flow__handle-right'))
                      );

                      if (isOverNode && isNearHandle && isValidTarget) {
                        handle.classList.add('valid-target');
                        node.classList.add('highlight');
                      } else {
                        handle.classList.remove('valid-target');
                        if (!isOverNode) {
                          node.classList.remove('highlight');
                        }
                      }
                    }
                  });
                }
              });
            };
            
            window.addEventListener('mousemove', onMouseMove);
            const flowHandlers = window as Window & { __flowMouseMoveHandler?: (e: MouseEvent) => void };
            flowHandlers.__flowMouseMoveHandler = onMouseMove;
          }}
          onConnectEnd={() => {
            setIsConnecting(false);
            setConnectionStartHandle(null);
            
            // Clean up all connection-related classes
            const nodes = document.querySelectorAll('.react-flow__node');
            nodes.forEach(node => {
              node.classList.remove('highlight');
            });

            const handles = document.querySelectorAll('.react-flow__handle');
            handles.forEach(handle => {
              handle.classList.remove('connecting');
              handle.classList.remove('valid-target');
              handle.classList.remove('invalid-target');
            });

            // Remove event listener
            const flowHandlers = window as Window & { __flowMouseMoveHandler?: (e: MouseEvent) => void };
            if (flowHandlers.__flowMouseMoveHandler) {
              window.removeEventListener('mousemove', flowHandlers.__flowMouseMoveHandler);
              delete flowHandlers.__flowMouseMoveHandler;
            }
          }}
          style={{ background: '#1a1a1a' }}
          proOptions={{ hideAttribution: true }}
          elevateNodesOnSelect={true}
          translateExtent={[
            [-Infinity, -Infinity],
            [Infinity, Infinity]
          ]}
          nodesDraggable={true}
          nodesConnectable={true}
          zoomOnDoubleClick={false}
          panOnScroll={true}
          panOnScrollMode={PanOnScrollMode.Free}
        >
          <Background 
            color="#2a2a2a" 
            gap={16} 
            size={1}
            style={{ backgroundColor: '#1a1a1a' }}
          />
          <Controls />
          <MiniMap
            nodeColor="#666"
            nodeStrokeWidth={3}
            zoomable
            pannable
            style={{ background: '#1a1a1a', borderColor: '#333' }}
          />
        </ReactFlow>
      </div>
      {selectedNode && (
        <div style={{ width: '300px', borderLeft: '1px solid #333', padding: '1rem', background: '#1a1a1a', color: '#fff' }}>
          <NodeProperties
            node={selectedNode}
            onChange={onNodePropertyChange}
          />
        </div>
      )}
    </div>
  ) : null;

  return content;
}
