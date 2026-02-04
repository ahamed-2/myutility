"""
🤖 Smart Utility Bot - Vercel Compatible Version
👨‍💻 Developer: Ahamed Rahim (@al_rahim2)
🔗 GitHub: https://github.com/ahamed-2
🌐 Portfolio: https://ahamed-rahim.pages.dev/
🔌 All API Credits: @Offline_669
📢 Channel: @ahamed_068
Deployment: Vercel + Flask Web Server
"""

import os
import asyncio
import json
import requests
import logging
import time
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import quote

from flask import Flask, request, jsonify
from pyrogram import Client, filters
from pyrogram.types import (
    Message, InlineKeyboardMarkup, 
    InlineKeyboardButton, CallbackQuery
)
from pyrogram.enums import ParseMode
import threading

# ==================== FLASK APP FOR VERCEL ====================
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    """Home endpoint for Vercel health check"""
    return jsonify({
        "status": "online",
        "service": "Smart Utility Bot",
        "developer": "@al_rahim2",
        "github": "https://github.com/ahamed-2",
        "channel": "@ahamed_068",
        "timestamp": datetime.now().isoformat()
    })

@app_flask.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "bot_status": "running" if hasattr(telegram_bot, 'is_running') else "stopped",
        "timestamp": datetime.now().isoformat()
    })

@app_flask.route('/api/status')
def api_status():
    """API status check"""
    try:
        return jsonify({
            "ai_apis": {
                "perplex_ai": check_url("https://perplex-pro.vercel.app"),
                "gpt4_ai": check_url("https://gpt-4-ask.vercel.app"),
                "multi_ai": check_url("https://multi-ai-ask.vercel.app")
            },
            "streaming_apis": {
                "primevideo": check_url("https://primevideo.the-zake.workers.dev"),
                "netflix": check_url("https://netflix.the-zake.workers.dev"),
                "spotify": check_url("https://spotifydl.the-zake.workers.dev")
            }
        })
    except:
        return jsonify({"error": "Status check failed"}), 500

def check_url(url):
    """Check if URL is accessible"""
    try:
        response = requests.get(url.split('?')[0], timeout=5)
        return response.status_code == 200
    except:
        return False

# ==================== CONFIGURATION ====================
ADMIN_IDS = {
    "Ahamed": 6844656059,
    "Jubair Bro": 8486562838,
    "Pokkie Torikul": 5967798239,
    "Aman Vai": 1956820398,
    "Ben": 1095091493,
    "Zoy Bro": 6556220592
}

# API ENDPOINTS
API_ENDPOINTS = {
    # AI APIs by @Offline_669
    "perplex_ai": "https://perplex-pro.vercel.app/api",
    "gpt4_ai": "https://gpt-4-ask.vercel.app/ask",
    "multi_ai": "https://multi-ai-ask.vercel.app/api",
    
    # Streaming APIs by @al_rahim2
    "primevideo": "https://primevideo.the-zake.workers.dev",
    "zee5": "https://zee5.the-zake.workers.dev",
    "appletv": "https://appletv.the-zake.workers.dev",
    "airtelxstream": "https://airtelxstream.the-zake.workers.dev",
    "sunnxt": "https://sunnxt.the-zake.workers.dev",
    "ahavideo": "https://ahavideo.the-zake.workers.dev",
    "iqiyi": "https://iqiyi.the-zake.workers.dev",
    "wetv": "https://wetv.the-zake.workers.dev",
    "shemaroo": "https://shemaroo.the-zake.workers.dev",
    "bookmyshow": "https://bookmyshow.the-zake.workers.dev",
    "plextv": "https://plextv.the-zake.workers.dev",
    "addatimes": "https://addatimes.the-zake.workers.dev",
    "stage": "https://stage.the-zake.workers.dev",
    "netflix": "https://netflix.the-zake.workers.dev",
    "spotify": "https://spotifydl.the-zake.workers.dev",
}

# ==================== LOGGING ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== TELEGRAM BOT ====================
# Vercel environment এ environment variables
API_ID = int(os.environ.get("API_ID", "26158708"))
API_HASH = os.environ.get("API_HASH", "5f4602d47f32aabce2cbe0ab1244171f")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8555126706:AAHiMEe0fly9lNFNHW7EsE4vCXzYz8-mBQ4")

