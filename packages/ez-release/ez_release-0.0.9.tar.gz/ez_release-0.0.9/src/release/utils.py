from semver import VersionInfo


def is_valid_semver(semver: str) -> bool:
    try:
        VersionInfo.parse(semver)
        return True
    except ValueError:
        return False
