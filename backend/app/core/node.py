from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class NodeRunner(ABC):
    """Base class for all node runners"""
    
    @abstractmethod
    async def execute(
        self,
        inputs: Dict[str, Any],
        config: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute the node's operation
        
        Args:
            inputs: Input values for the node's input ports
            config: Node configuration values
            context: Execution context (run_id, etc.)
            
        Returns:
            Dict mapping output port names to their values
        """
        pass

    def validate_inputs(self, inputs: Dict[str, Any], port_specs: Dict[str, Any]) -> None:
        """Validate input values against port specifications"""
        for port_name, spec in port_specs.items():
            if spec.get("required", True) and port_name not in inputs:
                raise ValueError(f"Required input port '{port_name}' has no value")
            
            if port_name in inputs:
                value = inputs[port_name]
                if "type" in spec:
                    self._validate_type(value, spec["type"], port_name)
                
                if "validator" in spec:
                    try:
                        spec["validator"](value)
                    except Exception as e:
                        raise ValueError(
                            f"Validation failed for input port '{port_name}': {str(e)}"
                        )

    def validate_outputs(self, outputs: Dict[str, Any], port_specs: Dict[str, Any]) -> None:
        """Validate output values against port specifications"""
        for port_name, spec in port_specs.items():
            if spec.get("required", True) and port_name not in outputs:
                raise ValueError(f"Required output port '{port_name}' has no value")
            
            if port_name in outputs:
                value = outputs[port_name]
                if "type" in spec:
                    self._validate_type(value, spec["type"], port_name)
                
                if "validator" in spec:
                    try:
                        spec["validator"](value)
                    except Exception as e:
                        raise ValueError(
                            f"Validation failed for output port '{port_name}': {str(e)}"
                        )

    def _validate_type(self, value: Any, expected_type: str, port_name: str) -> None:
        """Validate value against expected type"""
        type_mapping = {
            "string": str,
            "number": (int, float),
            "integer": int,
            "boolean": bool,
            "array": list,
            "object": dict
        }
        
        if expected_type in type_mapping:
            expected = type_mapping[expected_type]
            if not isinstance(value, expected):
                raise ValueError(
                    f"Invalid type for port '{port_name}'. "
                    f"Expected {expected_type}, got {type(value).__name__}"
                )

class TextGenerationNode(NodeRunner):
    """Node for generating text using language models"""
    
    async def execute(
        self,
        inputs: Dict[str, Any],
        config: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        # Validate inputs
        self.validate_inputs(inputs, {
            "prompt": {
                "type": "string",
                "required": True,
                "description": "The prompt text to generate from"
            },
            "max_tokens": {
                "type": "integer",
                "required": False,
                "description": "Maximum number of tokens to generate"
            }
        })
        
        # TODO: Implement actual text generation using configured model
        # For now, return dummy response
        response = f"Generated text for prompt: {inputs['prompt']}"
        
        outputs = {
            "text": response,
            "tokens": len(response.split())
        }
        
        # Validate outputs
        self.validate_outputs(outputs, {
            "text": {
                "type": "string",
                "required": True,
                "description": "The generated text"
            },
            "tokens": {
                "type": "integer",
                "required": True,
                "description": "Number of tokens in generated text"
            }
        })
        
        return outputs

class SpeechToTextNode(NodeRunner):
    """Node for converting speech to text"""
    
    async def execute(
        self,
        inputs: Dict[str, Any],
        config: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        # Validate inputs
        self.validate_inputs(inputs, {
            "audio": {
                "type": "string",  # Base64 encoded audio data
                "required": True,
                "description": "Audio data to transcribe"
            }
        })
        
        # TODO: Implement actual speech-to-text conversion
        # For now, return dummy response
        outputs = {
            "text": "Transcribed text would appear here",
            "confidence": 0.95
        }
        
        # Validate outputs
        self.validate_outputs(outputs, {
            "text": {
                "type": "string",
                "required": True,
                "description": "The transcribed text"
            },
            "confidence": {
                "type": "number",
                "required": True,
                "description": "Confidence score of transcription"
            }
        })
        
        return outputs

class TextToSpeechNode(NodeRunner):
    """Node for converting text to speech"""
    
    async def execute(
        self,
        inputs: Dict[str, Any],
        config: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        # Validate inputs
        self.validate_inputs(inputs, {
            "text": {
                "type": "string",
                "required": True,
                "description": "Text to convert to speech"
            },
            "voice": {
                "type": "string",
                "required": False,
                "description": "Voice ID to use"
            }
        })
        
        # TODO: Implement actual text-to-speech conversion
        # For now, return dummy response
        outputs = {
            "audio": "base64_encoded_audio_data_would_be_here",
            "duration": 3.5
        }
        
        # Validate outputs
        self.validate_outputs(outputs, {
            "audio": {
                "type": "string",
                "required": True,
                "description": "Base64 encoded audio data"
            },
            "duration": {
                "type": "number",
                "required": True,
                "description": "Duration of audio in seconds"
            }
        })
        
        return outputs

class ImageGenerationNode(NodeRunner):
    """Node for generating images"""
    
    async def execute(
        self,
        inputs: Dict[str, Any],
        config: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        # Validate inputs
        self.validate_inputs(inputs, {
            "prompt": {
                "type": "string",
                "required": True,
                "description": "Text prompt for image generation"
            },
            "style": {
                "type": "string",
                "required": False,
                "description": "Style to apply to the generated image"
            }
        })
        
        # TODO: Implement actual image generation
        # For now, return dummy response
        outputs = {
            "image": "base64_encoded_image_data_would_be_here",
            "width": 512,
            "height": 512
        }
        
        # Validate outputs
        self.validate_outputs(outputs, {
            "image": {
                "type": "string",
                "required": True,
                "description": "Base64 encoded image data"
            },
            "width": {
                "type": "integer",
                "required": True,
                "description": "Width of generated image"
            },
            "height": {
                "type": "integer",
                "required": True,
                "description": "Height of generated image"
            }
        })
        
        return outputs
