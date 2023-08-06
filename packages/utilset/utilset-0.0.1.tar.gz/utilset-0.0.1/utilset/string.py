def concat(*args: str) -> str:
    ret = ""
    for i in args:
        ret = f"{ret}{i}"
    return ret
