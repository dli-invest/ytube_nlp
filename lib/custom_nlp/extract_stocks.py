# Extracts stocks like

# The North American Marijuana Index fell to 94% today. Tilt Holdings (CSE: TILT) (OTCQB: TLLTF) fell more than 7% today. While the Cambridge
# Integra Resources Corp. (TSX-V:ITR) (OTCQX:IRRZF) CEO George Salamis tells Proactive the Vancouver-based development-stage mining company is


import spacy
from spacy.matcher import Matcher
from spacy.lang.en import English
from lib.nlp.patterns import cse_pattern, tsx_pattern
try:
    from lib.nlp.curr_tickers import stocks as stock_names
except ImportError as e:
    print(e)
    stock_names = []

# Make class so I don't have to load NLP twice
# Check if any stocks from my dash list are included
def has_stock_of_interest(text):
    stock_patterns = [{'LOWER': stock} for stock in stock_names if len(stock) > 1]
    print(text)

def has_stock_from_exchange(text):
    """
      Description: Checks a given sentence for stocks of interest
    """
    nlp = spacy.load("en_core_web_sm")
    matcher = Matcher(nlp.vocab)
    doc = nlp(text)
    matcher.add('TICKERS', None, cse_pattern, tsx_pattern)
    matches = matcher(doc)
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]  # Get string representation
        span = doc[start:end]  # The matched span
        print(match_id, string_id, start, end, span.text)
    if len(matches) > 0: return True
    return False

if __name__ == '__main__':
    has_stock_from_exchange("The North American Marijuana Index fell to 94% today. Tilt Holdings (CSE: TILT) (OTCQB: TLLTF) fell more than 7% today. While the Cambridge")
    has_stock_from_exchange("Integra Resources Corp. (TSX-V:ITR) (OTCQX:IRRZF) CEO George Salamis tells Proactive the Vancouver-based development-stage mining company is")