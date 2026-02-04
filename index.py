"""
🤖 Smart Utility Bot - Vercel Version
👨‍💻 Developer: Ahamed Rahim (@al_rahim2)
🔗 GitHub: https://github.com/ahamed-2
🌐 Portfolio: https://ahamed-rahim.pages.dev/
🔌 All API Credits: @Offline_669
📢 Channel: @ahamed_068
"""

import os
import json
import requests
import logging
import time
import random
from datetime import datetime
from pathlib import Path
from typing import Dict
from urllib.parse import quote
from flask import Flask, request, jsonify

# ==================== VERCEL FLASK APP ====================
app = Flask(__name__)

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
    "multi_ai": "https://multi-ai-ask.vercel.app",
    
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
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== DATABASE (SIMPLIFIED FOR VERCEL) ====================
class Database:
    def __init__(self):
        self.data_dir = Path("/tmp/data") if os.getenv("VERCEL") else Path("data")
        self.data_dir.mkdir(exist_ok=True)
        self.stats_file = self.data_dir / "stats.json"
        self.init_stats()
    
    def init_stats(self):
        default_stats = {
            "total_requests": 0,
            "ai_queries": 0,
            "api_calls": 0,
            "streaming_requests": 0,
            "last_updated": datetime.now().isoformat()
        }
        
        if not self.stats_file.exists():
            with open(self.stats_file, 'w') as f:
                json.dump(default_stats, f)
    
    def update_stats(self, key: str, increment: int = 1):
        try:
            with open(self.stats_file, 'r') as f:
                stats = json.load(f)
            
            stats[key] = stats.get(key, 0) + increment
            stats["last_updated"] = datetime.now().isoformat()
            
            with open(self.stats_file, 'w') as f:
                json.dump(stats, f, indent=2)
        except:
            pass
    
    def get_stats(self):
        try:
            with open(self.stats_file, 'r') as f:
                return json.load(f)
        except:
            return {"total_requests": 0, "ai_queries": 0}

db = Database()

