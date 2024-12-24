import { NodeCategory, NodeType } from '../types/nodes';

export const nodeDefinitions: Record<string, NodeType> = {
  textGeneration: {
    id: 'textGeneration',
    name: 'Text Generation',
    description: 'Generate text using AI language models',
    category: NodeCategory.AI_SERVICE,
    version: '1.0.0',
    inputPorts: [
      {
        id: 'prompt',
        name: 'Prompt',
        dataSchema: {
          type: 'object',
          properties: {
            text: { type: 'string' }
          },
          required: ['text']
        },
        isRequired: true,
        allowMultiple: false,
        validationRules: []
      }
    ],
    outputPorts: [
      {
        id: 'text',
        name: 'Generated Text',
        dataSchema: {
          type: 'object',
          properties: {
            text: { type: 'string' }
          },
          required: ['text']
        },
        isRequired: true,
        allowMultiple: true,
        validationRules: []
      }
    ],
    configSchema: {
      type: 'object',
      properties: {
        model: {
          type: 'string',
          enum: ['GPT-3.5 Turbo', 'GPT-4']
        },
        maxTokens: {
          type: 'number',
          minimum: 1,
          maximum: 4096
        }
      },
      required: ['model', 'maxTokens']
    },
    style: {
      backgroundColor: '#1a1a1a',
      borderColor: '#3b82f6',
      icon: '🤖'
    }
  },

  speechToText: {
    id: 'speechToText',
    name: 'Speech to Text',
    description: 'Convert audio to text using AI',
    category: NodeCategory.AI_SERVICE,
    version: '1.0.0',
    inputPorts: [
      {
        id: 'audio',
        name: 'Audio Input',
        dataSchema: {
          type: 'object',
          properties: {
            audioData: { type: 'string' },
            format: { type: 'string' }
          },
          required: ['audioData']
        },
        isRequired: true,
        allowMultiple: false,
        validationRules: []
      }
    ],
    outputPorts: [
      {
        id: 'text',
        name: 'Transcribed Text',
        dataSchema: {
          type: 'object',
          properties: {
            text: { type: 'string' }
          },
          required: ['text']
        },
        isRequired: true,
        allowMultiple: true,
        validationRules: []
      }
    ],
    configSchema: {
      type: 'object',
      properties: {
        model: {
          type: 'string',
          enum: ['Whisper']
        }
      },
      required: ['model']
    },
    style: {
      backgroundColor: '#1a1a1a',
      borderColor: '#10b981',
      icon: '🎤'
    }
  },

  textToSpeech: {
    id: 'textToSpeech',
    name: 'Text to Speech',
    description: 'Convert text to speech using AI',
    category: NodeCategory.AI_SERVICE,
    version: '1.0.0',
    inputPorts: [
      {
        id: 'text',
        name: 'Text Input',
        dataSchema: {
          type: 'object',
          properties: {
            text: { type: 'string' }
          },
          required: ['text']
        },
        isRequired: true,
        allowMultiple: false,
        validationRules: []
      }
    ],
    outputPorts: [
      {
        id: 'audio',
        name: 'Generated Audio',
        dataSchema: {
          type: 'object',
          properties: {
            audioData: { type: 'string' },
            format: { type: 'string' }
          },
          required: ['audioData', 'format']
        },
        isRequired: true,
        allowMultiple: true,
        validationRules: []
      }
    ],
    configSchema: {
      type: 'object',
      properties: {
        voice: {
          type: 'string',
          enum: ['Default', 'Male', 'Female']
        }
      },
      required: ['voice']
    },
    style: {
      backgroundColor: '#1a1a1a',
      borderColor: '#8b5cf6',
      icon: '🔊'
    }
  },

  imageGeneration: {
    id: 'imageGeneration',
    name: 'Image Generation',
    description: 'Generate images using AI models',
    category: NodeCategory.AI_SERVICE,
    version: '1.0.0',
    inputPorts: [
      {
        id: 'prompt',
        name: 'Prompt',
        dataSchema: {
          type: 'object',
          properties: {
            text: { type: 'string' }
          },
          required: ['text']
        },
        isRequired: true,
        allowMultiple: false,
        validationRules: []
      }
    ],
    outputPorts: [
      {
        id: 'image',
        name: 'Generated Image',
        dataSchema: {
          type: 'object',
          properties: {
            imageData: { type: 'string' },
            format: { type: 'string' }
          },
          required: ['imageData', 'format']
        },
        isRequired: true,
        allowMultiple: true,
        validationRules: []
      }
    ],
    configSchema: {
      type: 'object',
      properties: {
        model: {
          type: 'string',
          enum: ['DALL-E']
        }
      },
      required: ['model']
    },
    style: {
      backgroundColor: '#1a1a1a',
      borderColor: '#ec4899',
      icon: '🎨'
    }
  }
};
