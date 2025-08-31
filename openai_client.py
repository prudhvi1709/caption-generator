import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("LLMFOUNDRY_API_KEY")
if not API_KEY:
    raise ValueError("LLMFOUNDRY_API_KEY is not set in environment variables.")

url = "https://llmfoundry.straive.com/openai/v1/chat/completions"

def call_openai(raw_subtiles):
    headers = {
        "Authorization": f"Bearer {API_KEY}:caption-generator",
        "Content-Type": "application/json",
    }

    system_prompt = f"""
You are a professional subtitle corrector.

Input: raw subtitles (may have wrong indices, grammar, stacked sound effects, or malformed timestamps).  
Output: only corrected subtitles file.

Rules (strictly follow):

1. Indices must be sequential from 1.
2. Timestamps must be in the format: HH:MM:SS,mmm --> HH:MM:SS,mmm
   - Always 2 digits HH, MM, SS; 3 digits mmm.
   - Fix **malformed timestamps only**:
     - Missing leading zeros (e.g., 1:04:881 → 00:01:04,881)
     - Extra or missing digits in milliseconds (e.g., 3921 → 392)
   - **Never invent or guess timestamps**, do not shift subtitles.
3. Keep exactly one blank line between subtitle blocks.
4. Correct grammar, punctuation, and capitalization while preserving meaning.
5. Limit lines to ~42 characters, max 2 lines per subtitle block.
6. If multiple sound effects appear in one block, separate each SFX on its own line.
7. Before finalizing, ensure:
   - Indices are sequential
   - No overlapping timestamps
   - Proper formatting
8. Output **only** the corrected subtitles content. No ```srt ```. No explanations, no extra text.
9. Never miss the sound effects. Always have them, should be understandable and felt by deaf persons as well!

Example:

Raw:
22
01:04:881 --> 01:05:431
[LASERS FIRING]

Corrected:
22
00:01:04,881 --> 00:01:05,431
[LASERS FIRING]
"""
    
    user_prompt = f"""
Fix these raw subtitles...

Raw Subtitles:
{raw_subtiles}
"""

    payload = {
        "model": "gpt-4.1-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    return data["choices"][0]["message"]["content"]