import git
from semver import VersionInfo

from release.utils import is_valid_semver

INIT_VERSION = VersionInfo(0)
MAIN_BRANCH_NAMES = {"main", "master"}


def get_latest_version(repo: git.Repo) -> VersionInfo:
    valid_tags = filter(is_valid_semver, [tag.name for tag in repo.tags])
    ordered_semver_tags = sorted(valid_tags, key=VersionInfo.parse)
    if not ordered_semver_tags:
        return None
    return VersionInfo.parse(ordered_semver_tags.pop())


def get_next_version(repo: git.Repo, part: str) -> VersionInfo:
    latest_version = get_latest_version(repo)
    if not latest_version:
        return INIT_VERSION
    return latest_version.next_version(part=part)
