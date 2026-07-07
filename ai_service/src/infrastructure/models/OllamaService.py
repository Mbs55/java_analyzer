from src.infrastructure.models.interface.llmService import LlmService
from ollama import chat,ChatResponse,Client
from src.api.schemas.analyze import AnalyzeRequest,AnalyzeResponse
import json
import os

class model(LlmService):
    def prompt(self,rq:AnalyzeRequest):#->AnalyzeResponse:
        prompt:str=f"""
        Analyze the following Java method for security vulnerabilities.

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

        {rq.method}

        Return ONLY valid JSON.
        """
        system:str="""
        You are a senior Java Application Security Auditor.

        Your expertise includes:
        - Java
        - Spring Boot
        - JDBC
        - Hibernate
        - OWASP Top 10
        - CWE
        - Secure Coding
        - Static Code Analysis

        Your task is to analyze ONE Java method and detect security vulnerabilities.

        Rules:

        1. Return ONLY valid JSON.
        2. Do NOT return markdown.
        3. Do NOT use ```json.
        4. Do NOT include explanations outside the JSON.
        5. The JSON must exactly follow the schema below.
        6. If there are no vulnerabilities, return an empty vulnerabilities array.
        7. Use only the severity values:
           LOW
           MEDIUM
           HIGH
           CRITICAL
        8. Use only the status values:
           SAFE
           VULNERABLE
        9. confidence must be a number between 0.0 and 1.0.
        10. line must refer to the line number inside the provided method.
        11. Use official CWE identifiers when applicable.
        12.Your response MUST begin with '{' and end with '}'.
        13.Output ONLY the JSON object.
        14.Any text outside the JSON object is forbidden.
        15.The JSON schema is strict.
        16.Never add new fields.
        17.Never remove fields.
        18.Never rename fields.
        19.Never change the nesting.
        20.Never return null.
        21.Always return every required field.
        22.If there are no vulnerabilities, return:
        {
          "status": "SAFE",
          "overall_risk": "LOW",
          "confidence": 0.99,
          "summary": "No security vulnerabilities detected.",
          "vulnerabilities": []
        }

        23.Return exactly this JSON structure:

        {
          "status": "SAFE | VULNERABLE",
          "overall_risk": "LOW | MEDIUM | HIGH | CRITICAL",
          "confidence": 0.00,
          "summary": "",
          "vulnerabilities": [
            {
              "type": "",
              "severity": "LOW | MEDIUM | HIGH | CRITICAL",
              "cwe": "",
              "line": 0,
              "description": "",
              "recommendation": ""
            }
          ]
        }
        """
        METHOD=rq.method
        Host=os.getenv("OLLAMA_HOST")
        client=Client(host=Host)
        try:
            response:ChatResponse=client.chat(
                model="qwen2.5:7b",messages=[
                    {
                        "role":"system",
                        "content":system
                    },
                    {
                        "role":"user",
                        "content":prompt
                    }
                ],stream=False
            )
            result=json.loads(response.message.content)
            return AnalyzeResponse(**result)
        except Exception as e:
            return AnalyzeResponse()

# m=model()        
# req = AnalyzeRequest(
#     id=1,
#     method="""
# public User findUser(String username) {
#     String query = "SELECT * FROM users WHERE username = '" + username + "'";
#     return jdbcTemplate.queryForObject(query, ...);
# }
# """
# )
# print(m.prompt(req))
