from src.infrastructure.models.interface.llmService import LlmService
from ollama import chat,ChatResponse,Client
from src.api.schemas.analyze import AnalyzeRequest,AnalyzeResponse
import json
import os
from fastapi.concurrency import run_in_threadpool

class model(LlmService):
    async def prompt(self,req:AnalyzeRequest)->AnalyzeResponse:
        METHOD=req.method
        prompt:str=f"""
        Analyze the following Java method for security vulnerabilities.
        Analyze the following Java method.

        Requirements:

        - Examine every line.
        - Detect ALL vulnerabilities.
        - Report every finding independently.
        - Never stop after the first vulnerability.
        - Use the JSON schema defined in the system prompt.

        Detect issues such as:
        - SQL Injection
        - XSS
        - Command Injection
        - Path Traversal
        - Hardcoded Secrets
        - Insecure Deserialization
        - SSRF
        - XXE
        - LDAP Injection
        - Code Injection
        - Authentication flaws
        - Authorization flaws
        - Sensitive Data Exposure
        - Cryptographic issues
        - Any OWASP Top 10 vulnerability
        - Any relevant CWE

        Java Method:

        {METHOD}

        Return ONLY valid JSON.
        """
        Host:str=os.getenv("OLLAMA_HOST")
        client=Client(host=Host)
        response:ChatResponse=await run_in_threadpool(
            client.chat,model="java-auditor2",
            messages=[{"role":"user","content":prompt}],stream=False
        )
        print(prompt)
        result=json.loads(response.message.content)
        return AnalyzeResponse(**result)
