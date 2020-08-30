import os
from mailjet_rest import Client


def send_mailjet_email(cfg, html):
    api_key = os.getenv("MJ_APIKEY_PUBLIC")
    api_secret = os.getenv("MJ_APIKEY_PRIVATE")
    mailjet = Client(auth=(api_key, api_secret), version="v3.1")
    data = {
        "Messages": [
            {
                "From": {"Email": cfg["email"]["from"], "Name": "Youtube NLP"},
                "To": [{"Email": cfg["email"]["to"], "Name": "Stock Investor"}],
                "Subject": "Job Report",
                "HTMLPart": html,
            }
        ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())
