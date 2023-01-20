import os
from dotenv import load_dotenv
load_dotenv()

token = os.getenv('channel_id')
print(token)