# ==================== API HANDLER ====================
class APIHandler:
    """Handle all API calls for Vercel"""
    
    @staticmethod
    def perplex_ai(question: str) -> Dict:
        """Perplexity AI API"""
        try:
            url = f"{API_ENDPOINTS['perplex_ai']}?q={quote(question)}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=30)
            
            db.update_stats("api_calls")
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "answer": data.get('answer', data.get('response', 'উত্তর পাওয়া যায়নি')),
                    "source": "Perplexity AI",
                    "api": "@Offline_669"
                }
            return {"success": False, "error": "Perplexity API ত্রুটি"}
        except Exception as e:
            logger.error(f"Perplexity Error: {e}")
            return {"success": False, "error": f"Perplexity ত্রুটি: {str(e)}"}
    
    @staticmethod
    def gpt4_ai(question: str) -> Dict:
        """GPT-4 AI API"""
        try:
            url = f"{API_ENDPOINTS['gpt4_ai']}?prompt={quote(question)}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=30)
            
            db.update_stats("api_calls")
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "answer": data.get('response', data.get('answer', 'উত্তর পাওয়া যায়নি')),
                    "source": "GPT-4 AI",
                    "api": "@Offline_669"
                }
            return {"success": False, "error": "GPT-4 API ত্রুটি"}
        except Exception as e:
            logger.error(f"GPT-4 Error: {e}")
            return {"success": False, "error": f"GPT-4 ত্রুটি: {str(e)}"}
    
    @staticmethod
    def stream_download(service: str, url: str) -> Dict:
        """Streaming service downloader"""
        try:
            api_url = f"{API_ENDPOINTS.get(service)}?url={quote(url)}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(api_url, headers=headers, timeout=60)
            
            db.update_stats("streaming_requests")
            db.update_stats("api_calls")
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.text,
                    "service": service,
                    "api": "@al_rahim2"
                }
            return {"success": False, "error": f"API Error: {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def check_api_status() -> Dict:
        """Check all API status"""
        status = {}
        for name, url in API_ENDPOINTS.items():
            try:
                response = requests.get(url.split('?')[0], timeout=10)
                status[name] = response.status_code == 200
            except:
                status[name] = False
        return status

# ==================== UTILITY FUNCTIONS ====================
class Utility:
    """Utility functions for the bot"""
    
    @staticmethod
    def format_response(text: str, source: str = "", api: str = "") -> str:
        """Format responses with proper credits"""
        response = f"🤖 **AI উত্তর:**\n\n{text}\n\n"
        
        if source:
            response += f"🔍 **সোর্স:** {source}\n"
        
        response += "✨ **আরও সাহায্য:**\n"
        response += "- `/ai [প্রশ্ন]` - AI চ্যাট\n"
        response += "- `/ask [প্রশ্ন]` - Multi-AI\n"
        response += "- `/joke` - মজার জোক\n\n"
        
        response += "⚡ **Powered by @al_rahim2**\n"
        
        if api:
            response += f"🔌 **API Credits:** {api}\n"
        
        response += "📢 **Channel:** @ahamed_068\n"
        response += "🌐 **GitHub:** https://github.com/ahamed-2"
        
        return response
    
    @staticmethod
    def get_joke() -> str:
        """Get a random joke"""
        jokes = [
            "এক শিক্ষক ছাত্রকে জিজ্ঞেস করলেন, 'বৃষ্টি কেন পড়ে?'\nছাত্র উত্তর দিল, 'স্যার, মেঘের ফোনে ব্যাটারি ফুরিয়ে গেছে, তাই চার্জ নিচ্ছে!'",
            "বাবা: তুমি এত ফোন কিসের?\nছেলে: ব্যাটারি চার্জ দেখছি বাবা!",
            "ডাক্তার: আপনার বাচ্চা কি খায়?\nমা: স্যার, মোবাইল চার্জার!",
            "বন্ধু: তোমার নাক এত লম্বা কেন?\nআমি: গুগল ম্যাপে পিন মারতে!",
        ]
        return random.choice(jokes)

# ==================== VERCEL ROUTES ====================
@app.route('/')
def home():
    """Home page"""
    db.update_stats("total_requests")
    
    return jsonify({
        "status": "active",
        "message": "🤖 Smart Utility Bot API",
        "developer": "Ahamed Rahim (@al_rahim2)",
        "github": "https://github.com/ahamed-2",
        "channel": "@ahamed_068",
        "api_credits": "@Offline_669",
        "endpoints": {
            "/api/ai": "AI Chat - GET ?q=question",
            "/api/ask": "Multi AI - GET ?q=question",
            "/api/joke": "Get random joke",
            "/api/stream": "Streaming service - GET ?service=name&url=video_url",
            "/api/stats": "Bot statistics",
            "/api/status": "API status check"
        },
        "usage": "Use these endpoints for your applications"
    })

@app.route('/api/ai', methods=['GET'])
def ai_api():
    """AI API endpoint"""
    question = request.args.get('q', '').strip()
    
    if not question:
        return jsonify({
            "error": "Question parameter 'q' is required",
            "example": "/api/ai?q=বাংলাদেশের রাজধানী কোথায়?"
        }), 400
    
    db.update_stats("total_requests")
    db.update_stats("ai_queries")
    
    # Try Perplexity AI first
    result = APIHandler.perplex_ai(question)
    
    # If fails, try GPT-4
    if not result.get("success"):
        result = APIHandler.gpt4_ai(question)
    
    if result.get("success"):
        response = {
            "success": True,
            "question": question,
            "answer": result["answer"],
            "source": result.get("source", "AI"),
            "api_credits": result.get("api", "@Offline_669"),
            "developer": "@al_rahim2",
            "channel": "@ahamed_068",
            "formatted_response": Utility.format_response(
                result["answer"], 
                result.get("source", ""),
                result.get("api", "")
            )
        }
        return jsonify(response)
    else:
        return jsonify({
            "success": False,
            "error": result.get("error", "Unknown error"),
            "fallback_joke": Utility.get_joke(),
            "developer": "@al_rahim2"
        })

@app.route('/api/ask', methods=['GET'])
def ask_api():
    """Multi-AI API endpoint"""
    question = request.args.get('q', '').strip()
    
    if not question:
        return jsonify({
            "error": "Question parameter 'q' is required",
            "example": "/api/ask?q=পাইথন প্রোগ্রামিং শিখব কিভাবে?"
        }), 400
    
    db.update_stats("total_requests")
    db.update_stats("ai_queries")
    
    responses = []
    
    # Get response from Perplexity
    perplex_result = APIHandler.perplex_ai(question)
    if perplex_result.get("success"):
        responses.append({
            "source": "Perplexity AI",
            "answer": perplex_result["answer"][:500],
            "api": "@Offline_669"
        })
    
    # Get response from GPT-4
    gpt_result = APIHandler.gpt4_ai(question)
    if gpt_result.get("success"):
        responses.append({
            "source": "GPT-4 AI",
            "answer": gpt_result["answer"][:500],
            "api": "@Offline_669"
        })
    
    if responses:
        return jsonify({
            "success": True,
            "question": question,
            "responses": responses,
            "total_responses": len(responses),
            "developer": "@al_rahim2",
            "channel": "@ahamed_068",
            "api_credits": "@Offline_669"
        })
    else:
        return jsonify({
            "success": False,
            "error": "All AI services failed",
            "joke": Utility.get_joke(),
            "developer": "@al_rahim2"
        })

@app.route('/api/joke', methods=['GET'])
def joke_api():
    """Joke API endpoint"""
    db.update_stats("total_requests")
    
    joke = Utility.get_joke()
    
    return jsonify({
        "success": True,
        "joke": joke,
        "language": "Bengali",
        "formatted": f"😂 **জোক:**\n\n{joke}\n\n✨ আরও মজার জোকের জন্য আবার রিকোয়েস্ট করুন\n\n⚡ **Powered by @al_rahim2**\n📢 **Channel: @ahamed_068**",
        "developer": "@al_rahim2",
        "channel": "@ahamed_068"
    })

@app.route('/api/stream', methods=['GET'])
def stream_api():
    """Streaming service API"""
    service = request.args.get('service', '').strip()
    url = request.args.get('url', '').strip()
    
    if not service or not url:
        return jsonify({
            "error": "Both 'service' and 'url' parameters are required",
            "available_services": list(API_ENDPOINTS.keys()),
            "example": "/api/stream?service=netflix&url=https://netflix.com/watch/123"
        }), 400
    
    if service not in API_ENDPOINTS:
        return jsonify({
            "error": f"Service '{service}' not found",
            "available_services": list(API_ENDPOINTS.keys())
        }), 404
    
    db.update_stats("total_requests")
    db.update_stats("streaming_requests")
    
    result = APIHandler.stream_download(service, url)
    
    if result.get("success"):
        return jsonify({
            "success": True,
            "service": service,
            "url": url,
            "data": result["data"][:1000] + ("..." if len(result["data"]) > 1000 else ""),
            "data_length": len(result["data"]),
            "api_credits": result.get("api", "@al_rahim2"),
            "developer": "@al_rahim2",
            "channel": "@ahamed_068",
            "note": "This is streaming data. Use appropriate tools to process it."
        })
    else:
        return jsonify({
            "success": False,
            "service": service,
            "error": result.get("error", "Unknown error"),
            "developer": "@al_rahim2",
            "suggestion": "Check the URL or try another service"
        })

@app.route('/api/stats', methods=['GET'])
def stats_api():
    """Statistics API endpoint"""
    stats = db.get_stats()
    
    return jsonify({
        "success": True,
        "statistics": stats,
        "uptime": "24/7 (Vercel Hosted)",
        "developer": "@al_rahim2",
        "channel": "@ahamed_068",
        "github": "https://github.com/ahamed-2",
        "portfolio": "https://ahamed-rahim.pages.dev/",
        "formatted": f"""
📊 **বট স্ট্যাটিস্টিক্স**

👥 **টোটাল রিকোয়েস্ট:** {stats.get('total_requests', 0)}
🤖 **AI কোয়েরি:** {stats.get('ai_queries', 0)}
🔌 **API কল:** {stats.get('api_calls', 0)}
🎬 **স্ট্রিমিং রিকোয়েস্ট:** {stats.get('streaming_requests', 0)}
📅 **লাস্ট আপডেট:** {stats.get('last_updated', 'N/A')}

⚡ **Powered by @al_rahim2**
📢 **Channel: @ahamed_068**
🌐 **GitHub: https://github.com/ahamed-2**
        """
    })

@app.route('/api/status', methods=['GET'])
def status_api():
    """API status check"""
    status = APIHandler.check_api_status()
    
    working = sum(1 for s in status.values() if s)
    total = len(status)
    
    return jsonify({
        "success": True,
        "status": "operational",
        "apis_working": f"{working}/{total}",
        "details": status,
        "developer": "@al_rahim2",
        "channel": "@ahamed_068",
        "formatted": f"""
🔧 **API স্ট্যাটাস রিপোর্ট**

✅ **সক্রিয় API:** {working}/{total}

📡 **AI APIs:**
• Perplexity AI: {'✅' if status.get('perplex_ai') else '❌'}
• GPT-4 AI: {'✅' if status.get('gpt4_ai') else '❌'}
• Multi AI: {'✅' if status.get('multi_ai') else '❌'}

🎬 **স্ট্রিমিং APIs:**
• Prime Video: {'✅' if status.get('primevideo') else '❌'}
• Netflix: {'✅' if status.get('netflix') else '❌'}
• Spotify: {'✅' if status.get('spotify') else '❌'}
• Zee5: {'✅' if status.get('zee5') else '❌'}

⚡ **Powered by @al_rahim2**
🔌 **API Credits: @Offline_669**
📢 **Channel: @ahamed_068**
        """
    })

@app.route('/api/credits', methods=['GET'])
def credits_api():
    """Credits API"""
    return jsonify({
        "success": True,
        "developer": "Ahamed Rahim",
        "telegram": "@al_rahim2",
        "github": "https://github.com/ahamed-2",
        "portfolio": "https://ahamed-rahim.pages.dev/",
        "channel": "@ahamed_068",
        "api_credits": "@Offline_669",
        "streaming_api_credits": "@al_rahim2",
        "libraries": [
            "Flask - Web Framework",
            "Requests - HTTP Library",
            "Python 3.11+"
        ],
        "hosting": "Vercel",
        "version": "2.0.0",
        "release_date": "December 2024",
        "formatted": """
🤖 **Smart Utility Bot - Credits**

👨‍💻 **ডেভেলপার:**
• **Ahamed Rahim** (@al_rahim2)
• GitHub: https://github.com/ahamed-2
• Portfolio: https://ahamed-rahim.pages.dev/

🔌 **API প্রোভাইডার:**
• **@Offline_669** - AI APIs (Perplexity, GPT-4, Meta AI)
• **@al_rahim2** - Streaming Service APIs

📚 **লাইব্রেরি ক্রেডিট:**
• Flask - Web Framework
• Requests - HTTP Library
• Python 3.11+

🚀 **হোস্টিং:** Vercel
📅 **ভের্সন:** 2.0.0

⚡ **Powered by:** @al_rahim2
📢 **চ্যানেল:** @ahamed_068
        """
    })

@app.route('/api/utility/time', methods=['GET'])
def time_api():
    """World Time API"""
    import pytz
    from datetime import datetime
    
    city = request.args.get('city', 'Dhaka').strip()
    
    cities = {
        "dhaka": "Asia/Dhaka",
        "kolkata": "Asia/Kolkata",
        "delhi": "Asia/Kolkata",
        "london": "Europe/London",
        "newyork": "America/New_York",
        "tokyo": "Asia/Tokyo",
        "dubai": "Asia/Dubai",
        "singapore": "Asia/Singapore",
    }
    
    city_key = city.lower()
    if city_key not in cities:
        return jsonify({
            "error": f"City '{city}' not supported",
            "supported_cities": list(cities.keys())
        }), 404
    
    tz = pytz.timezone(cities[city_key])
    city_time = datetime.now(tz)
    
    return jsonify({
        "success": True,
        "city": city.capitalize(),
        "time": city_time.strftime("%Y-%m-%d %I:%M:%S %p"),
        "date": city_time.strftime("%A, %d %B %Y"),
        "timezone": str(tz),
        "developer": "@al_rahim2",
        "formatted": f"""
🕒 **{city.capitalize()} এর সময়**

📅 **তারিখ:** {city_time.strftime('%A, %d %B %Y')}
⏰ **সময়:** {city_time.strftime('%I:%M:%S %p')}
🌍 **টাইমজোন:** {tz}

⚡ **Powered by @al_rahim2**
📢 **Channel: @ahamed_068**
        """
    })

# ==================== ERROR HANDLERS ====================
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "available_endpoints": [
            "/api/ai",
            "/api/ask", 
            "/api/joke",
            "/api/stream",
            "/api/stats",
            "/api/status",
            "/api/credits",
            "/api/utility/time"
        ],
        "developer": "@al_rahim2"
    }), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "error": "Internal server error",
        "developer": "@al_rahim2",
        "contact": "t.me/al_rahim2"
    }), 500

# ==================== VERCEL SPECIFIC ====================
# This is required for Vercel to detect the app
if __name__ == "__main__":
    # For local testing
    app.run(debug=True, host='0.0.0.0', port=3000)
else:
    # For Vercel deployment
    handler = app
