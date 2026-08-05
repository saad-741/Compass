import os
import shutil
import uuid
import stat
import git
from pathlib import Path
from app.core.config import settings

ALLOWED_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx",
    ".java", ".go", ".cpp", ".html", ".css", ".md"
}

IGNORED_DIRS = {
    ".git", "node_modules", "dist", "build", "venv", ".venv",
    "coverage", "__pycache__", ".idea", ".vscode", "site-packages", "temp"
}

IGNORED_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".webp",
    ".mp4", ".webm", ".avi", ".mov", ".mkv",
    ".zip", ".tar", ".gz", ".7z", ".pdf", ".exe", ".bin"
}

class IngestionError(Exception):
    """Custom exception for repository ingestion failures."""
    pass

class RepoIngestionService:
    @staticmethod
    def _handle_remove_readonly(func, path, exc_info):
        """Helper to clear read-only flag on Windows files before deletion."""
        os.chmod(path, stat.S_IWRITE)
        func(path)

    @classmethod
    def clone_repository(cls, repo_url: str) -> tuple[str, Path]:
        """
        Clones a public GitHub repository using shallow clone (--depth 1).
        Returns a unique repo_id and the destination local Path.
        """
        repo_id = str(uuid.uuid4())
        dest_path = Path(settings.TEMP_DIR) / repo_id

        try:
            git.Repo.clone_from(
                url=repo_url,
                to_path=dest_path,
                depth=1,
                single_branch=True
            )
            return repo_id, dest_path
        except Exception as e:
            if dest_path.exists():
                cls.cleanup_repository(dest_path)
            raise IngestionError(f"Failed to clone repository: {str(e)}")

    @staticmethod
    def validate_and_filter_repository(repo_path: Path) -> list[Path]:
        """
        Scans cloned repository, validates size/file count, and filters allowed source files.
        """
        total_size_bytes = 0
        max_size_bytes = settings.MAX_REPO_SIZE_MB * 1024 * 1024
        valid_files: list[Path] = []

        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

            for file in files:
                file_path = Path(root) / file
                
                try:
                    file_size = file_path.stat().st_size
                    total_size_bytes += file_size
                except OSError:
                    continue

                if total_size_bytes > max_size_bytes:
                    raise IngestionError(
                        f"Repository exceeds maximum size limit of {settings.MAX_REPO_SIZE_MB} MB."
                    )

                ext = file_path.suffix.lower()
                if ext in ALLOWED_EXTENSIONS and ext not in IGNORED_EXTENSIONS:
                    valid_files.append(file_path)

        if len(valid_files) > settings.MAX_FILES:
            raise IngestionError(
                f"Repository contains too many code files ({len(valid_files)} found, maximum allowed is {settings.MAX_FILES})."
            )

        if not valid_files:
            raise IngestionError("No supported code files found in the repository.")

        return valid_files

    @classmethod
    def cleanup_repository(cls, repo_path: Path) -> None:
        """
        Deletes temporary clone folder, removing read-only permissions first if needed.
        """
        if repo_path.exists() and repo_path.is_dir():
            shutil.rmtree(repo_path, onerror=cls._handle_remove_readonly)


# import os
# import shutil
# import uuid
# import stat
# import git
# from pathlib import Path
# from app.core.config import settings

# # Supported extensions (Step 5 - Allow)
# ALLOWED_EXTENSIONS = {
#     ".py", ".js", ".ts", ".jsx", ".tsx",
#     ".java", ".go", ".cpp", ".html", ".css", ".md"
# }

# # Directories and exact names to ignore (Step 5 - Ignore)
# IGNORED_DIRS = {
#     ".git", "node_modules", "dist", "build", "venv", ".venv",
#     "coverage", "__pycache__", ".idea", ".vscode", "site-packages"
# }

# # Media / Binary extensions to explicitly ignore
# IGNORED_EXTENSIONS = {
#     ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".webp",
#     ".mp4", ".webm", ".avi", ".mov", ".mkv",
#     ".zip", ".tar", ".gz", ".7z", ".pdf", ".exe", ".bin"
# }

# class IngestionError(Exception):
#     """Custom exception for repository ingestion failures."""
#     pass

# class RepoIngestionService:
#     @staticmethod
#     def clone_repository(repo_url: str) -> tuple[str, Path]:
#         """
#         Clones a public GitHub repository using shallow clone (--depth 1).
#         Returns a unique repo_id and the destination local Path.
#         """
#         repo_id = str(uuid.uuid4())
#         dest_path = Path(settings.TEMP_DIR) / repo_id

#         try:
#             git.Repo.clone_from(
#                 url=repo_url,
#                 to_path=dest_path,
#                 depth=1,
#                 single_branch=True
#             )
#             return repo_id, dest_path
#         except Exception as e:
#             # Clean up if clone failed mid-way
#             if dest_path.exists():
#                 shutil.rmtree(dest_path, ignore_errors=True)
#             raise IngestionError(f"Failed to clone repository: {str(e)}")

#     @staticmethod
#     def validate_and_filter_repository(repo_path: Path) -> list[Path]:
#         """
#         Scans cloned repository:
#         1. Checks max size limit (Step 4 - 100 MB).
#         2. Filters allowed source code files (Step 5).
#         3. Enforces max code file count (Step 4 - 500 files).
#         Returns a list of valid file Paths.
#         """
#         total_size_bytes = 0
#         max_size_bytes = settings.MAX_REPO_SIZE_MB * 1024 * 1024
#         valid_files: list[Path] = []

#         for root, dirs, files in os.walk(repo_path):
#             # Prune ignored directories in-place during traversal
#             dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

#             for file in files:
#                 file_path = Path(root) / file
                
#                 # Compute total directory size to enforce size limit
#                 try:
#                     file_size = file_path.stat().st_size
#                     total_size_bytes += file_size
#                 except OSError:
#                     continue

#                 if total_size_bytes > max_size_bytes:
#                     raise IngestionError(
#                         f"Repository exceeds maximum size limit of {settings.MAX_REPO_SIZE_MB} MB."
#                     )

#                 # Filter supported file extensions
#                 ext = file_path.suffix.lower()
#                 if ext in ALLOWED_EXTENSIONS and ext not in IGNORED_EXTENSIONS:
#                     valid_files.append(file_path)

#         if len(valid_files) > settings.MAX_FILES:
#             raise IngestionError(
#                 f"Repository contains too many code files ({len(valid_files)} found, maximum allowed is {settings.MAX_FILES})."
#             )

#         if not valid_files:
#             raise IngestionError("No supported code files found in the repository.")

#         return valid_files

#     @staticmethod
#     def cleanup_repository(repo_path: Path) -> None:
#         """
#         Deletes temporary clone folder, forcing removal of read-only files (common in .git on Windows).
#         """
#         def remove_readonly(func, path, excinfo):
#             os.chmod(path, stat.S_IWRITE)
#             func(path)

#         if repo_path.exists() and repo_path.is_dir():
#             shutil.rmtree(repo_path, onerror=remove_readonly)
 
