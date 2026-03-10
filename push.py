import requests
import json
import sys
import os
import re
from datetime import datetime, timedelta
from urllib.parse import quote  # 必须引入这个来处理中文

ACC_TOKEN = os.getenv("ACC_TOKEN")
# 注意：这里我们把 API_URL 后面那个斜杠去掉，方便后面拼接
API_BASE = f"https://an.trah.cn/push/{ACC_TOKEN}"
START_DATE = datetime(2026, 3, 2)

def send_push(title, content):
    if not ACC_TOKEN:
        print("Error: ACC_TOKEN not found")
        return
    
    # 注意：路径参数中不能包含未转义的斜杠 / 或特殊字符
    safe_title = quote(title.replace("/", " "))
    safe_content = quote(content.replace("/", " "))
    
    # 严格按照样例图格式：https://an.trah.cn/push/{TOKEN}/{标题}/{内容}
    final_url = f"https://an.trah.cn/push/{ACC_TOKEN}/{safe_title}/{safe_content}"
    
    try:
        # 发送请求
        print(f"正在发送请求到: {final_url}")
        res = requests.get(final_url, timeout=10)
        print(f"推送响应状态码: {res.status_code}")
        print(f"服务器反馈: {res.text}")
    except Exception as e:
        print(f"请求失败: {e}")

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
        if active_events:
            content = "\n".join([f"⏰ {e['time']} | {e['name']} @{e['location']}" for e in active_events])
        else:
            content = "今天没课，享受科研！"
        send_push(title, content)
    else:
        for event in active_events:
            ev_time = datetime.strptime(event['time'].strip(), "%H:%M").replace(year=now.year, month=now.month, day=now.day)
            diff = (ev_time - now).total_seconds() / 60
            # 扩大检测范围到 30 分钟，确保手动测试能触发
            if 0 <= diff <= 30:
                send_push("🔔 上课提醒", f"课程：{event['name']}\n地点：{event['location']}\n时间：{event['time']}")

if __name__ == "__main__":
    main()
