from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.llm.groq_service import GroqService
from app.services.github_service import clone_github_repository
from app.services.repository_context import repository_context
from app.rag.retriever import Retriever
from app.services.repository_service import read_repository
from app.agent.agent_service import AgentService



router = APIRouter()

retriever = Retriever()
agent = AgentService(retriever)
llm = GroqService()

class GitHubIndexRequest(BaseModel):
    github_url: str

class IndexRequest(BaseModel):
    repository_path: str

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

@router.post("/agent/chat")
def agent_chat(request: QueryRequest):

    try:

        result = agent.run(
            request.query
        )

        return result

    except RuntimeError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )




@router.post("/index/github")
def index_github_repository(
    request: GitHubIndexRequest
):

    try:

        repository_path, repository_name = (
            clone_github_repository(
                request.github_url
            )
        )
        
        repository_context.set_repository(
            repository_path,
            repository_name
        )

        chunks = read_repository(
            repository_path
        )

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Repository cloned successfully, "
                    "but no supported source files were found."
                )
            )

        retriever.index_chunks(chunks)

        return {
            "message": "GitHub repository indexed successfully",
            "repository": repository_name,
            "repository_path": repository_path,
            "chunks": len(chunks)
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except RuntimeError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

@router.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "AI Engineering Copilot"
    }

@router.post("/index")
def index_repository(request: IndexRequest):

    try:
        chunks = read_repository(
            request.repository_path
        )
        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No supported source files found."
            )
        retriever.index_chunks(chunks)

        return {
            "message":"Repository indexed successfully",
            "chunks":len(chunks)
        }
    except FileNotFoundError as error:
        raise HTTPException(
            status_code=404,
            details=str(error)
        )

@router.post("/query")
def query_repository(request: QueryRequest):

    results = retriever.search(
        query=request.query,
        top_k=request.top_k
    )

    response = []

    for result in results:
        chunk = result["chunk"]

        response.append(
            {
                "score": result["score"],
                "file": chunk.file_path,
                "start_line": chunk.start_line,
                "end_line": chunk.end_line,
                "content": chunk.content
            }
        )
    return {
        "query": request.query,
        "results": response
    }

@router.post("/chat")
def chat_with_repository(request: QueryRequest):

    results = retriever.search(
        query=request.query,
        top_k=request.top_k
    )

    if not results:
        return {
            "answer": (
                "I couldn't find relevant code "
                "in the indexed repository."
            ),
            "sources": []
        }

    context_parts = []
    sources = []

    for result in results:

        chunk = result["chunk"]

        context_parts.append(
            f"""
FILE: {chunk.file_path}
LINES: {chunk.start_line}-{chunk.end_line}

{chunk.content}
"""
        )

        sources.append(
            {
                "file": chunk.file_path,
                "start_line": chunk.start_line,
                "end_line": chunk.end_line,
                "score": result["score"]
            }
        )

    context = "\n\n".join(context_parts)

    answer = llm.generate_answer(
        question=request.query,
        context=context
    )

    return {
        "answer": answer,
        "sources": sources
    }