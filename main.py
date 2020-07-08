import sys 
import argparse as ap
import pathlib
import glob
import shutil
from jinja2 import Template
from datetime import date, datetime
from lib.util import get_config
from lib.youtube.get_videos import get_video_data_for_channel
from lib.youtube.yt_nlp import YTNLP
from lib.email import send_mailjet_email
from jinja2 import Template

def main(args):
    end_date = str(date.today())
    gh_pages_name = 'gh-pages'

    # TODO convert to object since this is so complicated
    # With an object I think it would be easier to parallelize
    for report_cfg_file in glob.glob("lib/cfg/*.yml"):
        report_cfg = get_config(report_cfg_file)
        report_name = report_cfg["name"]
        output_folder = f"{args.output}/{report_name}"
        pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)

        gh_report_folder = f"{args.output}/{gh_pages_name}/{report_name}/{end_date}"
        pathlib.Path(gh_report_folder).mkdir(parents=True, exist_ok=True)

        email_channel_data = []
        # Make channel videos
        for channel in report_cfg["channels"]:
            channel_id = channel.get('id')
            if channel_id is not None:
                video_data = get_video_data_for_channel(channel_id)
                for video_info in video_data:
                    video_id = video_info.get('videoID')
                    title = video_info.get('title')
                    description = video_info.get('description')

                    with YTNLP(video_id=video_id, html_template='lib/ytube.jinja2') as yt_nlp:
                        file_path = f"{output_folder}/{video_id}.html"
                        is_generated = False
                        if channel.get('no_transcript') is not True:
                            is_generated = yt_nlp.gen_report_for_id(video_id, report_path=file_path, video_data=video_data)
                        
                        # temp array of objects
                        matches_per_vid = []
                        if title is not None:
                            temp_matches, _ = yt_nlp.stocks_of_interest(title)
                            matches_per_vid = [*matches_per_vid, *temp_matches]
                            temp_matches, _ = yt_nlp.stocks_from_exchange(title)
                            matches_per_vid = [*matches_per_vid, *temp_matches]
                        if description is not None:
                            temp_matches, _ = yt_nlp.stocks_of_interest(description)
                            matches_per_vid = [*matches_per_vid, *temp_matches]
                            temp_matches, _ = yt_nlp.stocks_from_exchange(description)
                            matches_per_vid = [*matches_per_vid, *temp_matches]
                        match_object = video_info
                        match_object['phrases'] = matches_per_vid
                        if is_generated is False:
                            match_object['has_report'] = False
                        else:
                            match_object['has_report'] = True
                    if channel.get('only_on_nlp_match') is True:
                        # check for nlp matches
                        if len(match_object['phrases']) > 0:
                            email_channel_data.append(match_object)
                        else:
                            # track channels that should have video transcripts, but don't
                            hello = True
                            # print(f'no matches found for {video_id}')
                    else:
                        email_channel_data.append(match_object)
            else:
                print('Channel not found for')
                print(channel)
        # Move to function or something or rewrite to class
        try:
            options=dict(Version="1.0.0", EMAIL_DATA=email_channel_data)
            with open("lib/email.jinja2") as file_:
                template = Template(file_.read())
            email_html = template.render(**options)
            # send email    
            send_mailjet_email(report_cfg, email_html)
            with open("report/investing/email.html", "w", errors='ignore') as f:
                f.write(email_html)
        except Exception as e:
            print('FAILED TO MAKE TEMPLATE')
            print(e)
        for report_file in glob.glob(f"{output_folder}/*"):
            try:
                # Move report files
                shutil.move(report_file, gh_report_folder)
            except shutil.Error as e:
                print(e)
        # Could make into another function
    
if __name__ == "__main__":
    assert sys.version_info >= (3, 6)
    startTime = datetime.now()
    parser = ap.ArgumentParser()
    parser.add_argument("-o",
                        "--output",
                        help="Output folder",
                        default="report")
    parser.add_argument("-t", 
                        "--template", 
                        help="Template file", 
                        default="lib/ytube.jinja2") 
    args = parser.parse_args()
    main(args)
    print("Script Complete")
    print(datetime.now() - startTime)