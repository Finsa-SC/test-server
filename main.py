from fastapi import FastAPI, Request
from pydantic import BaseModel
from datetime import datetime
import json
import os

app = FastAPI()

chatlog_path = "chat_log.json"

class Message(BaseModel):
    input: str
    output: str

@app.post("/log")
async def log_message(msg: Message):
    log = {
        "input": msg.input,
        "output": msg.output,
        "timestamp": datetime.now().isoformat()
    }

    if not os.path.exists(chatlog_path):
        with open(chatlog_path, "w") as f:
            json.dump({"conversations": [log]}, f, indent=2)
    else:
        with open(chatlog_path, "r+") as f:
            data = json.load(f)
            data["conversations"].append(log)
            f.seek(0)
            json.dump(data, f, indent=2)

    return {"status": "logged"}
