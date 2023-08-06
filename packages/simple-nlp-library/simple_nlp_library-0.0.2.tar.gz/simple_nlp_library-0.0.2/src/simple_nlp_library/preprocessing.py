import re


def remove_multiple_spaces(text: str) -> str:
    return ' '.join(text.split())


def leave_only_uncased_letters(text: str) -> str:
    return re.sub('[^a-z ]+', '', text.lower())
