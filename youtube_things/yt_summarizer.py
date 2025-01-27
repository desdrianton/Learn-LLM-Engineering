from youtube_transcript_api import YouTubeTranscriptApi

from core.llm_connector import ChatGPTConnector


def get_transcript(video_id, language='id'):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        return " ".join([item['text'] for item in transcript])
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None


def summarize_text(transcript_text: str):
    try:
        system_prompts = """
        You are a helpful assistant who provides concise and accurate summaries of text. Your task is to:

        - Capture the key points of the content.
        - Keep the summary brief and easy to understand.
        - Avoid summarizing overly lengthy texts or breaking them into excessively short summaries.
        - Use bullet points where appropriate to enhance clarity and structure.
        """

        user_prompt = f"Summarize the following text:\n{transcript_text}"

        llm_connector = ChatGPTConnector()
        return llm_connector.ask(system_prompt=system_prompts, user_prompt=user_prompt)
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return None

# yt_video_id = "kqaMIFEz15s"
yt_video_id = "tvAQGusmiDI"

transcript_text = get_transcript(yt_video_id)
summary = summarize_text(transcript_text)
print(summary)
