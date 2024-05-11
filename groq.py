import os
import requests
import json
import logging
import rich
from rich.markdown import Markdown

HOME = os.getenv("HOME")
BASE_PATH = os.getenv("BASE_PATH", os.path.dirname(os.path.abspath(__file__)))
logging.basicConfig(filename=os.path.join(BASE_PATH, "logs", "groq.log"), level=logging.INFO, format='%(message)s')


def setup():
    """
    Creates the folder $HOME/.config/ai-terminal if it does not already exist.

    Args:
        None

    Returns:
        None
    """
def setup():
    # if the folder $HOME/.config/ai-terminal does not exist, create it
    if not os.path.exists(os.path.join(HOME, ".config/ai-terminal")):
        os.makedirs(os.path.join(HOME, ".config/ai-terminal"))

setup()

# receive the parameters "set model llama3-70b-8192", read a json file located at $HOME/.config/ai-terminal/current.json, add the model key to it, and save it back to the same file.
def set_model(model):
    current = {}
    with open(os.path.join(HOME, ".config/ai-terminal/current.json"), "a+") as file:
        file.seek(0)
        try:
            current = json.load(file)

            # Validate model against a list of supported models
            supported_models = ["llama3-70b-8192", "mixtral-8x7b-32768"]
            if current["model"] not in supported_models:
                raise ValueError("Invalid model. Please choose from the supported models: llama3-70b-8192, gpt3.5-turbo")
            else:
                current["model"] = model

        except json.decoder.JSONDecodeError:
            current = {}

        file.seek(0)
        json.dump(current, file)




def log(log_data):
    logging.info(log_data)


# Set the API endpoint and the API key
url = "https://api.groq.com/openai/v1/chat/completions"
api_key = os.getenv("GROQ_API_TOKEN")
if api_key is None:
    raise Exception("Please set the GROQ_API_TOKEN environment variable")


prompt = ""
system_prompt = ""
with open(os.getenv("", os.path.join(BASE_PATH, "conf/prompts/system.j2")), "r") as file:
    system_prompt = file.read()


# Set the headers
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

# Set the payload
payload = {
    "messages": [
        {"role": "system", "content": system_prompt},
    ],
    "model": os.getenv("MODEL", "llama3-70b-8192"),
    "temperature": float(os.getenv("TEMPERATURE", "0.7")),
    "max_tokens": int(os.getenv("MAX_TOKENS", "8192")),
    "top_p": 1,
    "stream": False,
    "stop": None,
}

while True:
    prompt = input("Ask away: ")

    if prompt == "exit":
        break

    payload["messages"].append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    # Make the POST request
    response = requests.post(url, headers=headers, json=payload)

    # log the response
    log(f"{response.text}")

    # Check the response
    if response.status_code == 200:
        data = response.json()

        msg = data["choices"][0]["message"]["content"]

        payload["messages"].append(
            {
                "role": "system",
                "content": msg,
            }
        )

        markdown = Markdown(msg)
        rich.print(markdown)

    print("\n")
    print("#" * 80)
