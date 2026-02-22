PROFILE_PARSER_USER = """
Extract data from the following text:

TEXT:
"{raw_text}"

EXPECTED FORMAT:
{{
    "name": "string or null",
    "age": "integer or null",
    "city": "string or null",
    "bio": "string or null",
    "gender": "M/F or null"
}}
"""
