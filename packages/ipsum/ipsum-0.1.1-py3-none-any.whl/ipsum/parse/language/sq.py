from ipsum.parse.parser import Parser

sq_parser = Parser(
    "ABCÇDEËFGGHIJKLMNOPQRSSTUVXYZabcçdeëfgghijklmnopqrsstuvxyz’",
    internal_punctuation=[",", ":", ";", "-", "–", "—"],
    endings=["?!", "!?", ".", "!", "?", "…"],
    matched_punctuation=[("(", ")"), ("“", "”")],
    stop_words=(
        ["të", "e", "në", "i", "dhe", "për", "me", "që", "një", "ka", "se"]
        + ["nga", "është", "më", "nuk", "do", "së", "edhe", "u", "janë", "si"]
        + ["por", "shumë", "kanë", "po", "këtë", "mund", "te", "ai", "ne", "kujt"]
        + ["tij", "t", "duhet", "kjo", "ta", "ishte", "tyre", "tha", "parë"]
        + ["kur", "ku", "vetëm", "prej", "sa", "larg", "gjatë", "kush", "pse"]
    ),
)
