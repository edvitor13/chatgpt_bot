import os
import openai



class ChatGPT:
    
    def __init__(self):
        openai.api_key = os.environ['CHATGPT_API_KEY']
        self.__last_response: dict = None


    def ask(self, message: str) -> str | None:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=message,
            temperature=0,
            max_tokens=1950,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["<|endoftext|>"]
        )

        self.__last_response = response
        return response['choices'][0]["text"]
