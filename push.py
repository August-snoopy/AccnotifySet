import requests
import json
import sys
import os
import re
from datetime import datetime, timedelta

# 配置区
ACC_TOKEN = os.getenv("ACC_TOKEN")
API_URL = f"https://an.trah.cn/push/{ACC_TOKEN}"
START_DATE = datetime(2026, 3, 2)

def send_push(title, content):
    if not ACC_TOKEN:
        print("错误: 未找到 ACC_TOKEN")
        return
    payload = {"title": title, "content": content}
    res = requests.post(API_URL, data=payload, timeout=10)
    print(f"推送响应: {res.status_code}")

def get_current_week(now):
    delta = now - START_DATE
    return (delta.days // 7) + 1

def is_course_active(course_name, current_week):
    match = re.search(r'\((\d+)-(\d+)周\)', course_name)
    if match:
        start, end = map(int, match.groups())
        return start <= current_week <= end
    return True

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "summary"
    now = datetime.utcnow() + timedelta(hours=8)
    curr_week = get_current_week(now)
    
    with open('schedule.json', 'r', encoding='utf-8') as f:
        all_data = json.load(f)
    
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    today_name = weekdays[now.weekday()]
    today_events = all_data.get(today_name, [])
    active_events = [e for e in today_events if is_course_active(e['name'], curr_week)]

    if mode == "summary":
        title = f"📅 第{curr_week}周 {today_name} 课程概览"
        content = "\n".join([f"⏰ {e['time']} | {e['name']} @{e['location']}" for e in active_events]) if active_events else "今天没课，享受科研！"
        send_push(title, content)
    else:
        for event in active_events:
            ev_time = datetime.strptime(event['time'].strip(), "%H:%M").replace(year=now.year, month=now.month, day=now.day)
            diff = (ev_time - now).total_seconds() / 60
            if 15 <= diff <= 25:
                send_push("🔔 上课提醒", f"课程：{event['name']}\n地点：{event['location']}\n时间：{event['time']}")

if __name__ == "__main__":
    main()                                                                                                                                                                                                                                                                                                                         
