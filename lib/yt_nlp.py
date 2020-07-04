import spacy
from spacy.matcher import Matcher
from spacy.lang.en import English
import json
from jinja2 import Template
from youtube_transcript_api import YouTubeTranscriptApi

from lib.custom_nlp.text_processing import NLPLogic
# Youtube Natural Language Processing
class YTNLP(NLPLogic):
    # Initializer / Instance Attributes
    def __init__(self, video_id, html_template='ytube.jinja2'):
        self.html_template = html_template
        self.video_id = video_id
        self.transcript_list = []
        self.transcript = None
        # Dict line object for the transcript object returned 
        # from youtube with extra data from nlp
        self.lines = []
        NLPLogic.__init__(self)

    def fetch_transcript(self, languages=['en-US', 'en']):
        transcript_list = YouTubeTranscriptApi.list_transcripts(self.video_id)
        self.transcript_list = transcript_list
        transcript = transcript_list.find_transcript(languages)
        full_transcript = transcript.fetch()
        self.transcript = full_transcript
        with open(f'{self.video_id}.json', 'w') as raw_transcript:
            raw_transcript.write(json.dumps(full_transcript))
        return full_transcript
    

    # Extract entities of interest (person)
    # Extract numerical figures
    # Ignore if music text or other useless stuff
    # Match certain stock names
    # Match key financial phrases Q1, Financial Report
    # Bull Market, Bear Market
    def find_matches(self):
        if self.transcript is None:
            print("Matches are not found yet")
            return

        matcher = Matcher(self.nlp.vocab)
        matched_lines = []
        for text_obj in self.transcript:
            text = text_obj["text"]
            doc = self.nlp(text)
            detailed_obj = text_obj
            detailed_obj["ents"] = list(doc.ents)
            detailed_obj["sentiment"] = doc.sentiment
            # Iterate over the tokens in the doc
            for token in doc:
                # Check if the token resembles a number
                if token.like_num:
                    # G et the next token in the document
                    # Make sure the last token isn't reached
                    if token.i + 1  != len(doc):
                        next_token = doc[token.i + 1]
                        # Check if the next token's text equals "%"
                        if next_token.text == "%":
                            print(token)
                            print("Percentage found:", token.text)
                    
                    matched_lines.append(detailed_obj)
                    break
        self.lines = matched_lines
        print(matched_lines)

    def make_report(self, report_path='index.html'):
        """
            Makes a jinja2 report
        """
        with open(self.html_template) as file_:
            template = Template(file_.read())

        options=dict(Version="1.0.0", LINES=self.lines, VIDEO_ID=self.video_id)
        renderer_template = template.render(**options)
        with open(report_path, "w", errors='ignore') as f:
            f.write(renderer_template)
        pass



def main(args):
    video_id = args.video
    html_template = args.template
    youtube_nlp = YTNLP(video_id, html_template=html_template)
    youtube_nlp.fetch_transcript()
    youtube_nlp.find_matches()
    youtube_nlp.make_report()
    print('REPORT MADE AT index.html')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-v",
                        "--video",
                        help="Youtube Video Id",
                        default="VuavFEzN6oA")
    parser.add_argument("-t", 
                        "--template", 
                        help="Template file", 
                        default="lib/ytube.jinja2") 
    args = parser.parse_args()
    main(args)
