import shutil
import uuid
from pathlib import Path
from urllib.parse import urlparse

from git import Repo, GitCommandError


REPOSITORIES_DIR = Path("data/repositories")


def clone_github_repository(
    github_url: str
) -> tuple[str, str]:

    github_url = github_url.strip()

    # Validate URL
    parsed_url = urlparse(github_url)

    if parsed_url.scheme not in {"http", "https"}:
        raise ValueError(
            "Repository URL must use HTTP or HTTPS."
        )

    if parsed_url.hostname not in {
        "github.com",
        "www.github.com",
    }:
        raise ValueError(
            "Only GitHub repository URLs are supported."
        )

    # Extract owner and repository name
    path_parts = [
        part
        for part in parsed_url.path.split("/")
        if part
    ]

    if len(path_parts) != 2:
        raise ValueError(
            "Enter a valid GitHub repository URL."
        )

    owner = path_parts[0]
    repository_name = path_parts[1]

    if repository_name.endswith(".git"):
        repository_name = repository_name[:-4]

    if not owner or not repository_name:
        raise ValueError(
            "Invalid GitHub repository URL."
        )

    # Create repository storage directory
    REPOSITORIES_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Remove previous clones of this repository
    for existing_repository in REPOSITORIES_DIR.glob(
        f"{repository_name}-*"
    ):
        if existing_repository.is_dir():
            shutil.rmtree(
                existing_repository,
                ignore_errors=True
            )

    # Generate unique destination
    unique_id = uuid.uuid4().hex[:8]

    destination = (
        REPOSITORIES_DIR
        / f"{repository_name}-{unique_id}"
    )

    # Clone repository
    try:
        Repo.clone_from(
            github_url,
            destination,
            depth=1,
        )

    except GitCommandError as error:

        if destination.exists():
            shutil.rmtree(
                destination,
                ignore_errors=True
            )

        # Keep detailed error temporarily
        # while we finish testing Docker.
        raise RuntimeError(
            f"Git clone failed: {error}"
        ) from error

    # Verify clone
    if not destination.exists():
        raise RuntimeError(
            "Repository clone did not complete successfully."
        )

    return (
        str(destination.resolve()),
        repository_name,
    )