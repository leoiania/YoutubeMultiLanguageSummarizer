import argparse
import sys
sys.path.append('src')
from main import PolySummaryYT

if __name__ == "__main__":
    print('-'*200)
    parser = argparse.ArgumentParser(description="Summarize a video to a specified language.")

    parser.add_argument("input_url", type=str, help="The URL of the video to translate.")
    parser.add_argument("language", type=str, default="italian", help="['italian', 'english', 'francais', 'spanish', 'deutsch'] - The target language for translation.")
    parser.add_argument("--groq_key_input", type=str, default=None, help="The GROQ API key (optional). If not provided, the environment variable GROQ_API_KEY will be used")
    parser.add_argument("--openai_key", type=str, default=None, help="The OpenAI API key (optional). If not provided, the environment variable OPENAI_API_KEY will be used")
    
    args = parser.parse_args()

    # Assuming you have instantiated your class that contains translate_video method
    translator = PolySummaryYT()  # Replace with the actual class name
    result = translator.summarize_video(args.input_url, args.language, args.groq_key_input, args.openai_key)
    print(result)
    print(f'summarized and translated audio, file stored at: {result['audio_path']}')
