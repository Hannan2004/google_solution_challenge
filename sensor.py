import asyncio
import csv
from joblib import load
import json
import random

# from sklearn.pipeline import Pipeline
import websockets

pipe = load("./ml/out/model.joblib")

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

TIME_STAMP = 1  # change this to whatever time in seconds you want
HISTORY_FILE = "./history.csv"

with open("./ml/sample.csv", "r") as csvfile:
    csvreader = csv.reader(csvfile)
    headers = next(csvreader)  # assuming the first row contains headers

    for row in csvreader:
        data.append([float(i) for i in row][:-1])

connected_clients = set({})
cats_real_data = []  # A list to store cats_real data

initial = 0
final = 1
T = 20
current = 0


def write_to_history(data):
    with open(HISTORY_FILE, mode="a") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)

    with open(HISTORY_FILE, mode="r") as readfile:
        existing_lines = list(csv.reader(readfile))
        if len(existing_lines) > 100:
            with open(HISTORY_FILE, mode="w", newline="") as writefile:
                writer = csv.writer(writefile)
                writer.writerows(existing_lines[1:])


def wobbly():
    return current + random.random() * 0.1 - 0.05


async def handle_connection(websocket):
    global data, initial, final, T, current, indices, connected_clients, cats_real_data

    try:
        connected_clients.add(websocket)
        while True:
            # asynchronously wait for both regular data sending and message checking
            await asyncio.gather(
                send_regular_data(websocket), check_messages(websocket)
            )

    except websockets.exceptions.ConnectionClosed:
        print("Connection closed")

    finally:
        connected_clients.remove(websocket)


async def send_regular_data(websocket):
    global data, initial, final, T, current, indices, cats_real_data

    data1 = data[initial]
    data2 = data[final]
    dataN = [
        data1[i] * wobbly() / T + data2[i] * (T - wobbly()) / T
        for i in range(len(indices.keys()))
    ]

    dataN.append(pipe.predict([dataN]).tolist()[0][0])

    await websocket.send(json.dumps(dataN))

    write_to_history(dataN)

    current += 1
    if current == T:
        current = 0
        final = initial
        initial = (initial + 1) % len(data)
    await asyncio.sleep(TIME_STAMP)


async def check_messages(websocket):
    try:
        await asyncio.wait_for(websocket.recv(), timeout=1)
        lines = []
        with open(HISTORY_FILE, mode="r") as csvfile:
            for row in csvfile:
                lines.append([float(i) for i in row.split(",")])

        await websocket.send(json.dumps(lines))

    except asyncio.TimeoutError:
        pass


async def check_clients():
    global connected_clients

    while True:
        for websocket in connected_clients.copy():
            try:
                # send a ping to check if the connection is still alive
                await asyncio.wait_for(websocket.ping(), timeout=1)
            except asyncio.TimeoutError:
                # if the ping times out, close the connection
                # headache
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
// sample use in JS (not making another file for this):

let socket = new WebSocket('127.0.0.1:4000');
socket.onmessage = ({ data }) => {
  // data is a stringified JSON array 
  console.log(JSON.parse(data));
}

// sample use in JS for getting history

let history = socket.send(0);
// `history` contains recent history now
"""
