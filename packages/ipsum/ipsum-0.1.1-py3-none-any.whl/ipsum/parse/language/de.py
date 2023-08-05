from ipsum.parse.parser import Parser

de_parser = Parser(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÜÖẞabcdefghijklmnopqrstuvwxyzäüöß'",
    internal_punctuation=[",", ":", ";", "-", "–", "—"],
    endings=["?!", "!?", ".", "!", "?", "…"],
    matched_punctuation=[("(", ")"), ('"', '"')],
    stop_words=(
        ["und", "die", "der", "sie", "er", "in", "zu", "ich", "den", "das"]
        + ["wo", "was", "wer", "wie", "wann", "warum", "wohin", "woher"]
        + ["sich", "nicht", "es", "mit", "ein", "dem", "auf", "von", "so", "war"]
        + ["daß", "als", "ist", "aber", "an", "eine", "des", "auch", "ihr", "man"]
        + ["ihm", "mir", "hatte", "du", "im", "noch", "wenn", "aus", "nach"]
        + ["ihn", "mich", "sein", "um", "nur", "einen", "da", "wir", "für"]
    ),
    additional_substitutions=[(r"--", r"—"), (r"[»|«]", r'"')],
)
