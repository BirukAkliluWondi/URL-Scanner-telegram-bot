 URL Security Scanner Bot
A powerful Telegram bot that scans URLs for malware and security threats using the VirusTotal API. Get instant security analysis for any URL directly in your Telegram chat.

✨ Features
🛡️ URL Scanning
Instant Analysis: Scan any URL for malware, phishing, and security threats

Multi-Engine Scanning: Uses 70+ antivirus engines and URL scanners

Detailed Reports: Get comprehensive results with vendor breakdowns

Historical Data: Checks if URLs have been scanned before

🤖 Bot Commands
Command	Description	Example
/start	Welcome message and bot introduction	/start
/help	Show all available commands and usage	/help
/scan <url>	Scan a specific URL	/scan https://example.com
/privacy	View privacy policy	/privacy
/stats	Get bot usage statistics	/stats
📊 Scan Results
The bot provides comprehensive scan results including:

✅ Security vendors count - Total engines that scanned the URL

🔴 Malicious detections - Number of engines flagging as malicious

🟠 Suspicious detections - Number of suspicious flags

🟢 Harmless verdicts - Engines finding no threats

⚪ Undetected - Engines that didn't detect anything

🔗 Detailed Report - Direct link to full VirusTotal analysis

🎯 Key Features
Auto-Detection: Automatically detects URLs in any message

Smart Processing: Checks for existing reports before rescanning

Command Menu: Full Telegram bot command interface

Error Handling: Graceful error management with user notifications

Privacy Focused: No storage of personal data or scan history

🛠️ Installation
Prerequisites
Python 3.8 or higher

Telegram Bot Token (from @BotFather)

VirusTotal API Key (free tier available)

Step 1: Clone the Repository
bash
git clone https://github.com/yourusername/url-security-bot.git
cd url-security-bot
Step 2: Install Dependencies
bash
pip install -r requirements.txt
Or install manually:

bash
pip install python-telegram-bot requests
Step 3: Get API Keys
Telegram Bot Token:

Open Telegram and search for @BotFather

Send /newbot and follow instructions

Copy the bot token

VirusTotal API Key:

Sign up at VirusTotal

Go to your profile and get your API key

Free tier allows up to 4 requests per minute

Step 4: Configure the Bot
Edit bot.py and update the configuration:

python
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
VT_API_KEY = "YOUR_VIRUSTOTAL_API_KEY_HERE"
Step 5: Run the Bot
bash
python bot.py
📁 Project Structure
text
url-security-bot/
├── bot.py            
