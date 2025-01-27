from core.llm_connector import ChatGPTConnector

system_prompt: str = "Engkau adalah guru sejarah yang sangat sabar dan suka menjelaskan"
user_prompt1: str = "Siapakah presiden jokowi (jkw) ?"
user_prompt2: str = "Lebih detailkan penjelasan dari pertanyaan saya sebelumnya. Mohon minimal 50 paragraph"

chat_gpt = ChatGPTConnector()

print(f"\n\nContext 1:\n{chat_gpt.get_context()}\n\n")

print(f"{'#' * 100} 1")
print(f"Pertanyaan: {user_prompt1}\n\n")
result1 = chat_gpt.ask(system_prompt=system_prompt, user_prompt=user_prompt1)
print(result1)
print(f"\n\nContext 2:\n{chat_gpt.get_context()}\n\n")

print(f"{'#' * 100} Pertanyaan 2")
print(f"Pertanyaan: {user_prompt2}\n\n")
result2 = chat_gpt.ask(system_prompt=system_prompt, user_prompt=user_prompt2)
print(result2)
print(f"\n\nContext 3:\n{chat_gpt.get_context()}\n\n")
