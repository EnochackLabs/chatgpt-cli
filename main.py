import os

from openai import OpenAI, Stream
from openai.types.chat import ChatCompletionChunk


class ChatBot:
    def __init__(self, model: str = "gpt-4"):
        self.messages = []
        self.openai_client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        self.model = model

    def chat(self, message: str) -> Stream[ChatCompletionChunk] | str:
        try:
            self.messages.append({'role': 'user', 'content': message})
            stream = self.openai_client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                stream=True,
            )
            return stream
        except Exception as e:
            str(e)


def main():
    print("Welcome to ChatGPT! Type 'bye' to exit.\n")
    chatbot = ChatBot()

    while True:
        # Get user input
        user_input = input("You:\n")
        print()
        if user_input.lower() == 'bye':
            break
        # Get response from OpenAI
        print("ChatGPT:")
        stream = chatbot.chat(user_input)
        if type(stream) is str:
            print(stream)
            continue
        for chunk in stream:
            print(chunk.choices[0].delta.content or "", end="")
        print("\n")


if __name__ == "__main__":
    main()
