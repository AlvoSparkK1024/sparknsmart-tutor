import os
import google.generativeai as genai
from typing import Dict, Any, List
import base64
from PIL import Image
from io import BytesIO

class NotebookLMAgent:
    """Agent that uses Gemini and Imagen to generate lecture scripts and visual images."""
    def __init__(self):
        self.model = None
        self.imagen_model = None
        self.runtime = None

    async def initialize(self, runtime):
        self.runtime = runtime
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("GEMINI_API_KEY not set; generation disabled.")
            return
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Try to use Imagen for image generation
        try:
            self.imagen_model = genai.ImageGenerationModel('imagen-3.0-generate-001')
        except:
            print("Imagen model not available, will use text descriptions only")
        
        self.runtime.bus.subscribe("generate_explanation", self.handle_explanation_request)

    async def generate_image(self, prompt: str, index: int) -> str:
        """Generate an image using Imagen and save it."""
        try:
            if not self.imagen_model:
                return None
            
            # Generate image
            response = await self.imagen_model.generate_images_async(
                prompt=prompt,
                number_of_images=1
            )
            
            if response.images:
                # Save image
                os.makedirs("outputs/visuals", exist_ok=True)
                image_path = f"outputs/visuals/visual_{index}.png"
                response.images[0].save(image_path)
                return image_path
        except Exception as e:
            print(f"Error generating image: {e}")
            return None


    async def handle_explanation_request(self, data: Dict[str, Any]):
        """Generate explanation based on document and user question."""
        document = data.get("document", "")
        question = data.get("question", "")
        
        if not document or not question:
            return

        # Generate explanation with visual suggestions
        prompt = f"""
        You are an expert educator. Based on the following document, answer the user's question in a clear and engaging way.
        
        Document Content:
        {document}
        
        User Question:
        {question}
        
        Provide:
        1. A detailed explanation (2-3 paragraphs)
        2. Suggest 2-3 visual aids that would help understand this concept (describe what each visual should show)
        
        Format your response as:
        EXPLANATION:
        [Your detailed explanation here]
        
        VISUAL 1: [Description of first visual aid]
        VISUAL 2: [Description of second visual aid]
        VISUAL 3: [Description of third visual aid (if applicable)]
        """
        
        try:
            response = await self.model.generate_content_async(prompt)
            response_text = response.text
            
            # Parse response
            explanation = ""
            visual_prompts = []
            
            lines = response_text.split('\n')
            in_explanation = False
            
            for line in lines:
                if 'EXPLANATION:' in line:
                    in_explanation = True
                    continue
                elif line.startswith('VISUAL'):
                    in_explanation = False
                    # Extract visual description
                    visual_desc = line.split(':', 1)[1].strip() if ':' in line else line.strip()
                    visual_prompts.append(visual_desc)
                elif in_explanation and line.strip():
                    explanation += line + "\n"
            
            # Publish results
            await self.runtime.bus.publish("explanation_ready", {
                "explanation": explanation.strip(),
                "visual_prompts": visual_prompts
            })
            
        except Exception as e:
            print(f"Error generating explanation: {e}")
