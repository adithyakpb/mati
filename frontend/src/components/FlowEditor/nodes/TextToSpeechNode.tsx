import React, { memo } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

interface TextToSpeechData {
  label?: string;
  voice?: string;
  speed?: number;
  duration?: number;
}

function TextToSpeechNode({ data }: NodeProps<TextToSpeechData>) {
  return (
    <div className="px-4 py-2 shadow-md rounded-md bg-white border-2 border-stone-400">
      <div className="flex items-center">
        <div className="ml-2">
          <div className="text-lg font-bold">Text to Speech</div>
          <div className="text-gray-500">
            Voice: {data.voice || 'Default'}
            {data.speed && ` | Speed: ${data.speed}x`}
            {data.duration && ` | Duration: ${data.duration.toFixed(1)}s`}
          </div>
        </div>
      </div>

      <Handle
        type="target"
        position={Position.Left}
        id="text"
      />
      <Handle
        type="source"
        position={Position.Right}
        id="audio"
      />
    </div>
  );
}

export default memo(TextToSpeechNode);
