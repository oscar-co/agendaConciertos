MAX_Q = 80

def clean_q(s: str | None, max_len: int = MAX_Q) -> str | None:
    if not s:
        return None
    s = s.strip()
    if len(s) > max_len:
        s = s[:max_len]
    return s