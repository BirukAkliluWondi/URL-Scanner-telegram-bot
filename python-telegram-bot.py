import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import time
import urllib.parse
from telegram import BotCommand
async def set_commands(application: Application):
    """Register bot commands menu in Telegram"""
    commands = [
        BotCommand("start", "Get welcome message and instructions"),
        BotCommand("scan", "Scan a URL - usage: /scan https://example.com"),
        BotCommand("help", "Show all available commands"),
        BotCommand("privacy", "View the bot's privacy policy"),
        BotCommand("stats", "Get bot usage statistics")
    ]
    await application.bot.set_my_commands(commands)

# Add to your main() function before run_polling():

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
TOKEN = "YOUR_TELEGRAM_BOT_API"
VT_API_KEY = "YOUR_API_KEY_FROM_VIRUSTOTAL"  # Get from https://www.virustotal.com/

# Track ongoing scans
ongoing_scans = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\! I can scan URLs for malware\. '
        'Just send me a URL and I\'ll check it for malicious content\.'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a help message when the command /help is issued."""
    help_text = """
    *Bot Commands:*
    /start - Start the bot
    /help - Show this help message
    /scan <url> - Scan a URL for malware

    *How to use:*
    Just send me a URL and I'll scan it for malware automatically.
    Example: `https://example.com`
    """
    await update.message.reply_markdown(help_text)

async def scan_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /scan command with a URL."""
    if not context.args:
        await update.message.reply_text("Please provide a URL to scan. Example: /scan https://example.com")
        return

    url = context.args[0]
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    await process_url_scan(update, url)

