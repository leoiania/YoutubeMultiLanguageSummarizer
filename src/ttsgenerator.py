from abc import ABC, abstractmethod
import os
import time
from openai import OpenAI
from gtts import gTTS

class TTSGenerator(ABC):

    @abstractmethod
    def generate_audio(self, text):

        """
        Abstract method to generate the final audio file from the translated/summarized text. It returns a string representing the path in which the audio file is stored.
        Args:
            text (str): The text to be used for the TTS.
        
        Returns:
            str: A string containing the path of the generated audio.
        """
        pass


class Mock_TTSGenerator(TTSGenerator):
    
    def generate_audio(self, text, fake_key = None):
        mock_path = "src/mock_translation.mp3"
        return mock_path
    

class OpenAI_TTSGenerator(TTSGenerator):
    
    def generate_audio(self, text: str, openai_key:str = None) -> str:
        """
        Generates audio from the provided text using the OpenAI TTS API.

        Args:
            text (str): The text input that needs to be converted into audio.
            openai_key (str, optional): The API key for accessing the OpenAI service. If not provided, it takes the value of the environment variable 'OPENAI_API_KEY'.

        Returns:
            (str): The file path to the generated audio file.
        """
        if openai_key is None:
            openai_key = os.environ['OPENAI_API_KEY']
        
        timestamp = int(time.time())
        os.makedirs('translated_audio', exist_ok = True)
        translated_path = os.path.join('translated_audio', f"{timestamp}.wav")
        
        client = OpenAI(api_key = openai_key)
        response = client.audio.speech.create(
            model = "tts-1",
            voice = "alloy",
            input = text
            )
        
        with open(translated_path, "wb") as f:
            f.write(response.content)


        return translated_path
    


class g_TTSGenerator(TTSGenerator):
    
    def generate_audio(self, text: str, destination_language: str, input_url: str = None) -> str:
        """
        Generates audio locally using the gTTS library.

        Args:
            text (str): The text input that needs to be converted into audio.
            destination_language (str): The language of the desired TTS output.
            input_url (str, optional): The URL of the original video to be used to compose the filename. By default, the timestamp is used.

        Returns:
            (str): The file path to the generated audio file.
        """
        convert_language = {
        "italian":"it",
        "english":"en",
        "francais":"fr",
        "spanish":"es",
        "deutsch":"de"
        }
        if len(destination_language) > 2:
            destination_language = convert_language[destination_language]
        
        os.makedirs('translated_audio', exist_ok = True)
        if input_url is None:
            timestamp = int(time.time())
            translated_path = os.path.join('translated_audio', f"{timestamp}.wav")
        else:
            if "?v=" in input_url:
                video_name = input_url.split("?v=")[-1].split("&")[0] + ".mp3"
            elif "shorts" in input_url:
                video_name = input_url.split("/")[-1].split(".")[0] + ".mp3"
            translated_path = os.path.join('translated_audio', f"translated_{destination_language}_{video_name}.wav")
        
        if not os.path.isfile(translated_path):
            print('starting gTTS..')
            response = gTTS(text, lang = destination_language)
            response.save(translated_path)

        return translated_path
    
