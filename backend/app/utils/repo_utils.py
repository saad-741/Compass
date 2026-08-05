import re
from urllib.parse import urlparse

GITHUB_URL_PATTERN = re.compile(
    r"^https?://(www\.)?github\.com/(?P<owner>[\w.-]+)/(?P<repo>[\w.-]+?)(?:\.git)?$"
)

def validate_and_parse_github_url(url: str) -> tuple[str, str]:
    """
    Validates a GitHub repository URL and extracts (owner, repo).
    Raises ValueError if the URL format is invalid.
    """
    clean_url = url.strip().rstrip("/")
    match = GITHUB_URL_PATTERN.match(clean_url)
    
    if not match:
        raise ValueError("Invalid GitHub URL format. Expected: https://github.com/owner/repo")
    
    owner = match.group("owner")
    repo = match.group("repo")
    return owner, repo