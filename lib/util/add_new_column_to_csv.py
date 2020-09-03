import pandas as pd

yt_df = pd.read_csv("yt_data.csv")

yt_df = yt_df.set_index("video_id")

yt_df["title"] = ""
print(yt_df)
# yt_df.to_csv("yt_data.csv")
