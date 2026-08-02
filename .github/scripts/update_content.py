#!/usr/bin/env python3
"""
LILY Workbench - Daily Content Update Script
Runs inside GitHub Actions every day at 08:00 Beijing time.
Updates the HTML file with current date info and triggers GitHub Pages rebuild.
"""

import re
from datetime import datetime, timezone, timedelta

HTML_PATH = "index.html"
TZ = timezone(timedelta(hours=8))  # Beijing time
now = datetime.now(TZ)
today_str = now.strftime("%Y-%m-%d")

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Calculate day count since start date (2026-07-28)
start = datetime(2026, 7, 28, tzinfo=TZ)
day_num = (now.date() - start.date()).days + 1

# 1. Update footer date
old_footer = re.search(r"<span id=\"footer-date\">.*?</span>", html)
if old_footer:
    new_footer = f'<span id="footer-date">· 今日：{today_str}（第{day_num}天）</span>'
    html = html.replace(old_footer.group(), new_footer)

# 2. Update the update notice to show last refresh time
old_notice_tag = re.search(
    r'<div class="update-notice">.*?</div>',
    html, re.DOTALL
)
if old_notice_tag:
    new_notice = f'''<div class="update-notice">
    🤖 <strong>全自动更新</strong> · GitHub Actions 每日 08:00（北京时间）自动刷新 · 无需电脑开机 · 打开即最新
    <span style="display:block;font-size:0.75rem;font-weight:normal;margin-top:2px;">最近更新：{today_str} {now.strftime("%H:%M")} · 倒计时+今日任务+时政+资源+真题+预测全部每日自更新</span>
  </div>'''
    html = html.replace(old_notice_tag.group(), new_notice)

# 3. Update initial countdown display value (fallback before JS runs)
cd_match = re.search(r'<span class="num red" id="cd-days">(\d+)</span>', html)
if cd_match:
    exam_date = datetime(2027, 7, 26, 9, 0, 0, tzinfo=TZ)
    days_left = (exam_date - now).days
    html = html.replace(
        f'<span class="num red" id="cd-days">{cd_match.group(1)}</span>',
        f'<span class="num red" id="cd-days">{days_left}</span>'
    )

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ Updated: {today_str} (Day {day_num}, {days_left} days until exam)")
print(f"   GitHub Pages will auto-rebuild after push.")
