# YoutubeMultiLanguageSummarizer

A very easy-to-do (and easy-to-use) AI-powered summarizer (text and audio) that takes a YouTube video or short URL as input. This tool generates concise, multilingual summaries in both text and audio formats, making it ideal for quickly understanding videos in multiple languages without watching the entire content.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Languages Supported](#languages-supported)
- [Next Steps](#next-steps)

---

## Installation
To install **YoutubeMultiLanguageSummarizer**, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/YoutubeMultiLanguageSummarizer.git
   cd YoutubeMultiLanguageSummarizer
   ```
2. **The creation and usage of a virtual environment is suggested**:
   use ```python``` and ```pip``` instead of ```python3``` and ```pip3``` if needed
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. **Install the requirements**:
    ```bash
    pip3 install -r requirements.txt
    ```
Now you are ready to use it!

## Usage

You have two options to use this feature: by terminal or by the gradio app. Currently, the terminal only feature is present on this repo - the gradio app will be available soon.
To run this feature in your terminal - assuming you have to summarize and translate [this video](https://www.youtube.com/watch?v=-EtL1eOnkzI). in italian:
```bash
python3 inference_cli.py "https://www.youtube.com/watch?v=-EtL1eOnkzI" "it" --groq_key_input <<YOUR-GROQ-KEY>>
``` 
If you need help for the needed arguments, run:
```bash
python3 inference_cli.py -h
``` 
*There is the possibility - not automatically configured - to add the OpenAI API Key and use their voice ("Alloy" by default) for TTS.*

## Languages Supported

Our summarizer speaks your language! 🌐 Choose from:

- **Italian** 🇮🇹
- **English** 🇬🇧
- **Français** 🇫🇷
- **Spanish** 🇪🇸
- **Deutsch** 🇩🇪
  
## Next Steps

:warning: *This repository is just a preview of a more advanced YouTube translator that uses speaker diarization to achieve highly accurate, start-to-finish translations. The final version will automatically recognize and match speakers' voices and genders, offering an automated multilanguage voice-dubbing experience. You can find it [here](https://example.com).*:warning:
--
Here’s what’s coming up:

- [ ] **Gradio Web Apps**: At least two interactive Gradio applications will be added, making it even easier to try out features directly in your browser.
- [ ] **Expanded Voice Options**: Expect a greater variety of voices, providing more options for tone, accent, and style.
- [ ] **Full Local Deployment**: Support for running locally on powerful CPU and GPU systems for high-performance processing without the cloud.
- [ ] **Docker Support**: A Docker image will be available, making setup and deployment as simple as a single command.

Stay tuned for these enhancements, designed to make YouTube translation and dubbing more accessible and powerful!

