from ipsum.parse.parser import Parser

nl_parser = Parser(
    "AÁÂÀÄBCÇDEËÉÈÊFGHIJKLMNOÓÖPQRSTUÜÚVWXYZaáâàäbcçdeëéèêfghijklmnoóöpqrstuüúvwxyz’",
    internal_punctuation=[",", ":", ";", "-", "–", "—"],
    endings=["?!", "!?", ".", "!", "?", "…"],
    matched_punctuation=[("(", ")"), ("“", "”")],
    stop_words=(
        ["de", "het", "een", "van", "en", "in", "dat", "is", "op", "te", "niet"]
        + ["wat", "wie", "waarom", "wanneer", "hoe", "waar", "welk", "welke"]
        + ["zijn", "met", "die", "voor", "je", "er", "maar", "ook", "ik", "om"]
        + ["als", "aan", "dan", "ze", "nog", "bij", "heeft", "hij", "of", "we"]
        + ["naar", "wel", "door", "al", "uit", "dit", "meer", "over"]
        + ["zo", "was", "geen", "nu", "kan", "deze"]
    ),
    additional_substitutions=[(r"(\w)'(\w)", r"\1’\2")],
)
