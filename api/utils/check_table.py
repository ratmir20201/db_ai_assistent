import re


def is_backup_table(table_name: str) -> bool:
    """Возвращает True, если таблица — бэкапная, временная или содержит дату/номер в имени."""
    table_name = table_name.upper()
    patterns = [
        r".*_\d{6,8}$",
        r".*_BCKP(_\d+)?$",
        r".*_BACKUP(_\d+)?$",
        r".*_TMP(_\d+)?$",
        r".*_TEMP(_\d+)?$",
        r".*_ARCH(_\d+)?$",
        r".*_OLD(_\d+)?$",
        r".*_COPY(_\d+)?$",
    ]
    return any(re.match(pattern, table_name) for pattern in patterns)
