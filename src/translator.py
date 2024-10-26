from abc import ABC, abstractmethod
from groq import Groq
import os


class Translator(ABC):

    @abstractmethod
    def translate_transcription(self, original_text: str, destination_language: str) -> str:
        pass


class Groq_Translator(Translator):
    '''
    This object of this class are responsible for translating the transcription created using the GROQ API. 
    It implements the abstract method `translate_transcription` from the base `Translator` class, 
    allowing translation of the given `original_text` from one language to another specified by `destination_language`.
    
    '''
    def __init__(self, model_name:str = "llama-3.1-70b-versatile"):
        self.model = model_name #"llama3-8b-8192",
        self.char_limits = 1000
        

    def translate_transcription(self, transcription: str, original_title: str, destination_language: str, groq_api_key:str = None) -> str:
        '''
        This method is responsible for the translation of the transcription already generated. It is based on the GROQ API, using the LLM chosen as attribute self.model while initializing this subclass.
        
        Args:
            transcription (str): The transcription text to be translated.
            original_title (str): The title of the original content, used for contextual information.
            destination_language (str): The language to which the transcription should be translated.
            groq_api_key (str, optional): The API key for accessing the GROQ service, if needed.
        
        Returns:
            str: The translated transcription.
        '''
        if len(transcription) < self.char_limits:
            print('using directly a single translation step')
            assistant_prompt = f'You are an AI assistant that will receive the title and the transcription of a Youtube video. Your goal is to summarize this content in {destination_language} such that no information are lost without needing of watching the original video to understand the relevant content. You have to return the summary in {destination_language} only, do not write any other thing'
            translate_prompt = f'Original youtube title: {original_title}. \n Transcription of original video: "{transcription}".\n Summarize it in {destination_language}:'

            final_translation = self.translate_completion(assistant_prompt, translate_prompt, groq_api_key)
        
        else:
            print('using multiple step translation')
            final_translation = self.multiple_translation(transcription, original_title, destination_language, groq_api_key)
        print('text translation completed')
        return final_translation
    

    def translate_completion(self, assistant_prompt: str, translate_prompt: str, groq_api_key:str = None) -> str:
        """
        Sends prompts to the GROQ API to generate a translation completion based on the provided assistant and user prompts.

        Args:
            assistant_prompt (str): The system-level instruction or context for LLM.
            translate_prompt (str): The the text to be translated.
            groq_api_key (str, optional): The API key for accessing the GROQ service. If not provided, it defaults to the environment variable 'GROQ_API_KEY'.

        Returns:
            str: The translation retrieved by the GROQ API.
        """
        if groq_api_key is None:
            groq_api_key = os.environ['GROQ_API_KEY']
        
        self.groq_client = Groq(api_key=groq_api_key)
        messages_list = [
                {
                    "role": "system",
                    "content": assistant_prompt
                },
                {
                    "role": "user",
                    "content": translate_prompt,
                }
            ]

        chat_completion = self.groq_client.chat.completions.create(
            messages = messages_list,
            model= self.model,
            temperature=0.5,
            top_p=1,
            stop=None,
            stream=False,
            )
        
        return chat_completion.choices[0].message.content
    
    
    def multiple_translation(self, transcription: str, original_title: str, destination_language: str, groq_api_key:str = None) -> str:
        """
        Translates and summarizes a long transcription in multiple parts to avoid loss of information, using the GROQ API.

        Args:
            transcription (str): The full transcription text to be translated and summarized.
            original_title (str): The title of the original video for context in the translated summarization.
            destination_language (str): The target language for the summary translation.
            groq_api_key (str, optional): The API key for accessing the GROQ service. Defaults to the environment variable 'GROQ_API_KEY' if not provided.

        Returns:
            str: The concatenated translated and summarized text in the specified destination language.
        """

        final_text = ""

        transcription_list = self.split_transcription(transcription)
        for idx, transcription_chunk in enumerate(transcription_list):
            assistant_prompt = f'You are an AI assistant that will receive the title of a Youtube Video with its transcription splitted in {len(transcription_list)} parts, since it is very long. Your goal is to translate summarize this content in {destination_language} part by part, in order to avoid losing information without needing of watching the original video to understand the relevant content. You have to return the summary in {destination_language} only, do not write any other thing'

            translate_prompt =  f'Original video title: {original_title}.\n Part number {idx+1}° of the transcription of original video: "{transcription_chunk}".\n Summarize it in {destination_language}:'

            result_text = self.translate_completion(assistant_prompt, translate_prompt, groq_api_key)

            percentage = ((idx + 1) / len(transcription_list)) * 100
            bar_length = 30  # Length of the progress bar
            filled_length = int(bar_length * (idx + 1) / len(transcription_list))
            bar = '=' * filled_length + '-' * (bar_length - filled_length)
            # Print percentage and bar, using \r to overwrite each time
            print(f"{percentage:.2f}% [{bar}]", end="\r")

            final_text = final_text + result_text + " "
        print()
        return final_text
    

    def split_transcription(self, transcription: str) -> list:
        """
        Splits a long transcription into smaller chunks, each approximately 90% of the character limit set while initializing the object. 
        The split is not based on the string indices directly in order to avoid cutting word; rather the chunks are splitted at words-level, using as splitting word the one closer to the `self.char_limits` value

        Args:
            transcription (str): The full transcription text that needs to be split.

        Returns:
            list: A list of strings, where each string is a chunk of the original transcription, split by word boundaries.
        """

        cut_level = self.char_limits * 0.9
        final_list = []

        word_split = transcription.split(" ")

        newtxt = ""
        for i in range(len(word_split)):
            newtxt = newtxt + word_split[i] + " "
            if len(newtxt) > cut_level:
                final_list.append(newtxt)
                newtxt = ""

        return final_list
        
        