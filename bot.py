import qrcode
from telethon import TelegramClient, events
import os
from dotenv import load_dotenv

# Load environment variables (for local testing)
load_dotenv()

# Get credentials from environment variables (safer than hardcoding)
api_id = int(os.getenv("API_ID")) 
api_hash = os.getenv("API_HASH")  
bot_token = os.getenv("BOT_TOKEN")

# Create the client and connect
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

#Hold the user for waiting to write text---
waiting_for_text = {}

#Start message for user----
@client.on(events.NewMessage(pattern=r'/(?i)start'))
async def start(event):
    #Extract sender id-----
    sender = await event.get_sender()
    user_id = sender.id
    
    #Store user_id in waiting_for_text dic.----
    waiting_for_text[user_id] = True
    
    welcome_message = (
        "🎉 Welcome to the QR Code Generator Bot! 📱\n\n"
        "I can help you create QR codes quickly and easily! Just use the command:\n\n"
        "📝 /text <Your Text Here>\n\n"
        "For example: /text Demo Text\n\n"
        "Let's get started! What would you like to convert into a QR code? 🤔"
    )
    await event.respond(welcome_message)
    raise events.StopPropagation

#Make text sender programm----
@client.on(events.NewMessage(pattern=r'/text (.+)'))
async def text_handler(event):
    #Extract sender id-----
    sender = await event.get_sender()
    user_id = sender.id

    #Check user_id is inside waiting_for_text or not---
    if user_id in waiting_for_text and waiting_for_text[user_id]:
        #get the text which is after commands like (/text)----
        user_text = event.pattern_match.group(1) 

         # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=8,
            border=2,
        )
        qr.add_data(user_text)
        qr.make(fit=True)

        # Create an image from the QR Code instance
        img = qr.make_image(fill_color="black", back_color="white")

        #Convert to RGB to remove transparency---
        img = img.convert('RGB')

        # Save the image to a file----
        img_path = f'{user_id}.png'
        img.save(img_path, format='PNG')

        try:
            # Send the QR code image back to the user----
            await event.respond("Here is your QR code! 📷", file=img_path)
            
            #Remove save file with os---
            os.remove(img_path)
        except Exception as e:
            await event.respond(f"An Error occored: {e}") 

# Start the bot-----
print("Bot is running...")
client.run_until_disconnected()