from pathlib import Path
import os

ENV_PATH = ".env"


def unification_of_dicts(first_dict: dict, second_dict: dict) -> dict:
    return {**first_dict, **second_dict}


def validate(dict_of_dotenv: dict) -> dict:
    validated_dict = {}
    for key, value in zip(dict_of_dotenv.keys(), dict_of_dotenv.values()):
        key = key.strip()
        value = value.strip()
        try:
            if value.isdecimal():
                validated_dict[key] = int(value)
            elif Path(value).is_dir():
                validated_dict[key] = Path(value)
            else:
                validated_dict[key] = value
        except PermissionError:
            pass
    return validated_dict


def content_of_env_to_dict() -> dict:
    return validate(dict(os.environ))

def content_of_file_to_dict() -> dict:
    lines_of_dotenv = []
    with open(ENV_PATH) as env_file:
        lines_of_dotenv = env_file.read().splitlines()
    
    dict_of_dotenv = {}

    for line in lines_of_dotenv:
        key, value = line.split("=")
        dict_of_dotenv[key] = value

    return validate(dict_of_dotenv)


env = type("env", (object,), unification_of_dicts(content_of_file_to_dict(),
                                                  content_of_env_to_dict())
)





