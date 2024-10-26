from videodownloader import PytubeFix_VideoDownloader
from videotranscriptor import Groq_Transcriptor
from translator import Groq_Translator
from ttsgenerator import g_TTSGenerator

LANGUAGES_DICT = {
        "🇮🇹 Italian": "italian",
        "🇬🇧 English": "english",
        "🇫🇷 Francais": "francais",
        "🇪🇸 Spanish": "spanish",
        "🇩🇪 Deutsch": "deutsch",
        }


class PolySummaryYT():
    '''This class is the main class of all the repo - it manages all the steps from the youtube URL to the generation of the translated audio.'''

    def __init__(self):
        self.videodownloader = PytubeFix_VideoDownloader()
        self.videotranscriptor = Groq_Transcriptor("whisper-large-v3-turbo")
        self.translator = Groq_Translator()
        self.TTSGenerator = g_TTSGenerator()

    def get_languages(self):
        return list(LANGUAGES_DICT.keys())

    def summarize_video(self, input_url, language, groq_key_input = None, openai_key = None):
        destination_language = LANGUAGES_DICT[language]
        print('selected language:', destination_language)
        print('url:', input_url)

        # Download step:
        download_result = self.videodownloader.download_audio(input_url)
        original_audio_path = download_result['video_path']

        # Transcript step:
        transcripted_text = self.videotranscriptor.transcript_video(original_audio_path, 
                                                                    groq_key_input)
        
        # Translation step:
        translated_text = self.translator.translate_transcription(transcripted_text,
                                                                   download_result['video_title'],
                                                                   destination_language,
                                                                   groq_key_input
                                                                    )
        
        # TTS step:
        translated_audio_path = self.TTSGenerator.generate_audio(translated_text, 
                                                                destination_language,
                                                                input_url)
        
        return {
            "audio_path": translated_audio_path,
            "text": translated_text
        }
    
    
    
    