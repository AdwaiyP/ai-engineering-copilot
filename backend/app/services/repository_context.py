import json
from pathlib import Path


STATE_FILE = Path("data/active_repository.json")


class RepositoryContext:

    def __init__(self):
        self.repository_path: Path | None = None
        self.repository_name: str | None = None

        self._load_state()

    def set_repository(
        self,
        repository_path: str,
        repository_name: str
    ):
        path = Path(repository_path).resolve()

        if not path.exists():
            raise RuntimeError(
                "Repository path does not exist."
            )

        self.repository_path = path
        self.repository_name = repository_name

        self._save_state()

    def get_repository_path(self) -> Path:

        if self.repository_path is None:
            raise RuntimeError(
                "No repository has been indexed."
            )

        if not self.repository_path.exists():
            raise RuntimeError(
                "The indexed repository no longer exists."
            )

        return self.repository_path

    def get_repository_name(self) -> str | None:
        return self.repository_name

    def _save_state(self):

        STATE_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        state = {
            "repository_path": str(
                self.repository_path
            ),
            "repository_name": self.repository_name,
        }

        STATE_FILE.write_text(
            json.dumps(
                state,
                indent=2
            ),
            encoding="utf-8"
        )

    def _load_state(self):

        if not STATE_FILE.exists():
            return

        try:
            state = json.loads(
                STATE_FILE.read_text(
                    encoding="utf-8"
                )
            )

            repository_path = Path(
                state["repository_path"]
            ).resolve()

            if not repository_path.exists():
                return

            self.repository_path = repository_path
            self.repository_name = state.get(
                "repository_name"
            )

        except (
            json.JSONDecodeError,
            KeyError,
            OSError,
        ):
            self.repository_path = None
            self.repository_name = None


repository_context = RepositoryContext()