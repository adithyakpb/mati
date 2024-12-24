import React from 'react';
import { Node } from 'reactflow';
import { JSONSchema, PortDefinition } from '../../types/nodes';

interface NodePropertiesProps {
  node: Node;
  onChange: (nodeId: string, propertyKey: string, value: unknown) => void;
}

function NodeProperties({ node, onChange }: NodePropertiesProps) {
  const { nodeType, configuration } = node.data;

  const renderPropertyInput = (key: string, schema: JSONSchema, value: unknown) => {
    if (schema.enum) {
      return (
        <select
          className="w-full bg-gray-700 text-white rounded px-2 py-1"
          value={value as string}
          onChange={(e) => onChange(node.id, key, e.target.value)}
        >
          {schema.enum.map((option) => (
            <option key={String(option)} value={String(option)}>
              {String(option)}
            </option>
          ))}
        </select>
      );
    }

    switch (schema.type) {
      case 'number':
        return (
          <input
            type="number"
            className="w-full bg-gray-700 text-white rounded px-2 py-1"
            value={value as number}
            min={schema.minimum}
            max={schema.maximum}
            onChange={(e) => onChange(node.id, key, Number(e.target.value))}
          />
        );
      case 'boolean':
        return (
          <input
            type="checkbox"
            className="bg-gray-700 text-blue-500 rounded"
            checked={value as boolean}
            onChange={(e) => onChange(node.id, key, e.target.checked)}
          />
        );
      default:
        return (
          <input
            type="text"
            className="w-full bg-gray-700 text-white rounded px-2 py-1"
            value={value as string}
            onChange={(e) => onChange(node.id, key, e.target.value)}
          />
        );
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center space-x-2">
        {nodeType.style?.icon && (
          <span className="text-xl">{nodeType.style.icon}</span>
        )}
        <h2 className="text-lg font-bold">{nodeType.name}</h2>
      </div>
      
      <div className="text-sm text-gray-400">{nodeType.description}</div>

      <div className="space-y-3">
        {Object.entries(nodeType.configSchema.properties || {}).map(([key, schema]) => (
          <div key={key} className="space-y-1">
            <label className="block text-sm font-medium text-gray-300">
              {key}
              {nodeType.configSchema.required?.includes(key) && (
                <span className="text-red-500 ml-1">*</span>
              )}
            </label>
            {(schema as JSONSchema).description && (
              <div className="text-xs text-gray-500">{(schema as JSONSchema).description}</div>
            )}
            {renderPropertyInput(key, schema as JSONSchema, configuration[key])}
          </div>
        ))}
      </div>

      <div className="pt-4 border-t border-gray-700">
        <h3 className="text-sm font-medium text-gray-300 mb-2">Ports</h3>
        
        <div className="space-y-4">
          <div>
            <h4 className="text-xs font-medium text-gray-400 mb-1">Inputs</h4>
            <div className="space-y-1">
              {nodeType.inputPorts.map((port: PortDefinition) => (
                <div key={port.id} className="text-sm text-gray-300 flex items-center">
                  <span className="w-2 h-2 bg-blue-500 rounded-full mr-2" />
                  {port.name}
                  {port.isRequired && <span className="text-red-500 ml-1">*</span>}
                </div>
              ))}
            </div>
          </div>

          <div>
            <h4 className="text-xs font-medium text-gray-400 mb-1">Outputs</h4>
            <div className="space-y-1">
              {nodeType.outputPorts.map((port: PortDefinition) => (
                <div key={port.id} className="text-sm text-gray-300 flex items-center">
                  <span className="w-2 h-2 bg-blue-500 rounded-full mr-2" />
                  {port.name}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default NodeProperties;
