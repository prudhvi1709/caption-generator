import os
import requests
import json
from openai_client import call_openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

LLMFOUNDRY_TOKEN = os.environ.get("LLMFOUNDRY_TOKEN")
LLMFOUNDRY_PROJECT = os.environ.get("LLMFOUNDRY_PROJECT", "my-test-project")

if not LLMFOUNDRY_TOKEN:
    raise ValueError("LLMFOUNDRY_TOKEN is not set in environment variables.")

LLMFOUNDRY_BASE_URL = "https://llmfoundry.straive.com/gemini/v1beta"

def generate_raw_subtitles(file_obj, model="gemini-2.5-pro"):
    try:
        # Prepare the prompt
        base_prompt = "Give me subtitles for this video clip in SRT format, Focus on dialogue and important sound effects."
        
        # LLM Foundry supports multimodal inputs with base64-encoded data
        # We'll include the video as an inline data part
        
        system_prompt = """
You are a professional audiovisual subtitle generator.

Your task is to create industry-standard subtitles from video input, combining audio and visual analysis for maximum accuracy. Do NOT include speaker/character names; output only what is spoken or relevant cues.

Guidelines:

1. Multimodal Analysis
- Use both audio (speech, tone, music, sound effects) and video (facial expressions, actions, on-screen text, scene context).
- Disambiguate ambiguous sounds using visuals (e.g., frightened face + "aah" → [SCREAMING IN FEAR]).
- Adapt cues to the genre (horror, comedy, action, etc.).

2. Output Format
- Subtitles must be valid SRT:
  - Sequential numbering starting at 1
  - Timestamps `HH:MM:SS,mmm --> HH:MM:SS,mmm` (strict)
- Max 2 lines, ~42 characters per line (~84 total)
- Proper grammar, punctuation, and natural phrasing
- Ensure readable timing: min. 1s display, ~20 cps max

3. Non-Speech & Visual Cues
- Use square brackets for meaningful sounds: [MUSIC PLAYING], [GUNSHOT], [DOOR CREAKS], [APPLAUSE]
- Add plot-relevant visual cues only if essential: [ON-SCREEN TEXT: The End], [LIGHTNING FLASHES]
- Keep cues concise, descriptive, professional
- If multiple sounds in same block, separate each with a line break.

4. Consistency & Coverage
- Ensure full subtitle coverage of the video
- Maintain consistent style and formatting
- Never skip or alter timestamp format
- If the music starts and then goes on, Do not miss the music in the subtitles. i.e; [MUSIC PLAYING], [MUSIC PLAYING].... till the music stops. Same with the sound effects.

IMP: When ever there is an background noise, always have it in the subtitles, Even with minute details (e.g., [BIRD CHIRPING], [WIND RUSTLING], ...) - should be understandable and felt by deaf persons as well !
NEVER MISS Point 3 - Non-speech & Visual Cues, including the background noise, background music in the subtitles

Output natural, professional subtitles that meet industry standards and enhance comprehension, without adding speaker names.
"""
        
        # Prepare the request payload for LLM Foundry with multimodal input
        parts = [
            {
                "text": f"{system_prompt}\n\n{base_prompt}"
            }
        ]
        
        # Add video data if available
        if hasattr(file_obj, 'base64_data') and file_obj.base64_data:
            parts.append({
                "inline_data": {
                    "mime_type": file_obj.mime_type,
                    "data": file_obj.base64_data
                }
            })
        
        payload = {
            "contents": [
                {
                    "parts": parts
                }
            ],
            "generationConfig": {
                "temperature": 1.0,
                "maxOutputTokens": 8192
            }
        }
        
        # Set up headers with LLM Foundry authentication
        headers = {
            "Authorization": f"Bearer {LLMFOUNDRY_TOKEN}:{LLMFOUNDRY_PROJECT}",
            "Content-Type": "application/json"
        }
        
        print("Generating subtitles.... Please wait...")
        
        # Make the API request to LLM Foundry
        response = requests.post(
            f"{LLMFOUNDRY_BASE_URL}/models/{model}:generateContent",
            headers=headers,
            json=payload,
            timeout=300  # 5 minute timeout for video processing
        )
        
        if response.status_code != 200:
            raise Exception(f"LLM Foundry API error: {response.status_code} - {response.text}")
        
        response_data = response.json()
        
        # Extract the generated text from the response
        if "candidates" in response_data and len(response_data["candidates"]) > 0:
            candidate = response_data["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"]:
                raw_subtitles = candidate["content"]["parts"][0]["text"]
            else:
                raise Exception("Unexpected response format from LLM Foundry")
        else:
            raise Exception("No candidates in LLM Foundry response")

        print(raw_subtitles)
        return raw_subtitles
        
    except Exception as e:
        raise Exception(f"Error generating subtitles: {str(e)}")
    