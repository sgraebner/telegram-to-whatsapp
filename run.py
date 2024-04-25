import logging
from telethon import TelegramClient, events
from dotenv import load_dotenv
import os
import requests
import uuid
import time

# Load environment variables from the .env file located at ~/telegram_bot/.env
load_dotenv(dotenv_path=os.path.expanduser('~/telegram_bot/.env'))

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
whapi_api_key = os.getenv('WHAPI_API_KEY')
whatsapp_recipient = os.getenv('WHATSAPP_RECIPIENT')
channel_usernames = os.getenv('CHANNEL_USERNAMES').split(',')
debug_mode = os.getenv('DEBUG') == 'True'
local_image_path = os.getenv('LOCAL_IMAGE_PATH')
public_image_url = os.getenv('PUBLIC_IMAGE_URL')

# Logging configuration
logging.basicConfig(level=logging.DEBUG if debug_mode else logging.INFO)

# Initialize the Telegram client
client = TelegramClient('session', api_id, api_hash)

def save_image_locally(image_bytes):
    """Saves the image locally and returns the path and filename."""
    image_name = f"{uuid.uuid4()}.jpg"
    local_file_path = os.path.join(local_image_path, image_name)
    with open(local_file_path, 'wb') as file:
        file.write(image_bytes)
    return local_file_path, image_name

def send_to_whatsapp(message, image_url):
    """Sends a message with an image to WhatsApp via the API."""
    headers = {
        'Authorization': f'Bearer {whapi_api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        'media': image_url,
        'to': whatsapp_recipient,
        'caption': message
    }
    response = requests.post('https://gate.whapi.cloud/messages/image', json=payload, headers=headers)

    if response.status_code in [200, 201]:
        logging.info('Message successfully sent to WhatsApp.')
    else:
        logging.error(f'Failed to send message. Response code: {response.status_code}')

@client.on(events.NewMessage(chats=channel_usernames))
async def handler(event):
    """Responds to new messages in specified Telegram channels."""
    if event.photo:
        message_content = event.message.message
        photo_bytes = await client.download_media(event.message.photo, file=bytes)
        
        local_file_path, image_name = save_image_locally(photo_bytes)
        full_public_url = os.path.join(public_image_url, image_name)
        
        send_to_whatsapp(message_content, full_public_url)
        
        time.sleep(10)  # Waits 10 seconds before deleting the local file
        os.remove(local_file_path)  # Deletes the local file

client.start()
client.run_until_disconnected()
