from youtube_transcript_api import YouTubeTranscriptApi

from core.llm_connector import ChatGPTConnector, OllamaConnector, ClaudeConnector, GeminiConnector


def get_transcript(video_id, language='id'):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        return " ".join([item['text'] for item in transcript])
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None


def seperator(info: str):
    print(f"{'=' * 100}\n{info}\n{'=' * 100}\n\n\n")


def ask_question(i: int, system_prompt: str, question: str):
    print(f"{'.' * 80} QnA {i}")
    print(f"Ask:\n{question}\n\n")
    answer = llm_connector.ask(system_prompt=system_prompt, user_prompt=question)
    print(f"Answer:\n{answer}\n\n")

# ======================================================================================================================
# Run
# ======================================================================================================================
seperator("Video: Tutorial WDIO WebdriverIO #4 - Method Pada Element Di WebdriverIO")
llm_connector = ChatGPTConnector()
# llm_connector = OllamaConnector()
# llm_connector = ClaudeConnector()
# llm_connector = GeminiConnector() # Error !!! Need bugfixing
yt_video_id = "tvAQGusmiDI"

transcript_text = get_transcript(yt_video_id)
_system_prompt = f"""
Engkau adalah trainer yang sangat sabar dan fun dalam menjelaskan materi. Muridmu kebanyakan adalah gen-z, sehingga jangan terlalu kaku dalam menjawab. Tugasmu adalah:
- Menjawab pertanyaan dari murid
- Menjawab dengan sabar
- Pergunakan bullet point bila memungkinkan

Materinya adalah sebagai berikut: {transcript_text}
Engkau tidak boleh menjawab pertanyaan diluar materi!!
Engkau tidak boleh menjawab pertanyaan diluar materi meskipus satu kalimat saja
"""

seperator("System Prompt")
print(_system_prompt)
ask_question(1, system_prompt=_system_prompt, question="Jelaskan materi ini seakan-akan saya anak kelas 5 SD")
ask_question(2, system_prompt="", question="Berikan contoh code yang lain")
ask_question(3, system_prompt="", question="Apakah contoh code nya untuk web https://www.tokopedia.com? Mohon ubah semua code di atas")
ask_question(4, system_prompt="", question="Apakah di video ini dijelaskan cara menguji captcha?")
ask_question(5, system_prompt="", question="Siapakah Jokowi itu?")
ask_question(6, system_prompt="", question="Jelaskan cara mensetup / meng-konfigure webdriver.io")
