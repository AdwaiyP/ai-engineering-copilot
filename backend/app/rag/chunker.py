from dataclasses import dataclass

@dataclass
class CodeChunk:
    file_path: str
    content: str
    start_line: int
    end_line: int

def chunk_code(
        content: str,
        file_path: str,
        chunk_size: int = 80,
        overlap: int = 20
) -> list[CodeChunk]:
    
    lines = content.splitlines()

    chunks = []

    start = 0

    while start < len(lines):

        end = min(start + chunk_size, len(lines))

        chunk_content = "\n".join(lines[start:end])

        chunks.append(
            CodeChunk(
                file_path=file_path,
                content=chunk_content,
                start_line=start + 1,
                end_line=end
            )
        )

        if end == len(lines):
            break
        start = end - overlap

    return chunks