telegram_bot = Client(
    name="smart_util_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True,
    no_updates=True  # Vercel এর জন্য
)

# ==================== DATABASE (Vercel Compatible) ====================
class Database:
    """Vercel-compatible database using JSON files"""
    
    def __init__(self):
        # Vercel এ /tmp directory use করতে হবে
        self.data_dir = "/tmp/data" if os.path.exists("/tmp") else "data"
        self.users_file = f"{self.data_dir}/users.json"
        self.stats_file = f"{self.data_dir}/stats.json"
        self.ensure_files()
    
    def ensure_files(self):
        """Ensure data directory exists"""
        Path(self.data_dir).mkdir(exist_ok=True)
        Path("downloads").mkdir(exist_ok=True)
        
        default_stats = {
            "total_users": 0,
            "total_commands": 0,
            "ai_queries": 0,
            "media_downloads": 0,
            "start_time": datetime.now().isoformat()
        }
        
        # Create files if they don't exist
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)
        
        if not os.path.exists(self.stats_file):
            with open(self.stats_file, 'w') as f:
                json.dump(default_stats, f)
    
    def add_user(self, user_id: int, username: str, first_name: str):
        """Add user to database"""
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
            
            if str(user_id) not in users:
                users[str(user_id)] = {
                    "username": username,
                    "first_name": first_name,
                    "joined": datetime.now().isoformat(),
                    "commands_used": 0
                }
                
                with open(self.users_file, 'w') as f:
                    json.dump(users, f, indent=2)
                
                self.update_stats("total_users", 1)
                return True
            return False
        except Exception as e:
            logger.error(f"Database error: {e}")
            return False
    
    def update_stats(self, key: str, increment: int = 1):
        """Update statistics"""
        try:
            with open(self.stats_file, 'r') as f:
                stats = json.load(f)
            
            stats[key] = stats.get(key, 0) + increment
            
            with open(self.stats_file, 'w') as f:
                json.dump(stats, f, indent=2)
        except Exception as e:
            logger.error(f"Stats update error: {e}")
    
    def get_stats(self):
        """Get current statistics"""
        try:
            with open(self.stats_file, 'r') as f:
                return json.load(f)
        except:
            return {"error": "Could not load stats"}

db = Database()

# ==================== API HANDLER ====================
class APIHandler:
    """Handle all API calls"""
    
    @staticmethod
    async def perplex_ai(question: str) -> str:
        """Perplexity AI API"""
        try:
            url = f"{API_ENDPOINTS['perplex_ai']}?q={quote(question)}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('answer', data.get('response', 'উত্তর পাওয়া যায়নি'))
            return "Perplexity API ত্রুটি"
        except Exception as e:
            logger.error(f"Perplexity Error: {e}")
            return f"Perplexity ত্রুটি: API কাজ করছে না"
    
    @staticmethod
    async def gpt4_ai(question: str) -> str:
        """GPT-4 AI API"""
        try:
            url = f"{API_ENDPOINTS['gpt4_ai']}?prompt={quote(question)}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('response', data.get('answer', 'উত্তর পাওয়া যায়নি'))
            return "GPT-4 API ত্রুটি"
        except Exception as e:
            logger.error(f"GPT-4 Error: {e}")
            return f"GPT-4 ত্রুটি: API কাজ করছে না"

