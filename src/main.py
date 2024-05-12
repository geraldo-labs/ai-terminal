import os
import requests
import json
import logging
import rich
from rich.markdown import Markdown
import argparse

from config import set_config

HOME = os.getenv("HOME")
BASE_PATH = os.getenv("BASE_PATH", os.path.dirname(os.path.abspath(__file__)))
logging.basicConfig(filename=os.path.join(BASE_PATH, "logs", "groq.log"), level=logging.INFO, format='%(message)s')


parser = argparse.ArgumentParser(description="Ask any question")
parser.add_argument("question", help="The question you want to ask")
parser.add_argument("--model", help="Set the model to be used")
parser.add_argument("--temperature", help="Set the model to be used")
args = parser.parse_args()

for arg in vars(args):
    if getattr(args, arg):
        set_config(arg, getattr(args, arg))





# handle command line input to set the model and temperature
parser = argparse.ArgumentParser(description='Handle arguments of the application.')
subparsers = parser.add_subparsers(dest='set', help='Sub-command help')

# Subparser for the "model" command
model_parser = subparsers.add_parser('model', help='Set the model name')
model_parser.add_argument('modelname', type=str, help='Name of the model to set')

# Subparser for the "temperature" command
temp_parser = subparsers.add_parser('temperature', help='Set the temperature value')
temp_parser.add_argument('value', type=str, help='Temperature value to set')








print(temp_parser.parse_args())

exit()








parser = argparse.ArgumentParser(description='Set the model and temperature for the AI chatbot.')
parser.add_argument('--model', type=str, default='llama3-70b-8192', help='The model to use for chatbot')
parser.add_argument('--temperature', type=float, default=0.7, help='The temperature for chatbot response')
args = parser.parse_args()

# Set the model and temperature in the payload
payload["model"] = args.model
payload["temperature"] = args.temperature

def handle_command_input(prompt: str):
    """
    Handles the command input to set the model and temperature.

    Args:
        prompt (str): The user input prompt.

    Returns:
        bool: True if the prompt was a command, False otherwise.
    """
    match_model = re.match(r"ask set model (.+)", prompt)
    match_temperature = re.match(r"ask set temperature (\d+(\.\d+)?)", prompt)
    
    if match_model:
        args.model = match_model.group(1)
        payload["model"] = args.model
        return True
    elif match_temperature:
        args.temperature = float(match_temperature.group(1))
        payload["temperature"] = args.temperature
        return True
    else:
        return False

while True:
    prompt = input("Ask away: ")
    if prompt == "exit":
        break
    if handle_command_input(prompt):
        continue
    
    payload["messages"].append(
        {
            "role": "user",
            "content": prompt,
        }
    )
    # Make the POST request
    response = requests.post(url, headers=headers, json=payload)
    # log the response
    log("info", f"{response.text}")
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








def log(level: str, log_data: str):
    """
    Logs the provided data at the specified level.

    Args:
        level (str): The log level, either 'info' or 'error'.
        log_data (str): The data to be logged.

    Raises:
        ValueError: If an invalid log level is provided.

    Returns:
        None
    """

    if level == "info":
        logging.info(log_data)
    elif level == "error":
        logging.error(log_data)
    else:
        raise ValueError("Invalid log level. Please choose from 'info' or 'error'.")
    

setup()

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
    log("info", f"{response.text}")

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
