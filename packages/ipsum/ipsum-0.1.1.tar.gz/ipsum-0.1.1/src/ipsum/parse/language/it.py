from ipsum.parse.parser import Parser

it_parser = Parser(
    "AÀBCDEÈÉFGHIÍÌJKLMNOÒÓPQRSTUÙÚVXYZaàbcdeèéfghiíìjklmnoòópqrstuùúvxyz’",
    internal_punctuation=[",", ":", ";", "-", "–", "—"],
    endings=["?!", "!?", ".", "!", "?", "…"],
    matched_punctuation=[("(", ")"), ("“", "”")],
    stop_words=(
        ["di", "e", "il", "la", "che", "in", "a", "per", "è", "un", "del", "non"]
        + ["con", "i", "una", "le", "ha", "della", "si", "da", "al", "sono"]
        + ["anche", "ma", "dei", "più", "nel", "alla", "gli", "o"]
        + ["dove", "quando", "come", "quale", "cosa", "chi", "perchè"]
        + ["delle", "lo", "su", "dal", "questo", "hanno", "stato", "ad", "ci"]
        + ["nella", "tra", "se", "due", "sul", "dopo", "alle", "essere", "ai"]
    ),
    additional_substitutions=[(r"(\w)'(\w)", r"\1’\2"), (r"«", r"“"), (r"»", r"”")],
)