# ==================== COMMAND HANDLERS ====================
@telegram_bot.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    """Welcome command"""
    user = message.from_user
    
    # Add user to database
    db.add_user(
        user.id,
        user.username or "",
        user.first_name or "User"
    )
    
    # Update stats
    db.update_stats("total_commands")
    
    welcome_text = f"""
🎉 **স্বাগতম {user.first_name or 'ভাই/আপু'}!** 🎉

🤖 **Smart Utility Bot** এ আপনাকে স্বাগতম!

**দ্রুত শুরু:**
• `/ai [প্রশ্ন]` - AI এর সাথে কথা বলুন
• `/yt [লিঙ্ক]` - YouTube ভিডিও ডাউনলোড
• `/bg` - ছবির ব্যাকগ্রাউন্ড সরান
• `/time [শহর]` - বিশ্ব সময় দেখুন

**আরও ফিচার:** `/help`

👨‍💻 **ডেভেলপার:** @al_rahim2
🔗 **চ্যানেল:** @ahamed_068
🌐 **GitHub:** https://github.com/ahamed-2
⚡ **Deployed on:** Vercel
    """
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📚 সাহায্য", callback_data="help"),
            InlineKeyboardButton("⚡ ফিচার", callback_data="features")
        ],
        [
            InlineKeyboardButton("👨‍💻 ডেভেলপার", url="t.me/al_rahim2"),
            InlineKeyboardButton("🔗 চ্যানেল", url="t.me/ahamed_068")
        ]
    ])
    
    await message.reply_text(
        welcome_text,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )

