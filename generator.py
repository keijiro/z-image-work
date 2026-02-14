import requests
import time
import json
import re
import os
from pathlib import Path
from PIL import Image
from io import BytesIO

image_count = 30
file_prefix = "result_"

prompt = '''A realistic black-and-white photograph of a single rose placed on
an old wooden table. The aged wood surface shows scratches, grain, and signs of
wear. High contrast, fine texture detail, natural lighting, minimalist still
life.'''

base_url = 'https://api-inference.modelscope.ai/'
api_key = os.getenv("MODELSCOPE_API_KEY")
if not api_key:
    raise RuntimeError("MODELSCOPE_API_KEY is not set.")

common_headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

pattern = re.compile(rf"^{re.escape(file_prefix)}(\d+)\.jpg$")

def find_next_available_number():
    used_numbers = set()
    for path in Path(".").glob(f"{file_prefix}*.jpg"):
        match = pattern.match(path.name)
        if match:
            used_numbers.add(int(match.group(1)))

    number = 0
    while number in used_numbers:
        number += 1
    return number

for index in range(image_count):
    print(f"[{index + 1}/{image_count}] Generating...")

    try:
        response = requests.post(
            f"{base_url}v1/images/generations",
            headers={**common_headers, "X-ModelScope-Async-Mode": "true"},
            data=json.dumps({
                "model": "Tongyi-MAI/Z-Image-Turbo", # ModelScope Model-Id, required
                "size": "1440x810",
                "steps": 6,
                "prompt": prompt
            }, ensure_ascii=False).encode('utf-8')
        )
        response.raise_for_status()
        task_id = response.json()["task_id"]

        while True:
            result = requests.get(
                f"{base_url}v1/tasks/{task_id}",
                headers={**common_headers, "X-ModelScope-Task-Type": "image_generation"},
            )
            result.raise_for_status()
            data = result.json()

            if data["task_status"] == "SUCCEED":
                file_number = find_next_available_number()
                output_path = f"{file_prefix}{file_number:03d}.jpg"
                image = Image.open(BytesIO(requests.get(data["output_images"][0]).content))
                image.save(output_path)
                print(f"[{index + 1}/{image_count}] Saved: {output_path}")
                break
            elif data["task_status"] == "FAILED":
                print(f"[{index + 1}/{image_count}] Failed.")
                break

            time.sleep(5)
    except requests.RequestException as e:
        print(f"[{index + 1}/{image_count}] Request error: {e}")
