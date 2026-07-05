from ai_service.src.infrastructure.models.interface.llmService import LlmService
from ollama import chat,ChatResponse
prompt:str=f"""
Analyze the following Java method.

Return ONLY JSON.

Method:

{{METHOD}}
"""
system:str="""
You are a senior Java Application Security auditor.

Your expertise includes:
- Java
- Spring Boot
- JDBC
- OWASP Top 10
- CWE
- Secure coding
- Static analysis

You must produce accurate security analyses.

Never invent vulnerabilities.

Only report vulnerabilities that can be reasonably inferred from the provided code.

Always return valid JSON.

Never return Markdown.
"""
class model(LlmService):
    def prompt(self,METHOD:str):
        response:ChatResponse=chat(
            model="qwen2.5:7b",messages=[
                {
                    "role":"user",
                    "content":prompt
                }
                ,{
                    "role":"system",
                    "content":system
                }
            ],stream=True
        )
