from .bedrock_service import BedrockService

class AIService:
    def __init__(self):
        self.bedrock_service = BedrockService()
    
    def generate_text(self, question: str):

        prompt = self.build_prompt(question)
        return self.bedrock_service.invoke_model(prompt)
    
    def build_prompt(self, question: str) -> str:
        return f"""

        you are an expert assistant.
        Provide a clear and short 
        
        Question
        {question}
        """
