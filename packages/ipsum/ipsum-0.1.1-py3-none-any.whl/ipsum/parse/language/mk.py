from ipsum.parse.parser import Parser

mk_parser = Parser(
    "АБВГДЃЕЖЗЅИЈКЛЉМНЊОПРСТЌУФХЦЧШЏабвгдѓежзѕијклљмнњопрстќуфхцчшџѐѝ’",
    internal_punctuation=[",", ":", ";", "-", "–", "—"],
    endings=["?!", "!?", ".", "!", "?", "…"],
    matched_punctuation=[("(", ")"), ("„", "”")],
    stop_words=(
        ["и", "на", "се", "да", "во", "од", "не", "го", "со"]
        + ["за", "е", "ќе", "ги", "а", "му", "по", "но"]
        + ["јас", "ти", "тој", "таа", "тоа", "си", "ми"]
        + ["кога", "кој", "како", "каде", "што", "кои", "кого", "колку"]
        + ["но", "до", "ме", "ни", "сите", "него", "така", "еден", "кон"]
        + ["или", "им", "тие", "нѐ", "сѐ", "ѝ"]
    ),
    additional_substitutions=[(r"'", r"’")],
)
