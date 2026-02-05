import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.google import Gemini

# Load environment variables (API keys)
load_dotenv()

class AIAnalyst:
    def __init__(self):
        """
        Initializes the Agno Agent with specific fine-tuning for 
        IT Support and Data Analysis contexts using Gemini 2.5 Flash.
        """
        self.agent = Agent(
            model=Gemini(id="gemini-2.5-flash"), 
            
            # --- FINE TUNING & PERSONA ---
            description=(
                "You are a Senior Data Analyst specializing in IT Service Desk operations, "
                "Customer Support metrics, and Business Intelligence."
            ),
            
            # --- CONTEXT & INSTRUCTIONS ---
            instructions=[
                # 1. Operational Context
                "You are analyzing data from a Technical Support Dashboard.",
                "Your analysis should focus on operational efficiency, team performance, and product quality.",
                
                # 2. Specific Analytical Behaviors (Matching your App's logic)
                "If analyzing 'Backlog', warn about diverging trends (incoming > resolved).",
                "If analyzing 'Severity', distinguish between high-volume noise vs. critical blockers.",
                "If analyzing 'Resolution Time', identify inefficiencies or 'stale' tickets.",
                "If analyzing 'Hotspots', suggest regional resource allocation.",
                "If analyzing 'Volume Trend', identify if the load is scaling up or stabilizing.",
                
                # 3. Tone and Style
                "Provide actionable insights, not just descriptions of the numbers.",
                "Be concise, professional, and executive.",
                
                # 4. Technical Constraints (Crucial for Tkinter UI)
                "STRICT FORMATTING RULE: Do NOT use Markdown formatting.",
                "Do NOT use bold (**text**), headers (##), or code blocks.",
                "Use standard plain text with line breaks and hyphens (-) for lists.",
            ],
            markdown=False
        )

    def analyze(self, system_prompt, data_context):
        """
        Sends the specific graph context and raw data to the Cloud AI.
        """
        try:
            # Structuring the prompt to clearly separate objective from data
            user_message = (
                f"--- ANALYSIS OBJECTIVE ---\n"
                f"{system_prompt}\n\n"
                
                f"--- DATASET ---\n"
                f"{data_context}\n\n"
                
                f"--- REQUEST ---\n"
                "Based on the objective and the dataset above, generate a deep insight report. "
                "Highlight risks, trends, and recommended actions."
            )
            
            response = self.agent.run(user_message)
            return response.content

        except Exception as e:
            return f"AI Service Error: {str(e)}"