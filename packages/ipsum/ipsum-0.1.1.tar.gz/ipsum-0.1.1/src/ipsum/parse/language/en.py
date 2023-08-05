from ipsum.parse.parser import Parser

en_parser = Parser(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'",
    internal_punctuation=[",", ":", ";", "-", "–", "—"],
    endings=["?!", "!?", ".", "!", "?", "…"],
    matched_punctuation=[("(", ")"), ('"', '"')],
    stop_words=(
        ["the", "a", "an", "and", "of", "to", "in"]
        + ["i", "you", "he", "she", "it", "we", "they"]
        + ["me", "him", "her", "us", "them"]
        + ["my", "your", "his", "hers", "its", "our", "their"]
        + ["as", "at", "on", "be", "is", "was", "by", "so"]
        + ["who", "why", "what", "where", "when", "which", "whose", "how", "did"]
        + ["that", "had", "with", "for", "not", "but", "have", "this", "from"]
        + ["were", "if", "no", "one", "or"]
    ),
    additional_substitutions=[(r"(\w)’(\w)", r"\1'\2"), (r"[“|”]", r'"')],
)
