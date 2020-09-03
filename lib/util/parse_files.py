# Author - David Li
# Meant to convert hardcoded files to new data format

import pandas as pd

# pandas structure will be
#
# videoId, date, source, keywords (not used), route
# - source is N/A for legacy videos
import os
import glob
import re
from datetime import datetime


def extract_date(date_str: str) -> str:
    match = re.search(r"\d{4}-\d{2}-\d{2}", date_str)
    date = datetime.strptime(match.group(), "%Y-%m-%d").date()
    return match.group()


def get_video_id(file_path: str) -> str:
    rel_name = os.path.basename(file_path)
    filename, _ = os.path.splitext(rel_name)
    return filename


temp_data = []
for file_path in glob.iglob("investing/**/*.html"):
    video_id = get_video_id(file_path)
    extracted_date = extract_date(file_path)
    file_dict = {
        "video_id": video_id,
        "date": extracted_date,
        "source": "N/A",
        "keywords": [],
        "description": "",
        "path": file_path,
    }
    temp_data.append(file_dict)

yt_df = pd.DataFrame(temp_data)

yt_df.to_csv("yt_data.csv", index=False)
