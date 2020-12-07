import os
import json
import requests
from datetime import date

def send_data_to_discord(channel_data):
    print(channel_data)
    base_url = "http://dli-invest.github.io/ytube_nlp"
    def make_embed(list_item):
        videoId = list_item.get('videoId')
        channelId = list_item.get('channelId')
        title = list_item.get('title')
        end_date = str(date.today())
        report_path = f"{base_url}/investing/{end_date}/{videoId}.html"
        return {
            "title": f"Annotation for {title}",
            "description": f"Video from {channelId} for {videoId}",
            "url": f"{report_path}"
        }
    def chunks(l, n):
        n = max(1, n)
        return (l[i:i+n] for i in range(0, len(l), n))

    def make_discord_request(embeds):
        url = os.getenv("DISCORD_VIDEO_WEBHOOK")
        if url == None:
            print('DISCORD_VIDEO_WEBHOOK Missing')
            pass
        data = {}
        data["content"] = "Transcribed Videos"
        data["embeds"] = embeds
        result = requests.post(
            url, data=json.dumps(data), headers={"Content-Type": "application/json"}
        )
        print(result)

    for sublist in chunks(channel_data, 10):
        embeds = [make_embed(video_data) for video_data in sublist]
        make_discord_request(embeds)