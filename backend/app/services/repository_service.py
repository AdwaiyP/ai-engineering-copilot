from pathlib import Path

from app.rag.chunker import chunk_code

SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".cpp",
    ".c",
    ".h",
    ".hpp",
    ".go",
    ".rs",
    ".html",
    ".css",
    ".json",
    ".md",
}

def read_repository(repository_path: str):

    repository = Path(repository_path)

    if not repository.exists():
        raise FileNotFoundError(
            f"Repository not found: {repository_path}"
        )
    
    chunks = []

    for file_path in repository.rglob("*"):

        if not file_path.is_file():
            continue
        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        if any(
            part in {
                ".git",
                "node_modules",
                "venv",
                "__pycache__",
                ".next",
                "dist",
                "build",
            }
            for part in file_path.parts
        ):
            continue
        try:

            content = file_path.read_text(
                encoding="utf-8"
            )
        except (UnicodeDecodeError, OSError):
            continue
        relative_path = str(
            file_path.relative_to(repository)
        )
        file_chunks = chunk_code(
            content=content,
            file_path=relative_path
        )
        chunks.extend(file_chunks)
    return chunks 