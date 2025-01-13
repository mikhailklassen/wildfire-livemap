from fastapi import FastAPI, WebSocket
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import json
import asyncio
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

origins = [
    "http://localhost:5173",
    # Add more origins here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# FIRMS API Configuration
API_KEY = "b3b38f287a8ba9db57fac29012ed1e9c"
FIRMS_URL = f"https://firms.modaps.eosdis.nasa.gov/api/country/csv/{API_KEY}/VIIRS_NOAA21_NRT/USA/1"


last_data = pd.DataFrame()
clients = []  # List of active WebSocket connections

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Fetch FIRMS data periodically
def fetch_and_notify_firms_data():
    global last_data

    try:
        # Fetch FIRMS data
        df=pd.read_csv(FIRMS_URL)
        print(df.tail())
        current_data = df

        # Detect new data
        if not current_data.equals(last_data):
            print(f"New data detected at {datetime.now()}")
            last_data=current_data #update global last_data
            asyncio.run(notify_clients(current_data))

    except Exception as e:
        print(f"Error fetching FIRMS data: {e}")

# Notify all WebSocket clients
async def notify_clients(new_data):
    message = {"event": "new_data", "data": new_data.to_json(orient="records")}
    for client in clients:
        try:
            await client.send_text(json.dumps(message))
        except Exception as e:
            print(f"Error notifying client: {e}")
            clients.remove(client)  # Remove disconnected clients

# WebSocket Endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    print("New WebSocket client connected")

    try:
        while True:
            # Keep the WebSocket connection alive
            await websocket.receive_text()
    except Exception as e:
        print(f"WebSocket connection closed: {e}")
    finally:
        clients.remove(websocket)
        print("WebSocket client disconnected")

# Schedule the periodic task
@app.on_event("startup")
def startup_event():
    scheduler.add_job(fetch_and_notify_firms_data, "interval", minutes=1)

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

@app.get("/")
def root():
    return {"message": "FIRMS data monitoring service with WebSocket is running"}
