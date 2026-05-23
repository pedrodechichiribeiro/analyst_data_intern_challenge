import os
import logging
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.google import Gemini

# Load environment variables
load_dotenv()

# Set up basic logging for context size warnings
logger = logging.getLogger(__name__)

class AIAnalyst:
    def __init__(self) -> None:
        """
        Initializes the Agno Agent with specific fine-tuning for 
        IT Support and Data Analysis contexts using Gemini 3.5 Flash.
        """
        self.agent = Agent(
            model=Gemini(id="gemini-3.5-flash"), 
            
            # --- FINE TUNING & PERSONA ---
            description=(
                "You are a Senior Data Analyst specializing in IT Service Desk operations, "
                "Customer Support metrics, and Business Intelligence."
            ),
            
            # --- CONTEXT & INSTRUCTIONS ---
            instructions=[
                "You are analyzing data from a Technical Support Dashboard.",
                "Your analysis should focus on operational efficiency, team performance, and product quality.",
                "If analyzing 'Backlog', warn about diverging trends (incoming > resolved).",
                "If analyzing 'Severity', distinguish between high-volume noise vs. critical blockers.",
                "If analyzing 'Resolution Time', identify inefficiencies or 'stale' tickets.",
                "If analyzing 'Hotspots', suggest regional resource allocation.",
                "If analyzing 'Volume Trend', identify if the load is scaling up or stabilizing.",
                "Provide actionable insights, not just descriptions of the numbers.",
                "Be concise, professional, and executive.",
                
                # UI Constraints
                "STRICT FORMATTING RULE: Do NOT use Markdown formatting.",
                "Do NOT use bold (**text**), headers (##), or code blocks.",
                "Use standard plain text with line breaks and hyphens (-) for lists.",
            ],
            markdown=False
        )

    def analyze(self, analysis_objective: str, data_context: str) -> tuple[bool, str]:
        """
        Sends the specific graph context and raw data to the Cloud AI.
        
        Returns:
            tuple: (success_status: bool, response_content: str)
        """
        # Defensive check: ~1M tokens is roughly 3.5M characters
        if len(data_context) > 3_500_000:
            logger.warning("Data context is extremely large and may approach API token limits.")

        try:
            user_message = (
                f"--- ANALYSIS OBJECTIVE ---\n"
                f"{analysis_objective}\n\n"
                
                f"--- DATASET ---\n"
                f"{data_context}\n\n"
                
                f"--- REQUEST ---\n"
                "Based on the objective and the dataset above, generate a deep insight report. "
                "Highlight risks, trends, and recommended actions."
            )
            
            response = self.agent.run(user_message)
            return True, response.content

        except Exception as e:
            error_msg = f"AI Service Error: {str(e)}"
            logger.error(error_msg)
            return False, error_msg