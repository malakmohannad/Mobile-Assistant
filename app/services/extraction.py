import json
import os
from openai import OpenAI
from pydantic import ValidationError
from app.schema.device import Device
from app.prompts.templates import SYSTEM_PROMPT, build_user_message, build_retry_message

def extract_device(text:str)->Device:
    client=OpenAI()
    messagess=[
        {"role":"system","content": SYSTEM_PROMPT},
        {"role":"user","content": build_user_message(text)},
    ]
    max_retries=2
    for attempt in range (max_retries+1):
        response=client.chat.completions.create(
            model=os.environ.get("MODEL_NAME","gpt-4o-mini"),
            messages=messagess,
            response_format={"type":"json_object"},
        )
        raw=response.choices[0].message.content
        try:
            data=json.loads(raw)
            device=Device.model_validate(data)
            return device
        except (json.JSONDecodeError, ValidationError) as e:
            if attempt==max_retries:
                raise ValueError(f"Failed to extract device information after {max_retries+1} attempts. Last error: {e}")
            else:
                messagess.append({"role":"assistant","content":raw})
                messagess.append({"role":"user","content":build_retry_message(str(e))})

