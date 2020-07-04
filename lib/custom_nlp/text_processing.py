
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

  def stocks_of_interest(self, text):
    """
      Description: Checks a given sentence for stocks of interest

      Returns: 
        matched_strings: String matches from text 
        matches: spacy matches
    """
    stock_patterns = [{'LOWER': stock} for stock in stock_names if len(stock) > 1]

    matcher = Matcher(self.nlp.vocab)
    for stock_pattern in stock_patterns:
      stock_name = stock_pattern.get('LOWER')
      if stock_name != None:
        matcher.add(stock_name, None, [stock_pattern])
    doc = self.nlp(text)

    matches = matcher(doc)
    # Iterate and add stocks to the matcher, one by one
    matched_strings = []
    for match_id, start, end in matches:
      string_id = self.nlp.vocab.strings[match_id]  # Get string representation
      span = doc[start:end]  # The matched span
      print(match_id, string_id, start, end, span.text)
      matched_strings.append(span.text)
    return matched_strings, matches

  def stocks_from_exchange(self, text):
    """
      Description: Checks a given sentence for tickers from exchanges

      Returns: 
        matched_strings: String matches from text 
        matches: spacy matches
    """
    matcher = Matcher(self.nlp.vocab)
    doc = self.nlp(text)
    matcher.add('TICKERS', None, cse_pattern, tsx_pattern)
    matches = matcher(doc)

    matched_strings = []
    for match_id, start, end in matches:
      string_id = self.nlp.vocab.strings[match_id]  # Get string representation
      span = doc[start:end]  # The matched span
      print(match_id, string_id, start, end, span.text)
      matched_strings.append(span.text)
    return matched_strings, matches

if __name__ == '__main__':
  nlpLogic = NLPLogic()
