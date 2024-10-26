from pytubefix import YouTube
import os
from abc import ABC, abstractmethod

class VideoDownloader(ABC):
    def __init__(self, output_folder="download_audio"):
        self.output_folder = output_folder
        os.makedirs(self.output_folder, exist_ok=True)

    @abstractmethod
    def download_audio(self, url: str) -> dict:
        """
        Abstract method to download audio from a video URL.
        Args:
            url (str): The URL of the video.
        
        Returns:
            dict: Dictionary with video title and file path.
                Example: {"video_title": <title>, "video_path": <path_to_audio>}
        """
        pass

    def check_existing_download(self, video_name):
        videos_list = os.listdir(self.output_folder)
        return video_name in videos_list


class PytubeFix_VideoDownloader(VideoDownloader):

    def download_audio(self, url: str) -> dict:
        """
        Download audio from a video URL.
        Args:
            url (str): The URL of the video.
        
        Returns:
            dict: Dictionary with video title and file path.
                Example: {"video_title": <title>, "video_path": <path_to_audio>}
        """
        if not "youtube.com" in url:
            raise Exception(f"The provided is not a valid youtube URL - URL: {url}")

        if "?v=" in url:
            video_name = url.split("?v=")[-1].split("&")[0] + ".mp3"
        elif "shorts" in url:
            video_name = url.split("/")[-1].split(".")[0] + ".mp3"
        yt = YouTube(url)
        existing_video = self.check_existing_download(video_name)
        if not existing_video:
            ys = yt.streams.filter(only_audio=True).first()
            ys.download(output_path = self.output_folder, filename = video_name)
        else:
            print("video already cached")

        return {"video_title": yt.title,
                "video_path": os.path.join(self.output_folder, video_name)}


if __name__ == "__main__":
    downloader = PytubeFix_VideoDownloader()
    url = ""
    result = downloader.download_audio(url)
    print(result)