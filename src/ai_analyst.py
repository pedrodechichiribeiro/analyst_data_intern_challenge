import os
from pathlib import Path

# Robust path finding
current_path = Path(__file__).resolve()
BASE_DIR = current_path.parent.parent
# Check logic for 'models' folder in various locations
possible_paths = [
    current_path.parent / "models", # Same folder/models
    BASE_DIR / "models",            # Parent/models
    BASE_DIR / "src" / "models"     # Explicit src/models
]

MODELS_DIR = None
for p in possible_paths:
    if p.exists():
        MODELS_DIR = p
        break

try:
    from llama_cpp import Llama
    AI_AVAILABLE = True
except ImportError:
    print("WARNING: 'llama-cpp-python' not found. AI disabled.")
    AI_AVAILABLE = False
    Llama = None

class AIAnalyst:
    def __init__(self):
        self.llm = None
        self.model_filename = "gemma-3-4b-it-Q4_K_M.gguf"
        
        if not AI_AVAILABLE:
            return

        if MODELS_DIR is None:
            print("ERROR: 'models' directory not found.")
            return

        self.model_path = MODELS_DIR / self.model_filename
        
        if not self.model_path.exists():
            print(f"ERROR: Model file missing at {self.model_path}")
            print("Please download the .gguf model and place it in the 'models' folder.")
            return

        try:
            print(f"Loading AI Model from {self.model_path}...")
            # n_gpu_layers=-1 attempts to use GPU. If no GPU, it naturally falls back to CPU.
            self.llm = Llama(
                model_path=str(self.model_path),
                n_ctx=2048,      
                n_batch=512, 
                n_gpu_layers=-1, # <--- MAX PERFORMANCE 
                verbose=False     
            )
            print("AI Engine Online.")

        except Exception as e:
            print(f"AI Initialization Failed: {e}")
            self.llm = None

    def analyze(self, system_instructions, data_context):
        if not self.llm:
            if not AI_AVAILABLE:
                return "Error: AI Library not installed. Please run setup.py."
            return "Error: AI Model not loaded. Check console for 'models' folder path."
        
        full_prompt = f"""<start_of_turn>user
            INSTRUCTIONS: {system_instructions}
            STRICT CONTEXT DATA:
            {data_context}
            TASK:
            Provide a concise, professional analysis. 
            1. Highlight the most critical metric.
            2. Identify a potential cause.
            3. Recommend one actionable step.
            Keep it under 300 words.<end_of_turn>
            <start_of_turn>model
        """
        
        try:
            output = self.llm(
                full_prompt,
                max_tokens=900,
                temperature=0.3,
                stop=["<end_of_turn"]
            )
            return output['choices'][0]['text'].strip()
            
        except Exception as e:
            return f"Generation Error: {str(e)}"