import unittest
from lib.youtube.yt_nlp import YTNLP
class TestNLPLogic(unittest.TestCase):
    def setUp(self):
        self.YTNLP = YTNLP(html_template='lib/ytube.jinja2')

    def test_video_data_bad(self):
        video_data = [
          {'videoID': 'aBv_b6A5zl0', 'channelId': 'UC6zHYEnBuH4DYxbPLsbIaVw', 'description': 'KORE Mining (CVE: KORE) CEO Scott Trebilcock joined Steve Darling from Proactive to discuss the company, that is exploring 4 properties including their ...', 'title': 'KORE Mining is cashed up and ready for exploration on 4 unique projects'}
        ]
        video_1 = video_data[0].get('videoID')
        failed_attempt = self.YTNLP.gen_report_for_id(video_1, 'index.html')
        assert failed_attempt == False

    def test_real_data(self):
        video_data = [
            {
              'videoID': 'xLR25jvH22E', 'channelId': 'UCvJJ_dzjViJCoLf5uKUTwoA',
              'description': 'Of all the industries the coronavirus pandemic has affected, the airline industry is among those that have been hit the hardest. According to the International Air ...',
              'title': 'What Does The Future Of Air Travel Look Like?'
            }
        ]
        video_1 = video_data[0].get('videoID')
        success_attempt = self.YTNLP.gen_report_for_id(video_1, 'test-index.html')
        print(success_attempt)

if __name__ == '__main__':
    unittest.main()
