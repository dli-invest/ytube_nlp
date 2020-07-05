# Hold off on prophet image generation, probably not useful since I buy small caps

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

def main(args):
    end_date = str(date.today())
    gh_pages_name = 'gh-pages'
    for report_cfg_file in glob.glob("lib/cfg/*.yml"):
        report_cfg = get_config(report_cfg_file)
        report_name = report_cfg["name"]
        output_folder = f"{args.output}/{report_name}"
        pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)

        # Attempt to move the folder
        # Make in gh pages folder even if exists
        gh_report_folder = f"{args.output}/{gh_pages_name}/{report_name}/{end_date}"
        pathlib.Path(gh_report_folder).mkdir(parents=True, exist_ok=True)
        # Any files in the output folder, if I need nested files in folders
        # use something else

        # Make channel videos
        for channel in report_cfg["channels"]:
            channel_id = channel.get('id')
            if channel_id is not None:
                video_data = get_video_data_for_channel(channel_id)
                for video_info in video_data:
                    video_id = video_info.get('videoID')
                    with YTNLP(video_id=video_id, html_template='lib/ytube.jinja2') as yt_nlp:
                        file_path = f"{output_folder}/{video_id}.html"
                        success_attempt = yt_nlp.gen_report_for_id(video_id, report_path=file_path, video_data=video_data)
                        print(success_attempt)
                print(video_data)
                # If no_transcript is retrieved
                # analyze the video_data only 
                # else 
                # grab automate transcript from youtube
            else:
                print('Channel not found for')
                print(channel)
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