from ipsum.parse.parser import Parser

fr_parser = Parser(
    "AÀÂÆBCÇDEÉÈÊËFGHIÎÏJKLMNOÔÖŒPQRSTUÙÛÜVWXYŸZaàâæbcçdeéèêëfghiîïjklmnoôöœpqrstuùûüvwxyÿz’",
    internal_punctuation=[",", ":", ";", "-", "–", "—"],
    endings=["?!", "!?", ".", "!", "?", "…"],
    matched_punctuation=[("(", ")"), ("«", "»")],
    stop_words=(
        ["de", "la", "le", "à", "les", "et", "des", "en", "a", "du", "un", "pour"]
        + ["qui", "que", "quel", "quand", "pourquoi", "quoi", "quells", "quelle"]
        + ["ses", "une", "dans", "est", "au", "l", "il", "sur", "quelles"]
        + ["par", "ce", "pas", "d", "plus", "ont", "été", "son", "se", "avec"]
        + ["ne", "sont", "cette", "mais", "aux", "nous", "sa", "on", "deux"]
        + ["fait", "c’est", "je", "leur", "elle", "après", "ces", "tout", "ou"]
    ),
    additional_substitutions=[
        (r"(\w)'(\w)", r"\1’\2"),
        (r"“", r"«"),
        (r"”", r"»"),
        (r"«\s+", r"«"),
        (r"\s+»", r"»"),
    ],
)
