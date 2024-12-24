import React, { memo } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

interface SpeechToTextData {
  label?: string;
  language?: string;
  confidence?: number;
}

function SpeechToTextNode({ data }: NodeProps<SpeechToTextData>) {
  return (
    <div className="px-4 py-2 shadow-md rounded-md bg-white border-2 border-stone-400">
      <div className="flex items-center">
        <div className="ml-2">
          <div className="text-lg font-bold">Speech to Text</div>
          <div className="text-gray-500">
            Language: {data.language || 'English'}
            {data.confidence && ` | Confidence: ${(data.confidence * 100).toFixed(1)}%`}
          </div>
        </div>
      </div>

      <Handle
        type="target"
        position={Position.Left}
        id="audio"
      />
      <Handle
        type="source"
        position={Position.Right}
        id="text"
      />
    </div>
  );
}

export default memo(SpeechToTextNode);
