import re


def clean_text(text: str) -> str:
    # remove strange unicode characters
    text = text.encode("utf-8", "ignore").decode("utf-8")

    # remove excessive whitespace
    text = re.sub(r"\s+", " ", text)

    # remove weird bullet characters
    text = text.replace("•", " ")

    # strip leading/trailing spaces
    text = text.strip()

    return text