from config.envs import HOME
import os
import json


def setup():
    """
    Creates the folder $HOME/.config/ai-terminal if it does not already exist.

    Args:
        None

    Returns:
        None
    """
    # if the folder $HOME/.config/ai-terminal does not exist, create it
    if not os.path.exists(os.path.join(HOME, ".config/ai-terminal")):
        os.makedirs(os.path.join(HOME, ".config/ai-terminal"))


def validate_model(model: str):
    # Validate model against a list of supported models
    supported_models = ["llama3-70b-8192", "mixtral-8x7b-32768"]
    if model not in supported_models:
        raise ValueError(
            "Invalid model. Please choose from the supported models: llama3-70b-8192, mixtral-8x7b-32768"
        )


def validate_temperature(temperature: float):
    # Validate temperature
    if not 0.0 <= temperature <= 1.0:
        raise ValueError("Temperature must be a float between 0.0 and 1.0")


# receive the parameters "set model llama3-70b-8192", read a json file located at $HOME/.config/ai-terminal/current.json, add the model key to it, and save it back to the same file.
def set_config(key, value):
    current = {}
    with open(os.path.join(HOME, ".config/ai-terminal/current.json"), "a+") as file:
        file.seek(0)
        try:
            current = json.load(file)
            if key not in ["model", "temperature"]:
                raise ValueError(
                    "Invalid configuration key. Please choose from 'model', 'temperature'"
                )

            if key == "model":
                validate_model(value)
            elif key == "temperature":
                validate_temperature(float(value))

        except json.decoder.JSONDecodeError:
            current = {}

        file.seek(0)
        json.dump(current, file)
