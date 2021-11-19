# Move patterns to file for reusablity
cse_pattern = [
    {"TEXT": {"REGEX": "(?i)CSE|CVE"}},
    {"IS_PUNCT": True, "OP": "?"}
]

tsx_pattern = [
    {"TEXT": {"REGEX": "TSX|TSXV"}},
    {"TEXT": "-", "OP": "?"},
    {"TEXT": "V", "OP": "?"},
    {"IS_PUNCT": True, "OP": "?"},
    {"ENT_TYPE": "ORG"},
]


stock_phrases = [
   [{"LOWER": "hello"}, {"LOWER": "world"}],
   [{"ORTH": "Google"}, {"ORTH": "Maps"}]
]
stock_phrases = [[{"LOWER": "trutrace"}],
            [{"LOWER": "nextech"}],
            [{"LOWER": "imaginear"}],
            [{"LOWER": "blockchain"}],
            [{"LOWER": "cnbc"}, {"LOWER": "after"}, {"LOWER": "hours"}],
            [{"LOWER": "coronavirus"}],
            [{"LOWER": "bee"}, {"LOWER": "vector"}],
            [{"LOWER": "gamestop"}],
            [{"LOWER": "taxes"}]
            ]