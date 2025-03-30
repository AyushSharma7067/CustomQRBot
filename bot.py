import qrcode
import os
import telebot

# Initialize the bot with your token
bot = telebot.TeleBot("8033279511:AAGSFNHHDrmvi8l9o_lmIIAbqs2Grc9C_qo")

# Hold the user for waiting to write text
waiting_for_text = {}

# Start message for user
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    # Store user_id in waiting_for_text dict
    waiting_for_text[user_id] = True
    
    welcome_message = (
        "🎉 Welcome to the QR Code Generator Bot! 📱\n\n"
        "I can help you create QR codes quickly and easily! Just use the command:\n\n"
        "📝 /text <Your Text Here>\n\n"
        "For example: /text Demo Text\n\n"
        "Let's get started! What would you like to convert into a QR code? 🤔"
    )
    bot.reply_to(message, welcome_message)

# Text handler
@bot.message_handler(commands=['text'])
def handle_text(message):
    user_id = message.from_user.id

    # Check if user is in waiting_for_text
    if user_id in waiting_for_text and waiting_for_text[user_id]:
        # Get the text after the command
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Please provide some text after the /text command.")
            return
            
        user_text = ' '.join(message.text.split()[1:])

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

        # Convert to RGB to remove transparency
        img = img.convert('RGB')

        # Save the image to a file
        img_path = f'{user_id}.png'
        img.save(img_path, format='PNG')

        try:
            # Send the QR code image back to the user
            with open(img_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption="Here is your QR code! 📷")
            
            # Remove saved file
            os.remove(img_path)
        except Exception as e:
            bot.reply_to(message, f"An error occurred: {e}")

# Start the bot
print("Bot is running...")
bot.polling()
