# 🎬 Caption Generator

A powerful AI-driven subtitle generation tool that creates accurate, professional subtitles for video files using Google's Gemini AI and OpenAI for post-processing refinement.

## ✨ Features

- **Multimodal Analysis**: Leverages both audio and visual content for maximum subtitle accuracy
- **Professional Quality**: Generates industry-standard SRT subtitles with proper formatting
- **Smart Compression**: Automatically compresses videos to 480p for optimal processing
- **Dual AI Processing**: Uses Gemini for initial generation and OpenAI for refinement
- **Wide Format Support**: Supports MP4, AVI, MOV, WebM, and many other video formats
- **Sound Effect Detection**: Intelligently identifies and labels important audio cues
- **Visual Context**: Incorporates on-screen text and visual elements into subtitles

## 📦 Installation

### Prerequisites

- Python 3.13 or higher
- FFmpeg installed on your system
- Google Gemini API key
- OpenAI API key (via OpenRouter)

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/Yadav-Aayansh/caption-generator.git
cd caption-generator
```

2. **Install dependencies using uv:**
```bash
uv sync
```

3. **Create a `.env` file in the project root:**
```env
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openrouter_api_key_here
```

### 🔑 Getting API Keys

#### Google Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Create a new project or select an existing one
3. Generate an API key from the API section
4. Add the key to your `.env` file

#### OpenRouter API Key
1. Visit [OpenRouter](https://openrouter.ai/)
2. Sign up for an account
3. Generate an API key from your dashboard
4. Add the key to your `.env` file

## 🚀 Usage

Generate subtitles for a video file:
```bash
uv run main.py <video_file> -srt <output_subtitle_file>
```

### 💡 Examples

```bash
# Generate subtitles for a movie
uv run main.py movie.mp4 -srt movie_subtitles.srt

# Process a presentation video
uv run main.py presentation.mov -srt presentation_captions.srt

# Generate subtitles for a webinar
uv run main.py webinar.webm -srt webinar_subtitles.srt
```

## ⚙️ How It Works

1. **Video Preprocessing**: The tool automatically compresses videos larger than 480p to optimize processing time and API costs
2. **Upload & Processing**: Videos are securely uploaded to Google's servers for analysis
3. **AI Generation**: Gemini AI analyzes both audio and visual content to generate initial subtitles
4. **Refinement**: OpenAI processes the raw subtitles to fix formatting, grammar, and timing issues
5. **Output**: Clean, professional SRT files ready for use

## 📼 Supported Video Formats

- MP4 (.mp4, .m4v)
- MPEG (.mpeg, .mpg)
- QuickTime (.mov)
- AVI (.avi)
- Flash Video (.flv)
- WebM (.webm)
- Windows Media (.wmv)
- 3GPP (.3gp, .3gpp)

---

<div align="center">
  
**Made with ❤️ by [Aayansh Yadav](https://github.com/Yadav-Aayansh)**

</div>