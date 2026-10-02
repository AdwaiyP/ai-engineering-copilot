from pathlib import Path

from app.services.repository_context import repository_context


IGNORED_DIRECTORIES = {
    ".git",
    "node_modules",
    "venv",
    ".venv",
    "__pycache__",
    "dist",
    "build",
    ".next",
}


def _repository_root() -> Path:
    return repository_context.get_repository_path()


def list_files() -> list[str]:

    root = _repository_root()

    files = []

    for path in root.rglob("*"):

        if not path.is_file():
            continue

        relative = path.relative_to(root)

        if any(
            part in IGNORED_DIRECTORIES
            for part in relative.parts
        ):
            continue

        files.append(str(relative))

    return files[:500]

def read_file(
    file_path: str,
    start_line: int = 1,
    end_line: int = 200
) -> str:

    root = _repository_root()

    requested_path = (
        root / file_path
    ).resolve()

    # Security: don't allow reading outside repository.
    try:
        requested_path.relative_to(root)
    except ValueError:
        raise ValueError(
            "File path is outside the repository."
        )

    if not requested_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    if not requested_path.is_file():
        raise ValueError(
            f"Not a file: {file_path}"
        )

    try:
        content = requested_path.read_text(
            encoding="utf-8"
        )
    except UnicodeDecodeError:
        raise ValueError(
            "File is not a readable text file."
        )

    lines = content.splitlines()

    start = max(start_line - 1, 0)
    end = min(end_line, len(lines))

    numbered_lines = []

    for line_number, line in enumerate(
        lines[start:end],
        start=start + 1
    ):
        numbered_lines.append(
            f"{line_number}: {line}"
        )

    return "\n".join(numbered_lines)

def search_code(
    query: str,
    retriever,
    top_k: int = 5
) -> list[dict]:

    results = retriever.search(
        query=query,
        top_k=top_k
    )

    formatted_results = []

    for result in results:

        chunk = result["chunk"]

        formatted_results.append(
            {
                "file": chunk.file_path,
                "start_line": chunk.start_line,
                "end_line": chunk.end_line,
                "content": chunk.content,
                "score": result["score"],
            }
        )

    return formatted_results