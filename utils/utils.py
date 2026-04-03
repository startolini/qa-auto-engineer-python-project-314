import platform


def is_valid_email(email: str) -> bool:
    """
    Проверяет базовую валидность email:
    - есть '@'
    - есть '.' после '@'
    """
    if "@" not in email:
        return False
    local, domain = email.split("@", 1)
    if "." not in domain:
        return False
    if not local or not domain:
        return False
    return True


def get_os() -> str:
    """
    Определяет текущую операционную систему.

    Возвращает:
        'windows', 'mac', 'linux', или 'unknown'
    """
    os_name = platform.system().lower()
    if "windows" in os_name:
        return "windows"
    elif "darwin" in os_name:  # macOS
        return "mac"
    elif "linux" in os_name:
        return "linux"
    else:
        return "unknown"
