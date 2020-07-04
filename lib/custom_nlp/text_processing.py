
import spacy
from spacy.matcher import Matcher
from spacy.lang.en import English
from lib.custom_nlp.patterns import cse_pattern, tsx_pattern
try:
    from lib.custom_nlp.curr_tickers import stocks as stock_names
except ImportError as e:
    print(e)
    stock_names = []


# All NLP logic is encompassed in this object
class NLPLogic:
  def __init__(self):
    self.nlp = spacy.load("en_core_web_sm")

  def has_stock_of_interest(self, text):
    stock_patterns = [{'LOWER': stock} for stock in stock_names if len(stock) > 1]
    print(text)
    matcher = Matcher(self.nlp.vocab)
    for stock_pattern in stock_patterns:
      
    doc = self.nlp(text)
    # Iterate and add stocks to the matcher, one by one

  def has_stock_from_exchange(self, text):
    """
      Description: Checks a given sentence for stocks of interest
    """
    matcher = Matcher(self.nlp.vocab)
    doc = self.nlp(text)
    matcher.add('TICKERS', None, cse_pattern, tsx_pattern)
    matches = matcher(doc)
    for match_id, start, end in matches:
        string_id = self.nlp.vocab.strings[match_id]  # Get string representation
        span = doc[start:end]  # The matched span
        print(match_id, string_id, start, end, span.text)
    if len(matches) > 0: return True
    return False