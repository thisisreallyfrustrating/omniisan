from schema import Schema, And

TASK = Schema(
    {
        "url": And(
            str,
            (
                lambda s: (
                    s.startswith("https://forums.spacebattles.com/threads/")
                    or s.startswith("https://forums.sufficientvelocity.com/threads/")
                )
            ),
        ),
        "g-recaptcha-response": str,
    }
)
