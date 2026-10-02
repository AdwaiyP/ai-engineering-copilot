import json

from groq import Groq

from app.config import settings
from app.agent.tools import (
    list_files,
    read_file,
    search_code,
)

class AgentService:

    def __init__(self, retriever):
        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

        self.model = settings.GROQ_MODEL
        self.retriever = retriever
    
    def _tools(self):

        return [
            {
                "type": "function",
                "function": {
                    "name": "list_files",
                    "description": (
                        "List files in the currently indexed "
                        "GitHub repository."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {},
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "search_code",
                    "description": (
                        "Semantically search the indexed "
                        "repository for relevant source code."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": (
                                    "Description of the code "
                                    "to search for."
                                ),
                            },
                            "top_k": {
                                "type": "integer",
                                "default": 5,
                            },
                        },
                        "required": ["query"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": (
                        "Read a specific file from the "
                        "repository with line numbers."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                            },
                            "start_line": {
                                "type": "integer",
                                "default": 1,
                            },
                            "end_line": {
                                "type": "integer",
                                "default": 200,
                            },
                        },
                        "required": ["file_path"],
                    },
                },
            },
        ]
    
    def _execute_tool(self, name, arguments):

        if name == "list_files":
            return list_files()
        
        if name == "search_code":
            return search_code(
                query=arguments["query"],
                retriever=self.retriever,
                top_k=arguments.get("top_k", 5),
            )
        
        if name == "read_file":
            return read_file(
                file_path=arguments["file_path"],
                start_line=arguments.get(
                    "start_line",
                    1
                ),
                end_line=arguments.get(
                    "end_line",
                    200
                ),
            )
        
        raise ValueError(
            f"Unknown tool: {name}"
        )
    
    def run(
            self,
            question: str,
            max_iterations: int = 6
    ):
        
        messages = [
            {
                "role": "system",
                "content": """
You are an AI Engineering Copilot.

You have tools that allow you to investigate
the currently indexed software repository.

Use tools when necessary rather than guessing.

Available capabilities:
- list_files: understand repository structure
- search_code: semantically find relevant code
- read_file: inspect exact files and line ranges

When investigating implementation details:
1. Search for relevant code.
2. Read important files when necessary.
3. Base your final answer on the repository.
4. Mention relevant file paths.
5. Do not invent code that you have not inspected.
6. Explain your findings clearly and concisely.
""",
            },
            {
                "role": "user",
                "content": question,
            }
        ]

        tool_history = []

        for _ in range(max_iterations):

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self._tools(),
                tool_choice="auto",
                temperature=0.1,
            )

            message = response.choices[0].message

            if not message.tool_calls:

                return {
                    "answer": message.content,
                    "tools_used": tool_history,
                }
            
            messages.append(message)

            for tool_call in message.tool_calls:

                name = tool_call.function.name
                arguments = json.loads(
                     tool_call.function.arguments
                )
                
                try:
                    result = self._execute_tool(
                        name,
                        arguments
                    )
                except Exception as error:
                    result = {
                        "error": str(error)
                    }

                tool_history.append(
                    {
                        "tool":name,
                        "arguments":arguments,
                    }
                )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content":json.dumps(
                            result,
                            default=str
                        ),
                    }
                )

        return {
            "answer": (
                "I reached the maximum number of"
                "repository investigation steps."
            ),
            "tools_used": tool_history,
        }