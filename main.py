import os
import time

from openai import OpenAI


class ChatBot:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        self.assistant = self.openai_client.beta.assistants.retrieve(assistant_id="asst_yoH4bMIj6t4fWpIew9QUkRUP")
        self.thread = self.openai_client.beta.threads.create()

    def chat(self, prompt: str) -> str:
        try:
            message = self.openai_client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role="user",
                content=prompt,
            )
            run = self.openai_client.beta.threads.runs.create(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id,
            )
            while run.status == "queued" or run.status == "in_progress":
                run = self.openai_client.beta.threads.runs.retrieve(thread_id=self.thread.id, run_id=run.id)
                time.sleep(0.5)
            messages = self.openai_client.beta.threads.messages.list(thread_id=self.thread.id)
            return messages.data[0].content[0].text.value
        except Exception as e:
            return str(e)


def main():
    print("Welcome to ChatGPT! Type 'quit' to exit.")
    bot = ChatBot()

    while True:
        user_input = input("You:\n")
        print()
        if user_input.lower() == 'quit':
            break
        response = bot.chat(user_input)
        print(f"ChatGPT:\n{response}\n")


if __name__ == "__main__":
    main()
