def sino_to_bollo(s: str) -> bool:
    if s.lower() == "si":
        return True
    elif s.lower() == "no":
        return False
    raise ValueError(f"cannot deterine truth value of string {s}!")
