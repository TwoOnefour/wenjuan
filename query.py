import requests
import json
import random
import datetime
import urllib3
import time
import os


urllib3.disable_warnings()
# with open("./query.json", "r", encoding="utf-8") as f:
#     result = json.loads(f.read())
url = "https://www.wenjuan.com/api/rspd/s/UZBZJvzGbXK/?is=qrcode"


if not os.path.exists(os.getcwd() + "/query.json"):
    with open("./query.html","w",encoding="utf-8") as f:
        html = requests.get(url, verify=False,headers={
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34"
    }).text
        f.write(html)
        html = html.split("var project = ")[1].split("var")[0].strip("\n").strip(";")
        f.write(html)
    # print(requests.get(url, verify=False,headers={         "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34"     }).text)
else:
    with open("./query.json","r",encoding="utf-8") as f:
        html = f.read()
js = json.loads(html)
while True:
    result = js
    answer = {}
    for i in result["QUESTION_DICT"]:
        per_answer = []
        if result["QUESTION_DICT"][i]["question_type"] != 3:
            per_answer.append(result["QUESTION_DICT"][i]["option_id_list"][random.randint(0, len(result["QUESTION_DICT"][i]["option_id_list"]) - 1)])
            answer[result["QUESTION_DICT"][i]["_id"]["$oid"]] = per_answer
        else:
            loop = random.randint(1, len(result["QUESTION_DICT"][i]["option_id_list"]))
            for j in range(loop):
                last = random.randint(0, len(result["QUESTION_DICT"][i]["option_id_list"]) - 1)
                per_answer.append([result["QUESTION_DICT"][i]["option_id_list"][last]])
                answer[result["QUESTION_DICT"][i]["_id"]["$oid"]] = per_answer
                result["QUESTION_DICT"][i]["option_id_list"].pop(last)
    # from requests_html import HTMLSession
    # sessions = HTMLSession()
    # r = sessions.get("https://www.wenjuan.com/api/rspd/s/UZBZJvzGbXK/?is=qrcode",verify=False)
    # r.html.render()
    # sessions = requests.Sessions()
    result = requests.post(url, json = {
        "total_answers_str": json.dumps(answer),
        "finish_status": "1",
        "timestr": str(datetime.datetime.now())[:-7],
        "idy_uuid": "",
        "project_version": 1,
        "question_captcha_map_str": "{}",
        "wx_user_info_str": "{}",
        "auto_submit_post": False,
        "question_ids_skipped_by_time": "{}",
        "appkey": "",
        "web_site": "wenjuan_web",
        "timestamp": int(time.time()*1000),
        "signature": ""
    },verify=False, headers={
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34"
    })
    # time.sleep(1)
    if json.loads(result.text)["seq"] >= 120:
        break