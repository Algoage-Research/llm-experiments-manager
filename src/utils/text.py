import json
import re


def extract_json_from_string(s) -> dict | None:
    json_match = re.search(r'\{.*\}', s, re.DOTALL)
    if json_match is None:
        return None
    else:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            return None
