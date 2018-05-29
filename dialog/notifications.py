import requests
import json

header = {"Content-Type": "application/json; charset=utf-8",
          "Authorization": "Basic NjY5NDBjMjItOTkwZS00YjY2LTgxOGMtMDA0OTllOTliZTQ1"}

payload = {"app_id": "53af60e2-5c37-49e4-9b46-f58c6e329366",
           "included_segments": ["All"],
           "chrome_web_icon":"https://raw.githubusercontent.com/ArthurYang1228/MIS_project/master/misproject/LOGO(%E7%B2%89%2B%E8%97%8D).png",
           #"include_player_ids":["90621e10-88aa-4e9a-a5ba-5e69f3e0bd48"],
           "send_after":"2018-05-26 00:30:00 am UTC+8:00 ",
           "contents": {"en": "Crobot 提醒您吃藥囉!"}}


req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))

print(req.status_code, req.reason)