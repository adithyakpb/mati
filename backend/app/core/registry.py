from typing import Dict, Type
from .node import (
    NodeRunner,
    TextGenerationNode,
    SpeechToTextNode,
    TextToSpeechNode,
    ImageGenerationNode
)

class NodeRegistry:
    """Registry for node types and their implementations"""
    
    def __init__(self):
        self._runners: Dict[str, Type[NodeRunner]] = {}
    
    def register(self, node_type: str, runner_class: Type[NodeRunner]) -> None:
        """Register a node runner for a node type"""
        if node_type in self._runners:
            raise ValueError(f"Node type '{node_type}' is already registered")
        self._runners[node_type] = runner_class
    
    def get_runner(self, node_type: str) -> Type[NodeRunner]:
        """Get the runner class for a node type"""
        if node_type not in self._runners:
            raise ValueError(f"Unknown node type: {node_type}")
        return self._runners[node_type]
    
    def list_types(self) -> list[str]:
        """List all registered node types"""
        return list(self._runners.keys())
    
    def __contains__(self, node_type: str) -> bool:
        return node_type in self._runners
    
    def __getitem__(self, node_type: str) -> Type[NodeRunner]:
        return self.get_runner(node_type)

# Create global registry instance
node_registry = NodeRegistry()

# Register built-in node types
node_registry.register("text-generation", TextGenerationNode)
node_registry.register("speech-to-text", SpeechToTextNode)
node_registry.register("text-to-speech", TextToSpeechNode)
node_registry.register("image-generation", ImageGenerationNode)

# Example node type metadata for registration in database:
NODE_TYPE_SPECS = {
    "text-generation": {
        "name": "Text Generation",
        "category": "AI",
        "description": "Generate text using language models",
        "version": "1.0.0",
        "input_ports": [
            {
                "name": "prompt",
                "data_type": "string",
                "description": "The prompt text to generate from",
                "required": True
            },
            {
                "name": "max_tokens",
                "data_type": "integer",
                "description": "Maximum number of tokens to generate",
                "required": False,
                "default_value": 100
            }
        ],
        "output_ports": [
            {
                "name": "text",
                "data_type": "string",
                "description": "The generated text",
                "required": True
            },
            {
                "name": "tokens",
                "data_type": "integer",
                "description": "Number of tokens in generated text",
                "required": True
            }
        ],
        "config_schema": {
            "type": "object",
            "properties": {
                "model": {
                    "type": "string",
                    "enum": ["gpt-3.5-turbo", "gpt-4"],
                    "description": "The model to use for text generation"
                },
                "temperature": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 2,
                    "default": 0.7,
                    "description": "Controls randomness in the output"
                }
            },
            "required": ["model"]
        }
    },
    "speech-to-text": {
        "name": "Speech to Text",
        "category": "AI",
        "description": "Convert speech audio to text",
        "version": "1.0.0",
        "input_ports": [
            {
                "name": "audio",
                "data_type": "string",
                "description": "Base64 encoded audio data",
                "required": True
            }
        ],
        "output_ports": [
            {
                "name": "text",
                "data_type": "string",
                "description": "The transcribed text",
                "required": True
            },
            {
                "name": "confidence",
                "data_type": "number",
                "description": "Confidence score of transcription",
                "required": True
            }
        ],
        "config_schema": {
            "type": "object",
            "properties": {
                "language": {
                    "type": "string",
                    "default": "en",
                    "description": "Language code for transcription"
                },
                "model": {
                    "type": "string",
                    "enum": ["base", "enhanced"],
                    "default": "base",
                    "description": "Model to use for transcription"
                }
            }
        }
    },
    "text-to-speech": {
        "name": "Text to Speech",
        "category": "AI",
        "description": "Convert text to speech audio",
        "version": "1.0.0",
        "input_ports": [
            {
                "name": "text",
                "data_type": "string",
                "description": "Text to convert to speech",
                "required": True
            },
            {
                "name": "voice",
                "data_type": "string",
                "description": "Voice ID to use",
                "required": False
            }
        ],
        "output_ports": [
            {
                "name": "audio",
                "data_type": "string",
                "description": "Base64 encoded audio data",
                "required": True
            },
            {
                "name": "duration",
                "data_type": "number",
                "description": "Duration of audio in seconds",
                "required": True
            }
        ],
        "config_schema": {
            "type": "object",
            "properties": {
                "voice": {
                    "type": "string",
                    "description": "Voice ID to use"
                },
                "speed": {
                    "type": "number",
                    "minimum": 0.5,
                    "maximum": 2.0,
                    "default": 1.0,
                    "description": "Speech speed multiplier"
                }
            }
        }
    },
    "image-generation": {
        "name": "Image Generation",
        "category": "AI",
        "description": "Generate images from text descriptions",
        "version": "1.0.0",
        "input_ports": [
            {
                "name": "prompt",
                "data_type": "string",
                "description": "Text prompt for image generation",
                "required": True
            },
            {
                "name": "style",
                "data_type": "string",
                "description": "Style to apply to the generated image",
                "required": False
            }
        ],
        "output_ports": [
            {
                "name": "image",
                "data_type": "string",
                "description": "Base64 encoded image data",
                "required": True
            },
            {
                "name": "width",
                "data_type": "integer",
                "description": "Width of generated image",
                "required": True
            },
            {
                "name": "height",
                "data_type": "integer",
                "description": "Height of generated image",
                "required": True
            }
        ],
        "config_schema": {
            "type": "object",
            "properties": {
                "model": {
                    "type": "string",
                    "enum": ["dall-e-2", "dall-e-3", "stable-diffusion"],
                    "description": "Model to use for image generation"
                },
                "size": {
                    "type": "string",
                    "enum": ["256x256", "512x512", "1024x1024"],
                    "default": "512x512",
                    "description": "Size of generated image"
                },
                "num_images": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 4,
                    "default": 1,
                    "description": "Number of images to generate"
                }
            },
            "required": ["model"]
        }
    }
}
