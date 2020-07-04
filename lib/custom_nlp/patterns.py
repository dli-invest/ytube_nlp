# Move patterns to file for reusablity
cse_pattern = [
  {'TEXT': 'CSE'},
  {"IS_PUNCT": True, 'OP': '?'},
  {'ENT_TYPE': 'ORG'}
]

tsx_pattern = [
  {'TEXT': 'TSX'},
  {"TEXT": "-",'OP': '?'},
  {"TEXT": "V",'OP': '?'},
  {"IS_PUNCT": True, 'OP': '?'},
  {'ENT_TYPE': 'ORG'}
]