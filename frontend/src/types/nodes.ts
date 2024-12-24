export enum NodeCategory {
  AI_SERVICE = 'AI_SERVICE',
  DATA_CONNECTOR = 'DATA_CONNECTOR',
  FLOW_CONTROL = 'FLOW_CONTROL',
  STATE_MANAGEMENT = 'STATE_MANAGEMENT',
  TRANSFORMER = 'TRANSFORMER',
  INPUT_OUTPUT = 'INPUT_OUTPUT'
}

export interface JSONSchema {
  type: string;
  properties?: Record<string, JSONSchema>;
  required?: string[];
  additionalProperties?: boolean;
  // Additional validation properties
  enum?: Array<string | number>;
  minimum?: number;
  maximum?: number;
  minLength?: number;
  maxLength?: number;
  pattern?: string;
  format?: string;
  description?: string;
}

export interface ValidationRule {
  type: string;
  params?: Record<string, unknown>;
}

export interface PortDefinition {
  id: string;
  name: string;
  dataSchema: JSONSchema;
  isRequired: boolean;
  allowMultiple: boolean;
  validationRules: ValidationRule[];
}

export interface NodeType {
  id: string;
  category: NodeCategory;
  version: string;
  name: string;
  description: string;
  inputPorts: PortDefinition[];
  outputPorts: PortDefinition[];
  configSchema: JSONSchema;
  style?: {
    backgroundColor?: string;
    borderColor?: string;
    icon?: string;
  };
}

export interface Connection {
  id: string;
  name?: string;
  sourceNode: string;
  sourcePort: string;
  targetNode: string;
  targetPort: string;
  transformationRules?: TransformationRule[];
}

export interface TransformationRule {
  type: string;
  params?: Record<string, unknown>;
}

export interface Position {
  x: number;
  y: number;
}

export interface WorkflowNode {
  id: string;
  type: string;
  configuration: Record<string, unknown>;
  position: Position;
}

export interface WorkflowMetadata {
  name: string;
  description: string;
  version: string;
  created: string;
  modified: string;
  author: string;
}

export interface StateDefinition {
  variables: Record<string, JSONSchema>;
}

export interface Workflow {
  id: string;
  version: string;
  nodes: WorkflowNode[];
  connections: Connection[];
  inputSchema: JSONSchema;
  outputSchema: JSONSchema;
  metadata: WorkflowMetadata;
  globalState: StateDefinition;
}
