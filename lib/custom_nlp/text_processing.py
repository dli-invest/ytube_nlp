import spacy
from spacy.matcher import Matcher
from spacy.lang.en import English
from lib.custom_nlp.patterns import cse_pattern, tsx_pattern, stock_phrases
import re
from spacytextblob.spacytextblob import SpacyTextBlob
try:
    from lib.custom_nlp.curr_tickers import stocks as stock_names
except ImportError as e:
    print(e)
    stock_names = []


# All NLP logic is encompassed in this object
class NLPLogic:
    def __init__(self):
        nlp = spacy.load('en_core_web_sm')
        nlp.add_pipe("spacytextblob")
        self.nlp = nlp

    def get_text_matches(self, text):
        matches = []
        matched_strings = []

        temp_matched_strings, temp_matches = self.phrases_of_interest(text)
        matched_strings = [*matched_strings, *temp_matched_strings]
        matches = [*matches, *temp_matches]

        temp_matched_strings, temp_matches = self.stocks_of_interest(text)
        matched_strings = [*matched_strings, *temp_matched_strings]
        matches = [*matches, *temp_matches]

        temp_matched_strings, temp_matches = self.stocks_from_exchange(text)
        matched_strings = [*matched_strings, *temp_matched_strings]
        matches = [*matches, *temp_matches]

        return matched_strings, matches

    def phrases_of_interest(self, text):
        matcher = Matcher(self.nlp.vocab, validate=True)
        matcher.add(
            "Phrases",
            stock_phrases
        )
        doc = self.nlp(text)
        matches = matcher(doc)
        # Iterate and add stocks to the matcher, one by one
        matched_strings = []
        for match_id, start, end in matches:
            string_id = self.nlp.vocab.strings[match_id]  # Get string representation
            span = doc[start:end]  # The matched span
            matched_strings.append(span.text)
        return matched_strings, matches

    def stocks_of_interest(self, text):
        """
        Description: Checks a given sentence for stocks of interest

        Returns:
          matched_strings: String matches from text
          matches: spacy matches
        """
        stock_patterns = [{"TEXT": {"REGEX": f"{stock}"}} for stock in stock_names if len(stock) > 1]
        matcher = Matcher(self.nlp.vocab)
        matcher.add("stocks_patterns", [stock_patterns])
        doc = self.nlp(text)

        matches = matcher(doc)
        # Iterate and add stocks to the matcher, one by one
        matched_strings = []
        # for match_id, start, end in matches:
        #     string_id = self.nlp.vocab.strings[match_id]  # Get string representation
        #     span = doc[start:end]  # The matched span
        #     print(match_id, string_id, start, end, span.text)
        
        # https://spacy.io/usage/rule-based-matching
        for stock in stock_names:
            for match in re.finditer(stock, doc.text, flags=re.IGNORECASE):
                start, end = match.span()
                span = doc.char_span(start, end)
                # This is a Span object or None if match doesn't map to valid token sequence
                if span is not None:
                    matched_strings.append(span.text)
        # for match_id, start, end in matches:
        #     string_id = self.nlp.vocab.strings[match_id]  # Get string representation
        #     span = doc[start:end]  # The matched span
        #     matched_strings.append(span.text)
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
        matcher.add("CSE_TICKERS", [cse_pattern])
        matcher.add("TSX_TICKERS", [tsx_pattern])
        matches = matcher(doc)

        matched_strings = []
        for match_id, start, end in matches:
            string_id = self.nlp.vocab.strings[match_id]  # Get string representation
            span = doc[start:end]  # The matched span
            matched_strings.append(span.text)
            print(matches)
        print(matched_strings)
        return matched_strings, matches

    def __exit__(self, exc_type, exc_value, traceback):
        self.nlp = None


if __name__ == "__main__":
    nlpLogic = NLPLogic()
