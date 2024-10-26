from abc import ABC, abstractmethod
import os
from groq import Groq


class VideoTranscriptor(ABC):
    @abstractmethod
    def transcript_video(self, audio_path: str) -> str:
        """
        Abstract method to read an audio file from a path and return its transcription as string.
        Args:
            audio_path (str): The path of the audio file.
        
        Returns:
            str: A string containing the transcription of the audio.
        """


   
class Groq_Transcriptor(VideoTranscriptor):
    """
    A class that handles video transcription using the GROQ API.

    Attributes:
        model (str): The model name used for transcription, defaulting to "whisper-large-v3-turbo".
    """

    def __init__(self, model_name = "whisper-large-v3-turbo"):
        self.model = model_name

    def transcript_video(self, audio_path, groq_api_key = None):
        """
        Transcribes audio from a audio file path using the GROQ API.

        Args:
            audio_path (str): The file path to the audio file that needs to be transcribed.
            groq_api_key (str, optional): The API key for accessing the GROQ service. If not provided, take as default the value of the environment variable 'GROQ_API_KEY'.

        Returns:
            str: The transcribed text from the audio file.

        Behavior:
            - Initializes the GROQ client with the provided or environment API key.
            - Reads the audio file and sends it to the GROQ API for transcription.
            - Returns the transcription text received from the API.
        """

        if groq_api_key is None:
            groq_api_key = os.environ['GROQ_API_KEY']

        self.groq_client = Groq(api_key=groq_api_key)

        with open(audio_path, 'rb') as file:
            transcription = self.groq_client.audio.transcriptions.create(
                file = (audio_path, file.read()),
                model = self.model
            )
        
        return transcription.text
