import requests
from pytgcalls import idle
from KennedyMusic.callsmusic import run
from pyrogram import Client as Bot
from KennedyMusic.config import API_HASH, API_ID, BG_IMAGE, BOT_TOKEN


response = requests.get(BG_IMAGE)
with open("./etc/foreground.png", "wb") as file:
    file.write(response.content)




import asyncio
from pyrogram import Client, ClientSession
from pymongo import MongoClient
import config  # You may need to adjust the import for your configuration

# Initialize database
def initialize_database():
    global database
    database = {}

# Connect to MongoDB
def connect_to_mongodb():
    global db
    mongo_client = MongoClient(MONGO_DB_URI)
    db = mongo_client.wbb

# Load sudoers
async def load_sudoers():
    global sudoers
    print("[INFO]: Loading Sudo Users")
    sudoers_db = db.sudoers
    sudoers_data = await sudoers_db.find_one({"sudo": "sudo"})
    sudoers_data = [] if not sudoers_data else sudoers_data["sudoers"]
    
    for user_id in sudoers:
        if user_id not in sudoers_data:
            sudoers_data.append(user_id)
            await sudoers_db.update_one(
                {"sudo": "sudo"}, {"$set": {"sudoers": sudoers_data}}, upsert=True
            )
    
    sudoers = (sudoers + sudoers_data) if sudoers_data else sudoers
    print("[INFO]: Loaded Sudo Users")

# Initialize event loop and load sudoers
def initialize_event_loop():
    global loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(load_sudoers())

# Initialize Bot Client
def initialize_bot_client():
    print("[INFO]: Initializing Bot Client")
    app = Client(
        'Dragonz',
        API_ID,
        API_HASH,
        bot_token=BOT_TOKEN,
    )
    aiohttp_session = ClientSession()

# Initialize Assistant Client
def initialize_assistant_client():
    client = Client(config.SESSION_NAME, config.API_ID, config.API_HASH)

# Retrieve Bot and Assistant information
def retrieve_bot_and_assistant_info(app, client):
    global BOT_ID, BOT_NAME, BOT_USERNAME
    global ASSISTANT_ID, ASSISTANT_NAME, ASSISTANT_USERNAME, ASSISTANT_MENTION
    
    bot_info = app.get_me()
    assistant_info = client.get_me()
    
    BOT_ID = bot_info.id
    ASSISTIANT_ID = assistant_info.id
    
    if bot_info.last_name:
        BOT_NAME = bot_info.first_name + " " + bot_info.last_name
    else:
        BOT_NAME = bot_info.first_name
    BOT_USERNAME = bot_info.username
    
    ASSISTANT_NAME = (
        f"{assistant_info.first_name} {assistant_info.last_name}"
        if assistant_info.last_name
        else assistant_info.first_name
    )
    ASSITANT_USERNAME = assistant_info.username
    ASSISTANT_MENTION = assistant_info.mention

# Start Bot Client
def start_bot_client(app):
    print("[INFO]: Starting Bot Client")
    app.start()

# Start Assistant Client
def start_assistant_client(client):
    print("[INFO]: Starting Assistant Client")
    client.start()

# Load Bot and Assistant Profile Info
def load_bot_and_assistant_info(app, client):
    print("[INFO]: Loading Bot/Assistant Profile Info")
    retrieve_bot_and_assistant_info(app, client)
    print("[INFO]: Loaded Bot/Assistant Profile Info")
