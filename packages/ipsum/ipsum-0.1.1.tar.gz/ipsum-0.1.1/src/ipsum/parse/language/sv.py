from ipsum.parse.parser import Parser

sv_parser = Parser(
    "AÄÅÁ̈ÀÆBCDEÉÈËFGHIÍJKLMNOÖØPQRSTUÜVWXYZaäåá̈àæbcdeéèëfghiíjklmnoöøpqrstuüvwxyz'",
    internal_punctuation=[",", ":", ";", "-", "–", "—"],
    endings=["?!", "!?", ".", "!", "?", "…"],
    matched_punctuation=[("(", ")"), ('"', '"')],
    stop_words=(
        ["i", "och", "att", "på", "det", "en", "som", "är", "för", "med", "har"]
        + ["vad", "vilken", "var", "när", "vem", "vems", "varför", "vilka", "hur"]
        + ["till", "av", "den", "om", "de", "inte", "ett", "men", "vi", "han"]
        + ["du", "jag", "från", "man", "sig", "så", "kan", "ska", "nu"]
        + ["under", "ut", "efter", "säger", "vill", "år", "kommer", "hon"]
        + ["mot", "här", "där", "vid", "sin", "också", "ha", "vara", "in", "eller"]
    ),
    additional_substitutions=[(r"[“|”]", r'"')],
)
