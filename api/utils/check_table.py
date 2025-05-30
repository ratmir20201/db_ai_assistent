import re


def is_backup_table(table_name: str) -> bool:
    """Возвращает True, если таблица — бэкапная или временная."""
    patterns = [
        r".*_\d{6,8}$",
        r".*_BCKP$",
        r".*_BACKUP$",
        r".*_TMP$",
        r".*_TEMP$",
        r".*_ARCH$",
        r".*_OLD$",
    ]
    return any(re.match(pattern, table_name.upper()) for pattern in patterns)
