from pathlib import Path
import json
from typing import TypedDict
import pydantic

import ruamel.yaml
from .utils import hash_config, load_print, done_print
from . import (
    skills as skills_,
    questions as questions_,
    answers as answers_,
    students as students_,
)


#########
# types #
#########


class Config(pydantic.BaseModel):
    skills: skills_.Config = skills_.Config()
    questions: questions_.Config = questions_.Config()
    students: students_.Config = students_.Config()
    answers: answers_.Config = answers_.Config()
    hash: str = ""

    _hash_config = hash_config()


class Data(TypedDict):
    skills: list[skills_.Skill]
    students: list[students_.Student]
    questions: list[questions_.Question]
    answers: list[answers_.Answer]


############
# external #
############


def read_config(config: Path) -> Config:
    yaml = ruamel.yaml.YAML()
    with open(config, "r") as f:
        config_ = Config(**yaml.load(f))
    return config_


def save_config(config: Config, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    yaml = ruamel.yaml.YAML()
    with open(path, "w") as f:
        yaml.dump(_add_comments(config), f)


def generate(config: Config, echo: bool = True) -> Data:
    skills = skills_.generate(config.skills, echo=echo)
    students = students_.generate(config.students, skills, echo=echo)
    questions = questions_.generate(config.questions, skills, echo=echo)
    answers = answers_.generate(
        config.answers, students, questions, skills, echo=echo
    )
    done_print("Generated data.", echo=echo)
    return {
        "skills": skills,
        "students": students,
        "questions": questions,
        "answers": answers,
    }


def save_data(data: Data, output_file: Path, echo: bool = True) -> None:
    load_print("Saving data...", echo=echo)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)
    done_print(f"Saved data in {output_file}.", echo=echo)


############
# internal #
############


def _add_comments(config: Config) -> ruamel.yaml.CommentedMap:
    config_ = ruamel.yaml.CommentedMap(config.dict())
    config_["skills"] = skills_.add_comments(config.skills)
    config_["questions"] = questions_.add_comments(config.questions)
    config_["students"] = students_.add_comments(config.students)
    config_["answers"] = answers_.add_comments(config.answers)
    return config_
