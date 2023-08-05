from gydo.restapi import RESTManager
from gydo.WebsocketManager import WebsocketManager
import json
from gydo.ClientUser import ClientUser
import asyncio

APIEndpoint = 'https://discord.com/api/v8'

class Client:
    def __init__(self, token):
        self.token = token;
        self.endpoint = APIEndpoint
        self.manage = RESTManager(self.token, APIEndpoint)
        
        r = self.manage.RESTGetCurrentUser(self.token, APIEndpoint)
    
        self.ws = WebsocketManager(self)
        
        loop = asyncio.get_event_loop()

        connection = loop.run_until_complete(self.ws.connect())
        
        tasks = [
            asyncio.ensure_future(self.ws.heartbeat(connection)),
            asyncio.ensure_future(self.ws.receiveMessage(connection)),
        ]
    
        loop.run_until_complete(asyncio.wait(tasks))
        
        self.data = json.loads(r.text)
        
        self.user = ClientUser(self)
    
    def sendMessage(self, message, channelId, *embed):
        self.messageJSON = {
            'content': f'{message}',
            'embeds': []
        }
        
        r = self.manage.RESTPostMessage(self.token, APIEndpoint, channelId, self.messageJSON)
        
    def MessageEmbed(self, title, description):
        self.MessageEmbedJSON = {
            'title': title,
            'description': description
        }
        
        return self.MessageEmbedJSON
    
    def setActivity(self, name, type): 
        self.ws.presence(name, type)