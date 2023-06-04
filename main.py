import os
import poe
import logging

from fbchat import Client
from fbchat.models import *
from dotenv import load_dotenv


load_dotenv()
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
TOKEN = os.getenv('TOKEN')
BOT_NAME = os.getenv('BOT_NAME')


class MessengerGPT(Client):
    poe.logger.setLevel(logging.WARNING)
    poe_api = poe.Client(TOKEN)

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        if author_id != self.uid: 
            text = ''
            
            if message_object.text.startswith('/chat'):
                self.setTypingStatus(TypingStatus.TYPING, thread_id=thread_id, thread_type=thread_type)
                message = message_object.text[5:].strip()
                
                for chunk in MessengerGPT.poe_api.send_message(BOT_NAME, message): 
                    pass # Non-Streamed Sending
                text = chunk['text']
                
            elif message_object.text.startswith('/clear'):
                MessengerGPT.poe_api.send_chat_break(BOT_NAME)
                text = 'Context cleared'
                
            if text != '':
                self.send(Message(text), thread_id=thread_id, thread_type=thread_type)


if __name__ == "__main__":
    client = MessengerGPT(EMAIL, PASSWORD)
    client.listen()       
                