# Move patterns to file for reusablity
cse_pattern = [
    {"TEXT": {"REGEX": "(?i)CSE|CVE"}},
    {"IS_PUNCT": True, "OP": "?"},
    {"ENT_TYPE": "ORG"},
]

tsx_pattern = [
    {"TEXT": {"REGEX": "TSX|TSXV"}},
    {"TEXT": "-", "OP": "?"},
    {"TEXT": "V", "OP": "?"},
    {"IS_PUNCT": True, "OP": "?"},
    {"ENT_TYPE": "ORG"},
]
