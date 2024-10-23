import asyncio
import websockets
import random

# Server handler function
async def echo(websocket, path):
    async for message in websocket:
        # Append a random number to the incoming message
        random_number = random.randint(1, 1000)
        modified_message = f"{message} {random_number}"
        
        # Send the modified message back to the client
        await websocket.send(modified_message)

# Start the server
start_server = websockets.serve(echo, "localhost", 8765)

# Run the server until manually stopped
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
