import websockets
import asyncio
import json
import platform

class WebsocketManager:
    def __init__(self, data):
        self.token = data.token
        
        self.activity = None
        self.activityType = None
        pass

    async def connect(self):
        self.connection = await websockets.connect('wss://gateway.discord.gg')
        if self.connection.open:
            print('Connection stablished. Client correctly connected')
            
            self.identify = {
                'op': 2,
                'd': {
                    'token': self.token,
                    'intents': 513,
                    'properties': {
                        '$os': str(platform.system()).lower(),
                        '$browser': 'gydo.py',
                        '$device': 'gydo.py'
                    },
                    'presence': {
                        'activities': [{
                            'name': self.activity,
                            'type': self.activityType
                        }],
                    },
                }
            }
        
            await self.sendMessage(json.dumps(self.identify))
            return self.connection


    async def sendMessage(self, message):
        await self.connection.send(message)

    async def receiveMessage(self, connection):
        while True:
            try:
                message = await connection.recv()
                print('Discord Websocket:\n ' + str(message))

            except websockets.exceptions.ConnectionClosed:
                print('Connection with Discord Websocket closed')
                break
            
    async def heartbeat(self, connection):
        while True:
            try:
                await connection.send(json.dumps({"op":1,'d':2}))
                await asyncio.sleep(4.1250)
            except websockets.exceptions.ConnectionClosed:
                print('Connection with Discord Websocket closed')
                break
            
    async def presence(self, data, type):
        self.activity = data
        self.activityType = type