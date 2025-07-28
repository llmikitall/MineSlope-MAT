import re


async def TextVerification(text: str):
    text = re.sub(r"[\"\';\\\x00]", "", text)
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;"))
