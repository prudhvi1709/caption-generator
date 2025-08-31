import os
from google import genai
from google.genai import types
from openai_client import call_openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in environment variables.")

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_raw_subtitles(file_obj, model="gemini-2.5-pro"):
    try:
        # Prepare the prompt
        base_prompt = "Give me subtitles for this video clip in SRT format, Focus on dialogue and important sound effects."
        
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_uri(
                        file_uri=file_obj.uri,
                        mime_type=file_obj.mime_type
                    ),
                    types.Part.from_text(text=base_prompt)
                ],
            ),
        ]

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

IMP: When ever there is an background noise, always have it in the subtitles, Even with minute details (e.g., [BIRD CHIRPING], [WIND RUSTLING], ...) - should be understandable and felt by deaf persons as well !
NEVER MISS Point 3 - Non-speech & Visual Cues

Output natural, professional subtitles that meet industry standards and enhance comprehension, without adding speaker names.
"""
        
        generate_content_config = types.GenerateContentConfig(
            thinking_config = types.ThinkingConfig(
                thinking_budget=24576,
            ),
            system_instruction=[
                types.Part.from_text(text=system_prompt),
            ],
            temperature=1,
        )
        
        print("Generating subtitles...")
        
        # Generate subtitles
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )
        raw_subtitles = response.text
        
        # Clean up: delete the uploaded file
        try:
            client.files.delete(name=file_obj.name)
            print("Temporary file cleaned up")
        except:
            pass  # Ignore cleanup errors

        print(raw_subtitles)
        return raw_subtitles
        
    except Exception as e:
        raise Exception(f"Error generating subtitles: {str(e)}")
    