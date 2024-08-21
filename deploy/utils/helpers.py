import re
import json
from typing import Dict


def clean_text(text: str) -> str:
    text = re.sub(r'[\u2018\u2019\u201c\u201d]', "'", text)
    text = text.replace('\u2026', '...')
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text.strip()


def clean_json_output(output: str) -> str:
    output = output.strip()
    output = re.sub(r'^```json\s*', '', output)
    output = re.sub(r'\s*```$', '', output)
    if output.startswith('{'):
        return output
    match = re.search(r'\{.*\}', output, re.DOTALL)
    if match:
        return match.group(0)
    return output


def parse_json_safely(json_str: str) -> Dict:
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        cleaned_json = clean_json_output(json_str)
        try:
            return json.loads(cleaned_json)
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON", "raw_content": json_str}
