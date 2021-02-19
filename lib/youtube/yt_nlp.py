import spacy
from spacy.matcher import Matcher
from spacy.lang.en import English
import json
from jinja2 import Template
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
from youtube_transcript_api._errors import TranscriptsDisabled
from lib.custom_nlp.text_processing import NLPLogic
from icecream import ic
# Youtube Natural Language Processing
class YTNLP(NLPLogic):
    # Initializer / Instance Attributes
    def __init__(self, video_id=None, html_template="ytube.jinja2"):
        """
        Description: Constructor for YTNLP

        Arguments:
            video_id: youtube id, can be changed as needed
            html_template: html template should be set once
        """
        self.html_template = html_template
        self.video_id = video_id
        self.transcript = None
        # Dict line object for the transcript object returned
        # from youtube with extra data from nlp
        self.lines = []
        NLPLogic.__init__(self)

    def set_video_id(self, video_id):
        self.video_id = video_id

    def fetch_transcript(self, languages=["en-US", "en"]):
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(self.video_id)
            transcript = transcript_list.find_transcript(languages)
            full_transcript = transcript.fetch()
            self.transcript = full_transcript
            return full_transcript
        except TranscriptsDisabled as e:
            # add logger error here with video id and error type
            print(e)
            return None
        except NoTranscriptFound as e:
            print(e)
            return None
        except Exception as e:
            ic("Generic Exception")
            ic(e)
            return None

    # Extract entities of interest (person)
    # Extract numerical figures
    # Ignore if music text or other useless stuff
    # Match certain stock names
    # Match key financial phrases Q1, Financial Report
    # Bull Market, Bear Market
    def find_matches(self, yt_transcript):
        if yt_transcript is None:
            print("Matches are not found yet")
            return

        matcher = Matcher(self.nlp.vocab)
        matched_lines = []
        for text_obj in yt_transcript:
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
                    if token.i + 1 != len(doc):
                        next_token = doc[token.i + 1]
                        # Check if the next token's text equals "%"
                        if next_token.text == "%":
                            # Add % to stats
                            # print(token)
                            # print("Percentage found:", token.text)
                            TODO = False

                    matched_lines.append(detailed_obj)
                    break
        self.lines = matched_lines
        return matched_lines

    def make_report_simple(self, report_path="index.html"):
        """
        Makes a jinja2 report for the given yt_nlp
        """
        with open(self.html_template) as file_:
            template = Template(file_.read())

        options = dict(Version="1.0.0", LINES=self.lines, VIDEO_ID=self.video_id)
        renderer_template = template.render(**options)
        with open(report_path, "w", errors="ignore") as f:
            f.write(renderer_template)
        pass

    def make_report_complex(self, options=dict(), report_path="index.html"):
        with open(self.html_template) as file_:
            template = Template(file_.read())

        renderer_template = template.render(**options)
        with open(report_path, "w", errors="ignore") as f:
            f.write(renderer_template)

    def gen_report_for_id(self, video_id, report_path="index.html", video_data=None):
        """
        Description: Attempts to make a report for a given youtube video

        Returns: A boolean indication if the operation succeeded
        """
        assert video_id is not None
        self.set_video_id(video_id)
        transcript = self.fetch_transcript()
        if transcript is not None:
            lines = self.find_matches(transcript)
        else:
            print("Not producing report, no data")
            return False
        if video_data is None:
            self.make_report_simple(report_path)
        else:
            options = dict(
                Version="1.0.0", LINES=lines, VIDEO_ID=video_id, VIDEO_DATA=video_data
            )
            self.make_report_complex(options, report_path=report_path)
        return True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.nlp = None
        pass


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--video", help="Youtube Video Id", default="VuavFEzN6oA")
    parser.add_argument(
        "-t", "--template", help="Template file", default="lib/ytube.jinja2"
    )
    args = parser.parse_args()
    video_id = args.video
    html_template = args.template
    youtube_nlp = YTNLP(video_id, html_template=html_template)
    transcript = youtube_nlp.fetch_transcript()
    youtube_nlp.find_matches(transcript)
    youtube_nlp.make_report_simple()
