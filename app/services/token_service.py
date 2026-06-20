def generate_token_number(last_token_number: str | None):
    if not last_token_number:
        return "A001"

    current_number = int(last_token_number[1:])
    next_number = current_number + 1

    return f"A{next_number:03d}"