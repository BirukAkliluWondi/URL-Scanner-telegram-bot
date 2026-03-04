🚀 Odoo Error Bot
A powerful Telegram bot for managing and searching Odoo error solutions with OCR support. Built with Python, this bot helps Odoo developers and users quickly find solutions to common errors and contribute their own fixes to the community database.

✨ Features
📝 Error Management
Add Solutions: Post new error solutions with detailed descriptions

Text Mode: Manually type error messages, descriptions, and solutions

Image Mode: Upload screenshots - OCR automatically extracts error text

Search Database: Find solutions using keywords or natural language

Recent Solutions: View the latest 5 solutions added to the database

🖼️ OCR Capabilities
Automatic Text Extraction: Extracts text from error screenshots

Multiple OCR Configurations: Tries different recognition modes for accuracy

Image Enhancement: Auto-resizes and enhances images for better text detection

Smart Search: Uses OCR text to automatically search for matching solutions

👥 User Features
Persistent Storage: Remembers users even after clearing chat history

User Statistics: Tracks contributions and activity

Personal History: View your own posted solutions

Quick Actions: Inline keyboards for faster navigation

📊 Database
SQLite Storage: Lightweight, portable database

Structured Data: Stores error messages, descriptions, and solutions

Timestamp Tracking: Records when solutions are added

Full-Text Search: Case-insensitive search across all fields

🛠️ Commands
Command	Description	Example
/start	Welcome message and bot status	/start
/post	Add a new error solution	/post
/search <keyword>	Search for solutions	/search database error
/recent	Show latest 5 solutions	/recent
/myposts	View your contributions	/myposts
/stats	Bot statistics	/stats
/help	Show help guide	/help
/cancel	Cancel current operation	/cancel
📦 Installation
Prerequisites
Python 3.8 or higher

Tesseract OCR (for image processing)

Telegram Bot Token (from @BotFather)

Step 1: Clone the Repository
bash
git clone https://github.com/yourusername/odoo-error-bot.git
cd odoo-error-bot
Step 2: Install Tesseract OCR
Windows:

Download from: GitHub UB-Mannheim/tesseract

Install to: C:\Program Files\Tesseract-OCR\

Add to PATH or update path in code

Linux (Ubuntu/Debian):

bash
sudo apt update
sudo apt install tesseract-ocr
Linux (CentOS/RHEL):

bash
sudo yum install epel-release
sudo yum install tesseract
macOS:

bash
brew install tesseract
Step 3: Install Python Dependencies
bash
pip install -r requirements.txt
Or install manually:

bash
pip install python-telegram-bot Pillow pytesseract
Step 4: Configure the Bot
Edit bot.py and update the bot token:

python
BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'  # Get from @BotFather
Step 5: Run the Bot
bash
python bot.py
