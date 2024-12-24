import React, { memo, useCallback } from 'react';
import { Handle, Position, NodeProps, useReactFlow } from 'reactflow';

interface TextGenerationData {
  label?: string;
  model?: string;
  maxTokens?: number;
}

function TextGenerationNode({ data, id }: NodeProps<TextGenerationData>) {
  const { setNodes } = useReactFlow();

  const onHandleClick = useCallback((e: React.MouseEvent<HTMLDivElement>) => {
    const handle = e.currentTarget;
    const isSource = handle.classList.contains('react-flow__handle-right');
    
    // Add connecting class
    handle.classList.add('connecting');
    
    // Create connection line
    const connectionLine = document.querySelector('.react-flow__connectionline');
    if (connectionLine) {
      connectionLine.classList.add('visible');
    }

    // Track mouse movement
    const onMouseMove = (e: MouseEvent) => {
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
            const handleRect = handle.getBoundingClientRect();
            const handlePoint = svg.createSVGPoint();
            handlePoint.x = handleRect.left + handleRect.width / 2;
            handlePoint.y = handleRect.top + handleRect.height / 2;
            const handleTransformed = handlePoint.matrixTransform(ctm.inverse());

            const dx = Math.abs(transformed.x - handleTransformed.x);
            const controlPoint1X = handleTransformed.x + dx * 0.5;
            const controlPoint2X = transformed.x - dx * 0.5;

            connectionLine.setAttribute(
              'd',
              `M ${handleTransformed.x},${handleTransformed.y} C ${controlPoint1X},${handleTransformed.y} ${controlPoint2X},${transformed.y} ${transformed.x},${transformed.y}`
            );
          }
        }
      }
    };

    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('click', () => {
      handle.classList.remove('connecting');
      window.removeEventListener('mousemove', onMouseMove);
    }, { once: true });
  }, []);
  return (
    <div className="px-4 py-2 shadow-lg rounded-lg bg-gray-800 border-2 border-teal-500">
      <div className="p-2 -mx-4 -mt-2 mb-2 bg-gray-700 hover:bg-gray-600 transition-colors">
        <div className="flex items-center justify-between">
          <div className="text-lg font-bold text-white">Text Generation</div>
          <div className="text-xs bg-teal-500 text-white px-2 py-1 rounded">AI</div>
        </div>
      </div>
      <div className="space-y-1">
        <div className="text-gray-300">
          Model: <span className="text-teal-400">{data.model || 'GPT-3.5 Turbo'}</span>
        </div>
        <div className="text-gray-300">
          Max Tokens: <span className="text-teal-400">{data.maxTokens || 100}</span>
        </div>
      </div>

      <Handle
        type="target"
        position={Position.Left}
        id="prompt"
        onClick={onHandleClick}
        style={{ cursor: 'pointer' }}
      />
      <Handle
        type="source"
        position={Position.Right}
        id="text"
        onClick={onHandleClick}
        style={{ cursor: 'pointer' }}
      />
    </div>
  );
}

export default memo(TextGenerationNode);
