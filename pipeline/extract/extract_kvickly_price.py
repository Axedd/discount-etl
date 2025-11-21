import re

price_regex = re.compile(r"^\d+,\-$")

def extract_kvickly_price(raw_node):
    def walk(node):
        if isinstance(node, dict):
            text = node.get("text")
            if text and price_regex.match(text):
                return text

            for c in node.get("child_views", []):
                found = walk(c)
                if found:
                    return found

        return None

    price_str = walk(raw_node)
    if not price_str:
        return None

    return float(price_str.replace(",-", ""))