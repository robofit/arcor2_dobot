import pkgutil


def version() -> str:
    res = pkgutil.get_data(__name__, 'VERSION')
    if not res:
        return "unknown"
    return res.decode().strip()
