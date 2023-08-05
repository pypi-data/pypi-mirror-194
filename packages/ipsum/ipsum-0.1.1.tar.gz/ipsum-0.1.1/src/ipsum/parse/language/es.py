from ipsum.parse.parser import Parser

es_parser = Parser(
    "AÁBCDEÉFGHIÍJKLMNÑOÓPQRSTUÚVWXYZaábcdeéfghiíjklmnñoópqrstuúvwxyz'",
    internal_punctuation=[",", ":", ";", "-", "–", "—"],
    endings=["?!", "!?", ".", "!", "?", "…"],
    starting_punctuation=["¿", "¡"],
    matched_punctuation=[("(", ")"), ("“", "”")],
    stop_words=(
        ["de", "la", "el", "que", "en", "y", "a", "los", "se", "del", "un", "por"]
        + ["quién", "quiénes", "qué", "dónde", "cuándo", "cuál", "cómo"]
        + ["las", "con", "para", "una", "no", "es", "su", "al", "lo", "más"]
        + ["como", "este", "ha", "sus", "pero", "fue", "esta", "también", "o"]
        + ["le", "ya", "está", "si", "sobre", "sin", "son"]
        + ["dos", "han", "ser", "hay", "cuando", "hasta", "tiene"]
    ),
    additional_substitutions=[(r"[«|‘]", r"“"), (r"[»|’]", r"”")],
)