async def handle_url_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle URLs sent directly in messages."""
    # Extract URL from message
    url = update.message.text.strip()

    # Basic URL validation
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    await process_url_scan(update, url)

async def process_url_scan(update: Update, url: str):
    """Process URL scanning workflow."""
    try:
        # First check if URL has been scanned recently
        url_id = get_vt_url_id(url)
        report = await get_existing_report(url_id)

        if report:
            await display_results(update, report, url)
            return

        # If no recent scan, submit for analysis
        await update.message.reply_text(f"🔄 Submitting URL for scanning: {url}")
        analysis_id = await submit_url_for_scan(url)

        if not analysis_id:
            await update.message.reply_text("❌ Failed to submit URL for scanning. Please try again later.")
            return

        # Wait and then get the report
        await update.message.reply_text("⏳ Waiting for scan results (this may take 10-20 seconds)...")
        time.sleep(15)  # Wait for VirusTotal to process

        report = await get_scan_report(analysis_id)
        if report:
            await display_results(update, report, url)
        else:
            await update.message.reply_text("❌ Could not retrieve scan results. The URL may still be processing.")

    except Exception as e:
        logger.error(f"Error in URL scanning: {str(e)}")
        await update.message.reply_text("❌ An error occurred during the scanning process. Please try again.")

def get_vt_url_id(url: str) -> str:
    """Generate VirusTotal URL ID (base64 encoded URL without padding)"""
    import base64
    url_bytes = url.encode('ascii')
    base64_bytes = base64.urlsafe_b64encode(url_bytes)
    base64_string = base64_bytes.decode('ascii').strip('=')
    return base64_string

async def get_existing_report(url_id: str):
    """Check for existing scan report"""
    headers = {"x-apikey": VT_API_KEY}
    try:
        response = requests.get(
            f"https://www.virustotal.com/api/v3/urls/{url_id}",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        return None
    except requests.RequestException:
        return None

async def submit_url_for_scan(url: str):
    """Submit URL to VirusTotal for scanning"""
    headers = {
        "x-apikey": VT_API_KEY,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        response = requests.post(
            "https://www.virustotal.com/api/v3/urls",
            headers=headers,
            data=f"url={urllib.parse.quote(url)}",
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get('data', {}).get('id')
        logger.error(f"Submission failed: {response.status_code} - {response.text}")
        return None
    except requests.RequestException as e:
        logger.error(f"Submission error: {str(e)}")
        return None

async def get_scan_report(analysis_id: str):
    """Retrieve scan report from VirusTotal"""
    headers = {"x-apikey": VT_API_KEY}
    try:
        response = requests.get(
            f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        logger.error(f"Report fetch failed: {response.status_code} - {response.text}")
        return None
    except requests.RequestException as e:
        logger.error(f"Report error: {str(e)}")
        return None

async def display_results(update: Update, report: dict, original_url: str):
    """Display formatted results to user"""
    try:
        # Extract data from the report
        if 'data' in report and 'attributes' in report['data']:
            attributes = report['data']['attributes']

            # Get stats - handle both URL report and analysis report formats
            if 'stats' in attributes:
                stats = attributes['stats']
            elif 'last_analysis_stats' in attributes:
                stats = attributes['last_analysis_stats']
            else:
                raise ValueError("No stats found in report")

            malicious = stats.get('malicious', 0)
            suspicious = stats.get('suspicious', 0)
            harmless = stats.get('harmless', 0)
            undetected = stats.get('undetected', 0)
            total = malicious + suspicious + harmless + undetected

            # Determine result status
            if malicious > 0:
                result_emoji = "🔴"
                conclusion = f"{malicious} security vendors flagged this as malicious"
            elif suspicious > 0:
                result_emoji = "🟠"
                conclusion = f"{suspicious} vendors flagged this as suspicious"
            else:
                result_emoji = "🟢"
                conclusion = "No vendors flagged this as malicious"

            # Get the URL ID for the detailed report link
            url_id = attributes.get('url_id', get_vt_url_id(original_url))

            # Format the message
            message = (
                f"{result_emoji} *Scan Results for:* {original_url}\n\n"
                f"*Security Vendors:* {total}\n"
                f"*Malicious:* {malicious}\n"
                f"*Suspicious:* {suspicious}\n"
                f"*Harmless:* {harmless}\n"
                f"*Undetected:* {undetected}\n\n"
                f"*Conclusion:* {conclusion}\n\n"
                f"*Detailed Report:* https://www.virustotal.com/gui/url/{url_id}"
            )

            await update.message.reply_markdown(message)
        else:
            await update.message.reply_text("❌ Could not parse scan results.")

    except Exception as e:
        logger.error(f"Error displaying results: {str(e)}")
        await update.message.reply_text("❌ An error occurred while processing the scan results.")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Log errors and notify the user."""
    logger.error(f"Update {update} caused error {context.error}")
    if update and hasattr(update, 'message'):
        await update.message.reply_text("❌ An error occurred. Please try again.")

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("scan", scan_url))

    # Handle URLs sent directly in messages
    application.add_handler(MessageHandler(filters.Entity("url"), handle_url_message))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url_message))

    # Register error handler
    application.add_error_handler(error_handler)

    # Run the bot until the user presses Ctrl-C
    logger.info("Bot is running...")
    application.run_polling()
# Add these two new functions (keep all existing code)
async def privacy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /privacy command"""
    await update.message.reply_text(
        "🔒 Privacy Policy:\n"
        "• URLs are temporarily sent to VirusTotal for scanning\n"
        "• No personal data is collected or stored\n"
        "• Scan results are not saved after delivery"
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command"""
    await update.message.reply_text(
        "📊 Bot Statistics:\n"
        f"Total scans processed: {len(ongoing_scans)}\n"
        "Last scan: Just now"  # You can add real stats here
    )

# Then modify your main() function to add the new handlers:
def main():
    """Start the bot."""
    # Create the Application with command registration
    application = Application.builder().token(TOKEN).post_init(set_commands).build()

    # Register command handlers (ADD THE NEW ONES HERE)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("scan", scan_url))
    application.add_handler(CommandHandler("privacy", privacy))  # New
    application.add_handler(CommandHandler("stats", stats))      # New

    # Keep all existing handlers
    application.add_handler(MessageHandler(filters.Entity("url"), handle_url_message))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url_message))
    application.add_error_handler(error_handler)

    logger.info("Bot is running with full command support...")
    application.run_polling()
if __name__ == '__main__':
    main()
