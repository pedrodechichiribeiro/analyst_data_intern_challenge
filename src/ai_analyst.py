import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"

try:
    from llama_cpp import Llama
except ImportError:
    print("CRITICAL: 'llama-cpp-python' library not found. Please run: setup.py")
    Llama = None

class AIAnalyst:
    def __init__(self):
        print("Initializing AI Analyst (Gemma 3 4B Quantized)...")
        self.model_filename = "gemma-3-4b-it-Q4_K_M.gguf" 
        self.model_path = MODELS_DIR / self.model_filename
        model_path_str = str(self.model_path)

        if not os.path.exists(model_path_str):
            print(f"CRITICAL ERROR: Model file not found at {model_path_str}")
            print(f"Please download '{self.model_filename}' and place it in the 'models' folder.") # Updated instruction
            self.llm = None
            return
        
        if Llama is None:
            self.llm = None
            return

        try:
            # Initialize the AI model using llama-cpp-python
            self.llm = Llama(
                model_path=model_path_str,
                n_ctx=2048,      
                n_batch=512, 
                n_gpu_layers=0,   
                verbose=False     
            )

            print(f"AI Model ({self.model_filename}) loaded successfully.")

        except Exception as e:
            print(f"AI Load failed: {e}")
            self.llm = None

    def analyze(self, system_instructions, data_context):
        if not self.llm:
            return "AI module not active or library missing."
        
        # Gemma does not have a specific 'System' role tag. 
        # Standard practice is to prepend system instructions to the first User turn.
        
        full_prompt = f"""<start_of_turn>user
            INSTRUCTIONS: {system_instructions}
            STRICT CONTEXT DATA:
            {data_context}
            TASK:
            Provide a concise, professional analysis of the data above. 
            1. Highlight the most critical metric.
            2. Identify a potential cause.
            3. Recommend one actionable step.
            Keep it under 300 words.<end_of_turn>
            <start_of_turn>model
        """
        
        # The data_context and system_instructions changes according with the data selected for analysis, i.e. different data will change so the generated texts
        # maintains a minimum logic. A bigger data_context, AI model and further fine tuning will produce exponentially better results and through analysis.
        # Alas, this is just a proof of concept/demonstration meant to run on any marginally modern machine, so the model is small.
            
        # Generate response
        try:
            output = self.llm(
                full_prompt,
                max_tokens=900,
                temperature=0.3,
                top_p=0.9,
                top_k=40,
                repeat_penalty=1.1,
                stop=["<end_of_turn"]
            )
            # Extract text from the standard OpenAI-like response format of llama-cpp-python
            return output['choices'][0]['text'].strip()
            
        except Exception as e:
            return f"Error during generation: {str(e)}"