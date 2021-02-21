import unittest
from lib.custom_nlp.text_processing import NLPLogic


class TestNLPLogic(unittest.TestCase):
    def setUp(self):
        self.nlpLogic = NLPLogic()


    # note organization logic has changed
    def test_stock_exchange_cse(self):
        cse = """ The North American Marijuana 
          Index fell to 94% today. Tilt Holdings (CSE: TILT) (OTCQB: TLLTF) 
          fell more than 7% today. While the Cambridge
        """
        matched_strings, _ = self.nlpLogic.stocks_from_exchange(cse)
        assert matched_strings[0] == "CSE"

    def test_stock_exchange_cve(self):
        cse = """ The North American Marijuana 
          Index fell to 94% today. Tilt Holdings (CVE: TILT) (OTCQB: TLLTF) 
          fell more than 7% today. While the Cambridge
        """
        matched_strings, _ = self.nlpLogic.stocks_from_exchange(cse)
        assert matched_strings[0] == "CVE"

    def test_stock_exchange_tsx(self):
        tsx = """ Integra Resources Corp. (TSX-V:ITR)
          (OTCQX:IRRZF) CEO George Salamis tells Proactive
          the Vancouver-based development-stage mining company is
        """
        matched_strings, _ = self.nlpLogic.stocks_from_exchange(tsx)
        assert matched_strings[0] == "TSX-V:ITR"

    def test_stock_blackberry(self):
        bb = """ BlackBerry is a pass, says RBC
          Investors should still be in a wait-and-see
          mode when it comes to Canadian tech company
          BlackBerry (TSX:BB)
        """
        matched_strings, _ = self.nlpLogic.stocks_of_interest(bb)
        assert matched_strings[0] == "BB"

    def test_stock_hive(self):
        hive = """ Vancouver, Canada - June 11, 2020 
          (Investorideas.com Newswire) HIVE Blockchain
          Technologies Ltd. (TSX.V:HIVE) (OTCQX:HVBTF)
          (FSE:HBF) (the "Company" or "HIVE") is pleased
          to announce that it has ordered 1,090 Bitmain
          Antminer T17+ SHA 256 mining machines as it
          continues to scale up next generation mining
          power at its 30 megawatt capacity, green
          energy-powered bitcoin mining operation in Quebec acquired in April.
        """
        matched_strings, _ = self.nlpLogic.stocks_of_interest(hive)
        assert matched_strings[0] == "HIVE"


if __name__ == "__main__":
    unittest.main()