import React, { useState } from 'react';
import { nodeDefinitions } from '../../config/nodeDefinitions';
import { NodeCategory } from '../../types/nodes';

interface ToolbarProps {
  onAddNode: (type: string) => void;
}

function Toolbar({ onAddNode }: ToolbarProps) {
  const [selectedCategory, setSelectedCategory] = useState<NodeCategory | null>(null);

  // Group nodes by category
  const nodesByCategory = Object.entries(nodeDefinitions).reduce((acc, [nodeId, nodeDef]) => {
    const category = nodeDef.category;
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push({ nodeId, ...nodeDef });
    return acc;
  }, {} as Record<NodeCategory, Array<typeof nodeDefinitions[keyof typeof nodeDefinitions] & { nodeId: string }>>);

  const categories = Object.values(NodeCategory);

  return (
    <div className="absolute top-4 left-4 z-10 bg-gray-800 rounded-lg shadow-lg border border-gray-700">
      <div className="p-2 space-y-2">
        {/* Category Tabs */}
        <div className="flex space-x-1 bg-gray-900 rounded-md p-1">
          {categories.map((category) => (
            <button
              key={category}
              className={`px-3 py-1.5 text-sm rounded-md transition-colors ${
                selectedCategory === category
                  ? 'bg-blue-500 text-white'
                  : 'text-gray-400 hover:text-white hover:bg-gray-700'
              }`}
              onClick={() => setSelectedCategory(
                selectedCategory === category ? null : category
              )}
            >
              {category.replace(/_/g, ' ')}
            </button>
          ))}
        </div>

        {/* Node List */}
        {selectedCategory && nodesByCategory[selectedCategory] && (
          <div className="grid grid-cols-1 gap-1 min-w-[200px]">
            {nodesByCategory[selectedCategory].map((node) => (
              <button
                key={node.nodeId}
                className="flex items-center space-x-2 px-3 py-2 text-sm text-gray-300 hover:bg-gray-700 rounded-md transition-colors"
                onClick={() => onAddNode(node.nodeId)}
              >
                {node.style?.icon && (
                  <span className="text-lg">{node.style.icon}</span>
                )}
                <span>{node.name}</span>
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Toolbar;
