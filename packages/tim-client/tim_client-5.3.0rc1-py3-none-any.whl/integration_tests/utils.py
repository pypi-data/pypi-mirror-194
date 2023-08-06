from datetime import datetime
from typing import Optional


def create_random_string_with_timestamp(prefix: Optional[str] = None, postfix: Optional[str] = None) -> str:
    return f'{prefix or ""}_{datetime.now().strftime("%Y%m%d-%H%M%S")}_{postfix or ""}'
