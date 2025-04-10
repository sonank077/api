import telebot
import requests
import json
import html
import re
import traceback
import time
from urllib.parse import urlparse, parse_qs
Python

import telebot
import requests
import json
import html
import re
import traceback
import time
from urllib.parse import urlparse, parse_qs
import subprocess
import sys

def install_missing_packages(module_names):
    """Installs missing Python packages using pip."""
    missing = []
    for module_name in module_names:
        try:
            __import__(module_name)
        except ImportError:
            missing.append(module_name)

    if missing:
        print(f"Installing missing packages: {', '.join(missing)}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
            print("Successfully installed missing packages.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing packages: {e}")
            print("Please ensure pip is installed and in your system's PATH.")
            sys.exit(1)
    else:
        print("All required packages are already installed.")

# List of required modules
required_modules = ['telebot', 'requests']
# Replace with your actual bot token
BOT_TOKEN = "6578917837:AAE_aFNfulvYw3clA94XZigAG0jdBQJZ48Y"
ALLOWED_GROUP_ID = [-1002170354953]  # Replace with your allowed group IDs (as integers)

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """Chào mừng bạn đến với bot tăng follow TikTok!

Để sử dụng các lệnh, vui lòng xem /help để biết thêm chi tiết.""")

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
Các lệnh hiện có:

/fl1 <username_tiktok> - Sử dụng API 1 để tăng follow TikTok.
    Ví dụ: /fl1  bacgau

/fl2 <username_tiktok> - Sử dụng API 22 để tăng follow TikTok.
    Ví dụ: /fl2 bacgau

/like <url> - Gửi yêu cầu đến API like với URL được cung cấp.
    Ví dụ: /like https://www.tiktok.com/@username/video/123456789

Lưu ý: Hiệu quả của các API có thể khác nhau và không được đảm bảo. Vui lòng sử dụng một cách thận trọng.
"""
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['fl1'])
def handle_fl1(message):
    user_id = str(message.from_user.id)
    args = message.text.split()

    if len(args) < 2:
        bot.reply_to(message, "<b>⚠️ Vui Lòng Nhập Username TikTok</b> \n\nVí dụ: \n<code>/fl1 bacgau</code>", parse_mode="HTML")
        return

    username = args[1]
    api_url = f"https://nvp310107.x10.mx/fltik.php?username={username}&key=shareconcac"

    try:
        response = requests.get(api_url, timeout=30, verify=False)
        response.raise_for_status()
        try:
            response_data = response.json()
            print(f"API 1 Response: {response_data}")
            if response_data.get("success"):
                bot.reply_to(message, f"<b>✅ Tăng Follow Thành Công (API 1):</b> @{html.escape(username)}", parse_mode="HTML")
            elif response_data.get("message"):
                wait_time_match = re.search(r'(\d+)\s*giây', response_data["message"], re.IGNORECASE)
                if wait_time_match:
                    bot.reply_to(message, f"<b>⚠️ Vui Lòng Chờ {wait_time_match.group(1)} Giây Trước Khi Thử Lại (API 1)!</b>\n\nhttps://www.tiktok.com/@{username}", parse_mode="HTML")
                else:
                    bot.reply_to(message, f"<b>⚠️ Lỗi Khi Tăng Follow (API 1)!</b>\n\nLỗi từ API 1: <code>{html.escape(response_data.get('message', 'Không có thông báo lỗi cụ thể'))}</code>\n\nhttps://www.tiktok.com/@{username}", parse_mode="HTML")
            else:
                bot.reply_to(message, f"<b>⚠️ Lỗi Khi Tăng Follow (API 1)!</b>\n\nPhản hồi không mong đợi từ API 1.\n\nhttps://www.tiktok.com/@{username}", parse_mode="HTML")
        except json.JSONDecodeError as e:
            print(f"Lỗi Giải Mã JSON (API 1): {e} - Raw Response: {response.text if 'response' in locals() else 'Không có phản hồi'}")
            bot.reply_to(message, f"<b>⚠️ Lỗi Khi Tăng Follow (API 1)!</b>\n\nLỗi khi xử lý phản hồi từ API 1.\n\nhttps://www.tiktok.com/@{username}", parse_mode="HTML")
    except requests.RequestException as e:
        print(f"Lỗi Kết Nối Api 1: {e}")
        bot.reply_to(message, f"<b>⚠️ Lỗi Kết Nối Đến API 1!</b>\n\nhttps://www.tiktok.com/@{username}", parse_mode="HTML")

user_cooldowns = {}  # {user_id: last_request_time}
COOLDOWN_DURATION = 180  # Thời gian chờ mặc định là 60 giây

MAINTENANCE_MESSAGE = "⚠️ Chức năng tăng follow hiện đang bảo trì. Vui lòng thử lại sau!"

@bot.message_handler(commands=['fl2'])
def handle_fl2(message):
    bot.reply_to(message, MAINTENANCE_MESSAGE, parse_mode="HTML")

@bot.message_handler(commands=['like'])
def handle_like(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "<b>⚠️ Vui lòng cung cấp URL sau lệnh /like</b>\n\nVí dụ: <code>/like https://www.tiktok.com/@username/video/123456789</code>", parse_mode="HTML")
        return

    url = args[1]
    api_url = f"https://nvp310107.x10.mx/tim.php?video_url={url}&key=shareconcac"

    try:
        response = requests.get(api_url, timeout=30, verify=False)
        response.raise_for_status()
        try:
            response_data = response.json()
            print(f"API Like Response (JSON): {response_data}")
            bot.reply_to(message, f"<b>✅ Yêu cầu thích (like) đã được gửi đi!</b>\n\nPhản hồi từ API (JSON):\n<code>{json.dumps(response_data, indent=4, ensure_ascii=False)}</code>", parse_mode="HTML")
        except json.JSONDecodeError as e:
            response_text = response.text
            print(f"Lỗi Giải Mã JSON (API Like): {e} - Raw Response: {response_text}")
            bot.reply_to(message, f"<b>⚠️ Lỗi Khi Xử Lý Phản Hồi API Like (Không phải JSON)!</b>\n\nPhản hồi từ API:\n<code>{html.escape(response_text[:500])}...</code>", parse_mode="HTML")
    except requests.RequestException as e:
        print(f"Lỗi Kết Nối API Like: {e}")
        bot.reply_to(message, f"<b>⚠️ Lỗi Kết Nối Đến API Like!</b>\n\n{html.escape(str(e))}", parse_mode="HTML")

if __name__ == '__main__':
    print("Bot is running...")
    bot.polling(none_stop=True)
