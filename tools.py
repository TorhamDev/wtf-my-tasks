from constants import START_HELP

def get_starter_text(user_first_name: str) -> str:
    return f"Hello dear {user_first_name}\n" + START_HELP
