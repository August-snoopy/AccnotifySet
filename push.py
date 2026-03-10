import requests
import json
import sys
import os
import re
from datetime import datetime, timedelta

# 配置区
ACC_TOKEN = os.getenv("ACC_TOKEN")
API_URL = f"https://an.trah.cn/push/{ACC_TOKEN}"
START_DATE = datetime(2026, 3, 2) # 第一周周一

def send_push(title, content):
    payload = {"title": title, "content": content}
        try:
                res = requests.post(API_URL, data=payload, timeout=10)
                        print(f"推送状态: {res.status_code}")
                            except Exception as e:
                                    print(f"推送出错: {e}")

                                    def get_current_week(now):
                                        delta = now - START_DATE
                                            return (delta.days // 7) + 1

                                            def is_course_active(course_name, current_week):
                                                # 简单正则匹配 "(1-8周)" 这种格式
                                                    match = re.search(r'\((\d+)-(\d+)周\)', course_name)
                                                        if match:
                                                                start, end = map(int, match.groups())
                                                                        return start <= current_week <= end
                                                                            return True # 如果没写周数，默认常驻

                                                                            def main():
                                                                                if len(sys.argv) < 2: return
                                                                                    mode = sys.argv[1]
                                                                                        
                                                                                            # 强制获取北京时间
                                                                                                now = datetime.utcnow() + timedelta(hours=8)
                                                                                                    curr_week = get_current_week(now)
                                                                                                        
                                                                                                            with open('schedule.json', 'r', encoding='utf-8') as f:
                                                                                                                    all_data = json.load(f)
                                                                                                                        
                                                                                                                            weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                                                                                                                                today_name = weekdays[now.weekday()]
                                                                                                                                    today_events = all_data.get(today_name, [])

                                                                                                                                        # 过滤当前周有效的课程
                                                                                                                                            active_events = [e for e in today_events if is_course_active(e['name'], curr_week)]

                                                                                                                                                if mode == "summary":
                                                                                                                                                        title = f"📅 第{curr_week}周 {today_name} 课程概览"
                                                                                                                                                                if not active_events:
                                                                                                                                                                            content = "今天没有排课，可以专注科研或休息。"
                                                                                                                                                                                    else:
                                                                                                                                                                                                content = "\n".join([f"⏰ {e['time']} | {e['name']} @{e['location']}" for e in active_events])
                                                                                                                                                                                                        send_push(title, content)importimportimport

                                                                                                                                                                                                            elif mode == "reminder":
                                                                                                                                                                                                                    for event in active_events:
                                                                                                                                                                                                                                ev_time = datetime.strptime(event['time'], "%H:%M").replace(
                                                                                                                                                                                                                                                year=now.year, month=now.month, day=now.day
                                                                                                                                                                                                                                                            )
                                                                                                                                                                                                                                                                        diff = (ev_time - now).total_seconds() / 60
                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                                # 课前 15-25 分钟触发提醒
                                                                                                                                                                                                                                                                                                            if 15 <= diff <= 25:
                                                                                                                                                                                                                                                                                                                            send_push("🔔 上课提醒", f"课程：{event['name']}\n地点：{event['location']}\n上课时间：{event['time']}")

                                                                                                                                                                                                                                                                                                                            if __name__ == "__main__":
                                                                                                                                                                                                                                                                                                                                main()import