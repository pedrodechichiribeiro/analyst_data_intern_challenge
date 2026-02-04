import os
from agno.agent import Agent
from agno.models.google import Gemini

class AIAnalyst:
    def __init__(self):
        # Configure a chave aqui se necessário
        os.environ["GOOGLE_API_KEY"] = "AIzaSyACwcrqpecdgdIa4uJ-ndeb_fDM3jrZ-UY" 

        self.agent = Agent(
            # TENTATIVA 1: Versão Estável Específica (Recomendado)
            model=Gemini(id="gemini-2.5-flash"), 
            
            # Se a de cima não funcionar, tente esta (Versão 2.0 Experimental - Mais inteligente):
            # model=Gemini(id="gemini-2.0-flash-exp"),

            description="Você é um Cientista de Dados Sênior especialista em suporte técnico.",
            instructions=[
                "Analise os dados fornecidos focando em insights de negócio.",
                "Seja direto e profissional.",
                "Não use formatação Markdown (como negrito ou títulos).",
                "Use texto puro para compatibilidade com a interface gráfica.",
            ],
            markdown=False
        )

    def analyze(self, system_prompt, data_context):
        try:
            user_message = (
                f"CONTEXTO: {system_prompt}\n\n"
                f"DADOS:\n{data_context}\n\n"
                "Gere um relatório executivo curto sobre esses dados."
            )
            
            response = self.agent.run(user_message)
            return response.content

        except Exception as e:
            # Isso vai ajudar a gente a ver o erro exato na interface se falhar de novo
            return f"Erro Google Gemini: {str(e)}"