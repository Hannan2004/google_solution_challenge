import asyncio
import csv
import json
import random
import websockets

indices = {
    "Iron": 0,
    "Nitrate": 1,
    "Chloride": 2,
    "Lead": 3,
    "Zinc": 4,
    "Color": 5,
    "Turbidity": 6,
    "Fluoride": 7,
    "Copper": 8,
    "Odor": 9,
    "Sulfate": 10,
    "Chlorine": 11,
    "Manganese": 12,
    "Total Dissolved Solids": 13,
    "Water Temperature": 14,
    "Air Temperature": 15,
}

data = []

with open("./sample.csv", "r") as csvfile:
    csvreader = csv.reader(csvfile)
    headers = next(csvreader)  # assuming the first row contains headers

    for row in csvreader:
        data.append([float(i) for i in row][:-1])

connected_clients = set({})

initial = 0
final = 1
T = 20
current = 0


def wobbly():
    return current + random.random() * 0.1 - 0.05


async def handle_connection(websocket):
    global data, initial, final, T, current, indices, connected_clients

    try:
        connected_clients.add(websocket)
        while True:
            # wait for a message from the client
            data1 = data[initial]
            data2 = data[final]
            dataN = [
                data1[i] * wobbly() / T + data2[i] * (T - wobbly()) / T
                for i in range(len(indices.keys()))
            ]
            await websocket.send(json.dumps(dataN))
            current += 1
            if current == T:
                current = 0
                final = initial
                initial = (initial + 1) % len(data)
            await asyncio.sleep(1)

    except websockets.exceptions.ConnectionClosed:
        print("Connection closed")

    finally:
        connected_clients.remove(websocket)


async def check_clients():
    global connected_clients

    while True:
        for websocket in connected_clients.copy():
            try:
                # send a ping to check if the connection is still alive
                await asyncio.wait_for(websocket.ping(), timeout=1)
            except asyncio.TimeoutError:
                # if the ping times out, close the connection
                print("closing connection due to timeout")
                await websocket.close()
                connected_clients.remove(websocket)

        await asyncio.sleep(20)


server_address = "127.0.0.1"
server_port = 4000

start_server = websockets.serve(handle_connection, server_address, server_port)

print(f"socket started at ws://{server_address}:{server_port}")

# run the event loop
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_until_complete(check_clients())
asyncio.get_event_loop().run_forever()

"""
sample use in JS (not making another file for this):

let socket = new WebSocket('127.0.0.1:4000');
socket.onmessage = ({ data }) => {
  // data is a stringified JSON array 
  console.log(JSON.parse(data));
}
"""
