import React, { memo } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

interface ImageGenerationData {
  label?: string;
  model?: string;
}

function ImageGenerationNode({ data }: NodeProps<ImageGenerationData>) {
  return (
    <div className="px-4 py-2 shadow-lg rounded-lg bg-gray-800 border-2 border-orange-500">
      <div className="p-2 -mx-4 -mt-2 mb-2 bg-gray-700 hover:bg-gray-600 transition-colors">
        <div className="flex items-center justify-between">
          <div className="text-lg font-bold text-white">Image Generation</div>
          <div className="text-xs bg-orange-500 text-white px-2 py-1 rounded">AI</div>
        </div>
      </div>
      <div className="space-y-1">
        <div className="text-gray-300">
          Model: <span className="text-orange-400">{data.model || 'DALL-E'}</span>
        </div>
      </div>

      <Handle
        type="target"
        position={Position.Left}
        id="prompt"
      />
      <Handle
        type="source"
        position={Position.Right}
        id="image"
      />
    </div>
  );
}

export default memo(ImageGenerationNode);
