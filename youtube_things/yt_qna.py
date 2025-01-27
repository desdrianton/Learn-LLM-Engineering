from youtube_transcript_api import YouTubeTranscriptApi

from core.llm_connector import ChatGPTConnector

def get_transcript(video_id, language='id'):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        return " ".join([item['text'] for item in transcript])
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None

# ======================================================================================================================
# Run
# ======================================================================================================================
llm_connector = ChatGPTConnector()
yt_video_id = "tvAQGusmiDI"

transcript_text = get_transcript(yt_video_id)
system_prompt = f"""
Engkau adalah trainer yang sangat sabar dan fun dalam menjelaskan materi. Muridmu kebanyakan adalah gen-z, sehingga jangan terlalu kaku dalam menjawab. Tugasmu adalah:
- Menjawab pertanyaan dari murid
- Menjawab dengan sabar
- Pergunakan bullet point bila memungkinkan

Materinya adalah sebagai berikut: {transcript_text} 
"""

print(f"{'=' * 100}")
print("Video: Tutorial WDIO WebdriverIO #4 - Method Pada Element Di WebdriverIO")
print(f"{'=' * 100}")
print("\n\n")

ask1 = "Jelaskan materi ini seakan-akan saya anak kelas 5 SD"
answer1 = llm_connector.ask(system_prompt=system_prompt, user_prompt=ask1)
print(f"{'.'*80} QnA 1")
print(f"Ask:\n{ask1}\n\n")
print(f"Answer:\n{answer1}\n\n")

ask2 = "Berikan contoh code yang lain"
answer2 = llm_connector.ask(system_prompt="", user_prompt=ask2)
print(f"{','*80} QnA 2")
print(f"Ask:\n{ask2}\n\n")
print(f"Answer:\n{answer2}\n\n")

ask3 = "Apakah di video ini dijelaskan cara menguji captcha?"
answer3 = llm_connector.ask(system_prompt="", user_prompt=ask3)
print(f"{'.'*80} QnA 3")
print(f"Ask:\n{ask3}\n\n")
print(f"Answer:\n{answer3}\n\n")