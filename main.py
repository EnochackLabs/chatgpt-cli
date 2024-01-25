import os

from openai import OpenAI

openai_client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))


def chat_gpt(prompt, model="gpt-4"):
    try:
        stream = openai_client.chat.completions.create(
            model=model,
            messages=[{"role": "user",
                       "content": prompt}],
            stream=True,
        )
        return stream
    except Exception as e:
        return str(e)


def main():
    print("Welcome to ChatGPT! Type 'quit' to exit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break

        stream = chat_gpt(user_input)
        print("ChatGPT: ", end="")
        for chunk in stream:
            print(chunk.choices[0].delta.content or "", end="")
        print()


if __name__ == "__main__":
    main()
