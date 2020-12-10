import sys
import argparse as ap
import pathlib
import glob
import shutil
import pandas as pd

from datetime import date, datetime, timedelta
from lib.util import get_config
from lib.youtube.get_videos import get_video_data_for_channel
from lib.youtube.yt_nlp import YTNLP
from lib.email import send_mailjet_email
from jinja2 import Template
from lib.util.send_discord import send_data_to_discord

def path_to_url(url: str) -> str:
    if url == "":
        return None
    base_url = "http://dli-invest.github.io/ytube_nlp"
    return f"{base_url}/{url}"


def main(args):
    end_date = str(date.today())
    tomorrow = date.today() + timedelta(1)
    gh_report_folder_next = datetime.strftime(tomorrow, '%Y-%m-%d')
    gh_pages_name = "gh-pages"
    yt_df = pd.read_csv("yt_data.csv", index_col="video_id")
    # TODO convert to object since this is so complicated
    # With an object I think it would be easier to parallelize
    for report_cfg_file in glob.glob("lib/cfg/*.yml"):
        report_cfg = get_config(report_cfg_file)
        report_name = report_cfg["name"]
        output_folder = f"{args.output}/{report_name}"
        pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)

        gh_report_folder = f"{args.output}/{gh_pages_name}/{report_name}"
        pathlib.Path(gh_report_folder).mkdir(parents=True, exist_ok=True)
        gh_report_folder2 = (
            f"{args.output}/{gh_pages_name}/{report_name}/{gh_report_folder_next}"
        )
        pathlib.Path(gh_report_folder2).mkdir(parents=True, exist_ok=True)

        email_channel_data = []
        # Make channel videos
        # This loop isn't extremely expensive as
        # we are just fetching text from an api
        for channel in report_cfg["channels"]:
            channel_id = channel.get("id")
            channel_label = channel.get("label")
            if channel_id != None:
                video_data = get_video_data_for_channel(channel_id)
                # loop through videos
                for video_info in video_data:
                    video_id = video_info.get("videoId")
                    # skip if video found already
                    if video_id in yt_df.index:
                        continue
                    title = video_info.get("title")
                    description = video_info.get("description")
                    publishedAt = video_info.get("publishedAt")

                    with YTNLP(
                        video_id=video_id, html_template="lib/ytube.jinja2"
                    ) as yt_nlp:
                        # this is adjusted with a date for the gh pages step
                        file_folder1 = f"{output_folder}/{gh_report_folder_next}/{video_id}"
                        file_folder2 = f"{output_folder}/{end_date}/{video_id}"
                        pathlib.Path(file_folder1).mkdir(parents=True, exist_ok=True)
                        pathlib.Path(file_folder2).mkdir(parents=True, exist_ok=True)
                        file_path = f"{output_folder}/{end_date}/{video_id}.html"
                        is_generated = False
                        # Since I intend to only use transcript videos
                        # this line doesnt matter
                        if channel.get("no_transcript") != True:
                            is_generated = yt_nlp.gen_report_for_id(
                                video_id, report_path=file_path, video_data=video_data
                            )

                        # temp array of objects
                        matches_per_vid = []
                        if title is not None:
                            temp_matches, _ = yt_nlp.get_text_matches(title)
                            matches_per_vid = [*matches_per_vid, *temp_matches]
                        if description is not None:
                            temp_matches, _ = yt_nlp.get_text_matches(description)
                            matches_per_vid = [*matches_per_vid, *temp_matches]
                        match_object = video_info
                        match_object["phrases"] = matches_per_vid
                        match_object["source"] = channel_label
                        if is_generated is False:
                            match_object["has_report"] = False
                        else:
                            match_object["has_report"] = True

                            # append object to pandas dataframe
                            new_file = {
                                "date": publishedAt,
                                "title": title,
                                "source": channel_label,
                                "keywords": [],
                                "description": description,
                                "path": file_path,
                            }
                            # df.loc[video_id] = new_file
                            if video_id in yt_df.index:
                                print(f"Video {video_id} exists - not setting vid_id")
                            else:
                                print("adding row")
                                # add row to df
                                yt_df = yt_df.append(
                                    pd.Series(
                                        new_file, index=yt_df.columns, name=video_id
                                    )
                                )
                                print(new_file)

                    if channel.get("only_on_nlp_match") is True:
                        # check for nlp matches
                        if len(match_object["phrases"]) > 0:
                            email_channel_data.append(match_object)
                    else:
                        email_channel_data.append(match_object)
            else:
                print("Channel not found for")
                print(channel)
        # Try to send data to discord
        try:
            send_data_to_discord(email_channel_data)
        except Exception as e:
            print(e)
            pass
        # Move to function or something or rewrite to class
        try:
            options = dict(Version="1.0.0", EMAIL_DATA=email_channel_data)
            with open("lib/email.jinja2") as file_:
                template = Template(file_.read())
            email_html = template.render(**options)
            # send email
            send_mailjet_email(report_cfg, email_html)
            with open("report/investing/email.html", "w", errors="ignore") as f:
                f.write(email_html)

        except Exception as e:
            print("FAILED TO MAKE TEMPLATE")
            print(e)
        # this includes folders, need to correct my output folder to be nested one more
        for report_file in glob.glob(f"{output_folder}/*"):
            try:
                # Move report files
                # gh report folder expected to be gh-pages/subcategory/date
                shutil.move(report_file, gh_report_folder)
            except shutil.Error as e:
                print(e)
        yt_df = yt_df.sort_values(by=["date"], ascending=False)
        yt_df.to_csv("yt_data.csv")
        yt_df["path"] = yt_df["path"].apply(
            lambda x: path_to_url(x)
        )  # f'<a href="./{investing/2020-07-09/-5aG8r2fkM0.html}'
        try:
            options = dict(
                HTML_TABLE=yt_df.to_html(
                    table_id="datatable",
                    classes="uk-table cell-border compact stripe",
                    render_links=True,
                )
            )
            with open("lib/index.jinja2") as file_:
                template = Template(file_.read())
            index_html = template.render(**options)
            with open("report/gh-pages/index.html", "w") as file_:
                file_.write(index_html)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    assert sys.version_info >= (3, 6)
    startTime = datetime.now()
    parser = ap.ArgumentParser()
    parser.add_argument("-o", "--output", help="Output folder", default="report")
    parser.add_argument(
        "-t", "--template", help="Template file", default="lib/ytube.jinja2"
    )
    # Ensure keys are available

    args = parser.parse_args()
    main(args)
    print("Script Complete")
    print(datetime.now() - startTime)