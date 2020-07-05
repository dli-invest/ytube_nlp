import requests 
import os
from datetime import datetime, timezone, timedelta

def main(args):
    channel_id = args.channel
    video_data = get_video_data_for_channel(channel_id)

def get_video_data_for_channel(channel_id):
    raw_video_data = search_videos_for_channel(channel_id)
    video_data = extract_key_video_data(raw_video_data)
    return video_data

def extract_key_video_data(video_data):
    # Takes video search response and extracts the data of interest
    # videoId, title, description, channelId, publishedAt
    key_video_data = []
    for video in video_data.get("items"):
        snippet = video.get('snippet')
        vid_id = video.get('id')
        
        videoID = vid_id.get('videoId')
        channelId = snippet.get('channelId')
        description = snippet.get('description')
        title = snippet.get('title')
        video_data = dict(
            videoID=videoID,
            channelId=channelId,
            description=description,
            title=title
        )
        key_video_data.append(video_data)
    return key_video_data

def search_videos_for_channel(channel_id, params=dict(part='snippet')):
    youtube_api = 'https://www.googleapis.com/youtube/v3/search'
    youtube_api_key = os.getenv("YOUTUBE_API_KEY")
    params['channelId'] = channel_id
    params['order'] = 'date'
    current_date = datetime.now(timezone.utc)
    publishedBefore = (current_date - timedelta(hours=12)).isoformat()
    publishedAfter = (current_date - timedelta(hours=48)).isoformat()
    params['publishedBefore'] = publishedBefore
    params['publishedAfter'] = publishedAfter
    params['maxResults'] = 100
    params['key'] = youtube_api_key

    r = requests.get(youtube_api, params=params).json()
    # NLP for CSE and CVE
    return r

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-c",
                        "--channel",
                        help="Youtube Video Id",
                        default="UC6zHYEnBuH4DYxbPLsbIaVw")
    args = parser.parse_args()
    main(args)
