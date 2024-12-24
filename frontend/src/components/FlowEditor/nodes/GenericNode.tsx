import React, { memo } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';
import { NodeType } from '../../../types/nodes';

interface GenericNodeData {
  nodeType: NodeType;
  configuration: Record<string, unknown>;
}

function GenericNode({ data }: NodeProps<GenericNodeData>) {
  const { nodeType, configuration } = data;

  return (
    <div className="relative">
      <div 
        className="px-4 py-2 shadow-lg rounded-lg border-2" 
        style={{ 
          backgroundColor: nodeType.style?.backgroundColor || '#1a1a1a',
          borderColor: nodeType.style?.borderColor || '#3b82f6',
          position: 'relative',
          zIndex: 1
        }}
      >
        {/* Header */}
        <div className="p-2 -mx-4 -mt-2 mb-2 bg-gray-700 hover:bg-gray-600 transition-colors">
          <div className="flex items-center justify-between">
            <div className="text-lg font-bold text-white flex items-center gap-2">
              {nodeType.style?.icon && <span>{nodeType.style.icon}</span>}
              {nodeType.name}
            </div>
            <div className="text-xs bg-blue-500 text-white px-2 py-1 rounded">
              {nodeType.category}
            </div>
          </div>
        </div>

        {/* Configuration Display */}
        <div className="space-y-1">
          {Object.entries(configuration).map(([key, value]) => (
            <div key={key} className="text-gray-300">
              {key}: <span className="text-blue-400">{String(value)}</span>
            </div>
          ))}
        </div>

        {/* Input Ports */}
        {nodeType.inputPorts.map((port) => (
          <Handle
            key={port.id}
            type="target"
            position={Position.Left}
            id={port.id}
          >
            <div className="absolute left-0 top-1/2 transform -translate-y-1/2 -translate-x-full pr-2">
              <span className="text-xs text-gray-400">{port.name}</span>
            </div>
          </Handle>
        ))}

        {/* Output Ports */}
        {nodeType.outputPorts.map((port) => (
          <Handle
            key={port.id}
            type="source"
            position={Position.Right}
            id={port.id}
          >
            <div className="absolute right-0 top-1/2 transform -translate-y-1/2 translate-x-full pl-2">
              <span className="text-xs text-gray-400">{port.name}</span>
            </div>
          </Handle>
        ))}
      </div>
    </div>
  );
}

export default memo(GenericNode);
