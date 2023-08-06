import re
from typing import TypeVar

import questionary
import requests
import typer

EnumType = TypeVar("EnumType")


def camel_to_snake(text: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", text).lower()


def question(question: str, choices: EnumType) -> questionary.Question:
    prompt = camel_to_snake(choices.__name__).replace("_", " ")  # type: ignore
    return questionary.select(question, choices=list(choices))


def question_input(text: str) -> questionary.Question:
    return questionary.text(text)


def binary_question(option: str) -> questionary.Question:
    return questionary.confirm(f"Do you want {option}?", default=False)


def get_package_version(package_name) -> str:
    try:
        response = requests.get(f"https://pypi.python.org/pypi/{package_name}/json")
        data = response.json()
        return data["info"]["version"]
    except Exception as e:
        print(e)
        return "*"