@telegram_bot.on_message(filters.command("ai"))
async def ai_command(client: Client, message: Message):
    """AI command"""
    if len(message.command) < 2:
        await message.reply_text("❌ **ব্যবহার:** `/ai [আপনার প্রশ্ন]`")
        return
    
    question = " ".join(message.command[1:])
    db.update_stats("ai_queries")
    db.update_stats("total_commands")
    
    processing_msg = await message.reply_text("🤖 **AI চিন্তা করছে...**")
    
    try:
        # Try Perplexity AI first
        response = await APIHandler.perplex_ai(question)
        
        # If empty or error, try GPT-4
        if not response or len(response) < 10 or "ত্রুটি" in response:
            response = await APIHandler.gpt4_ai(question)
        
        # Format response
        final_text = f"🤖 **AI উত্তর:**\n\n{response}\n\n"
        final_text += "✨ **আরও সাহায্য:** `/help`\n\n"
        final_text += "⚡ **Powered by @al_rahim2**\n"
        final_text += "🔌 **API Credits: @Offline_669**\n"
        final_text += "🌐 **Hosted on: Vercel**"
        
        await processing_msg.edit_text(
            final_text,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
        
    except Exception as e:
        await processing_msg.edit_text(
            f"❌ **ত্রুটি হয়েছে:**\n\n"
            f"`{str(e)[:200]}`\n\n"
            f"দুঃখিত, AI সার্ভিস সাময়িকভাবে অকার্যকর।"
        )

@telegram_bot.on_message(filters.command("ping"))
async def ping_command(client: Client, message: Message):
    """Ping command"""
    start_time = time.time()
    msg = await message.reply_text("🏓 **পিং...**")
    end_time = time.time()
    
    latency = round((end_time - start_time) * 1000, 2)
    stats = db.get_stats()
    
    response = f"🏓 **পং!**\n\n"
    response += f"⏱️ **লেটেন্সি:** `{latency}ms`\n"
    response += f"👥 **ইউজার:** `{stats.get('total_users', 0)}`\n"
    response += f"📊 **কমান্ড:** `{stats.get('total_commands', 0)}`\n"
    response += f"🤖 **AI কোয়েরি:** `{stats.get('ai_queries', 0)}`\n\n"
    response += f"✅ **বট স্ট্যাটাস:** একটিভ\n"
    response += f"☁️ **হোস্টিং:** Vercel\n\n"
    response += "⚡ **Powered by @al_rahim2**\n"
    response += "📢 **Channel: @ahamed_068**"
    
    await msg.edit_text(response, parse_mode=ParseMode.MARKDOWN)

@telegram_bot.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    """Help command"""
    help_text = """
🤖 **Smart Utility Bot - সাহায্য**

**মূল কমান্ড:**
• `/ai [প্রশ্ন]` - AI চ্যাট
• `/ping` - বট স্ট্যাটাস
• `/time [শহর]` - বিশ্ব সময়
• `/calc [এক্সপ্রেশন]` - ক্যালকুলেটর

**টেক্সট টুলস:**
• `/text [option] [text]` - টেক্সট এডিট
• `/style [text]` - স্টাইলিশ ফন্ট
• `/fake` - ফেইক তথ্য

**ইউটিলিটি:**
• `/quote` - উক্তি
• `/joke` - জোক
• `/credits` - ক্রেডিটস

⚡ **Powered by @al_rahim2**
🌐 **Hosted on: Vercel**
📢 **Channel: @ahamed_068**
    """
    
    await message.reply_text(help_text)

@telegram_bot.on_message(filters.command("time"))
async def world_time(client: Client, message: Message):
    """World time command"""
    import pytz
    from datetime import datetime
    
    cities = {
        "ঢাকা": "Asia/Dhaka",
        "কলকাতা": "Asia/Kolkata",
        "লন্ডন": "Europe/London",
        "নিউইয়র্ক": "America/New_York",
        "টোকিও": "Asia/Tokyo",
    }
    
    response = "🕒 **বিশ্ব সময়**\n\n"
    
    for city, tz_name in cities.items():
        tz = pytz.timezone(tz_name)
        city_time = datetime.now(tz).strftime("%I:%M %p")
        response += f"• **{city}:** `{city_time}`\n"
    
    response += "\n⚡ **Powered by @al_rahim2**"
    await message.reply_text(response)

# ==================== CALLBACK HANDLERS ====================
@telegram_bot.on_callback_query()
async def handle_callback(client: Client, query: CallbackQuery):
    """Handle callback queries"""
    
    if query.data == "help":
        await query.message.edit_text(
            "ℹ️ **সাহায্য পেতে:** `/help` কমান্ড ব্যবহার করুন\n\n"
            "বা ভিজিট করুন:\n"
            "• GitHub: https://github.com/ahamed-2\n"
            "• Portfolio: https://ahamed-rahim.pages.dev/\n\n"
            "⚡ **Powered by @al_rahim2**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 ব্যাক", callback_data="back_start")]
            ])
        )
    
    elif query.data == "features":
        await query.message.edit_text(
            "⚡ **মূল ফিচারসমূহ:**\n\n"
            "• AI চ্যাট (Perplexity, GPT-4)\n"
            "• টেক্সট প্রসেসিং টুলস\n"
            "• বিশ্ব সময় দেখানো\n"
            "• ইউটিলিটি কমান্ড\n\n"
            "সব ফিচার দেখতে: `/help`\n\n"
            "⚡ **Powered by @al_rahim2**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 ব্যাক", callback_data="back_start")]
            ])
        )
    
    elif query.data == "back_start":
        user = query.from_user
        welcome_text = f"🎉 **স্বাগতম {user.first_name or 'ভাই/আপু'}!**\n\nআপনার কী সাহায্য লাগবে?"
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📚 সাহায্য", callback_data="help"),
                InlineKeyboardButton("⚡ ফিচার", callback_data="features")
            ],
            [
                InlineKeyboardButton("👨‍💻 ডেভেলপার", url="t.me/al_rahim2"),
                InlineKeyboardButton("🔗 চ্যানেল", url="t.me/ahamed_068")
            ]
        ])
        
        await query.message.edit_text(
            welcome_text,
            reply_markup=keyboard
        )
    
    await query.answer()

# ==================== BOT STARTUP FUNCTION ====================
async def run_bot():
    """Run the Telegram bot"""
    try:
        await telegram_bot.start()
        telegram_bot.is_running = True
        print("🤖 Telegram Bot Started Successfully!")
        print(f"👨‍💻 Developer: @al_rahim2")
        print(f"📢 Channel: @ahamed_068")
        print(f"🌐 Host: Vercel")
        
        # Keep bot running
        await telegram_bot.idle()
        
    except Exception as e:
        print(f"❌ Bot Error: {e}")
        telegram_bot.is_running = False

def start_flask():
    """Start Flask server for Vercel"""
    port = int(os.environ.get("PORT", 8080))
    app_flask.run(host='0.0.0.0', port=port)

# ==================== VERCEL COMPATIBLE MAIN ====================
def main():
    """Main function for Vercel deployment"""
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()
    
    # Start Telegram bot
    print("🚀 Starting Smart Utility Bot on Vercel...")
    asyncio.run(run_bot())

# Vercel এর জন্য এই ফাংশন কল হবে
if __name__ == "__main__":
    main()
