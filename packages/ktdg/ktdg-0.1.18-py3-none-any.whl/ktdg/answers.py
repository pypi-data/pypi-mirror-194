from typing import TypedDict

import numpy as np
import pydantic
import ruamel.yaml

from .utils import (
    create_skill_vector,
    hash_config,
    load_print,
    load_progress,
    parse_config,
    set_seed_if_missing,
)

from .distributions import (
    Constant,
    Distribution,
    add_distribution_comments,
    generate_values,
    parse_distribution,
)
from .questions import Question
from .skills import Skill
from .students import Student

#########
# types #
#########


class Config(pydantic.BaseModel):
    wrong_answer_adjustment: float = 0
    guess_adjustment: float = 0
    mastery_importance: float = 1
    n_per_student: Distribution = Constant(value=50)
    max_repetitions: int = 1
    can_repeat_correct: bool = False
    seed: int = 0
    hash: str = ""

    _parse_n_per_student = parse_config("n_per_student", parse_distribution)
    _set_seed = set_seed_if_missing("seed")
    _hash_config = hash_config()


class Answer(TypedDict):
    id: int
    student: int
    question: int
    timestamp: int
    correct: bool
    p_correct: float
    state: dict[int, float]


############
# external #
############


def add_comments(config: Config) -> ruamel.yaml.CommentedMap:
    config_ = ruamel.yaml.CommentedMap(config.dict())
    config_.yaml_add_eol_comment(
        "How much should the learning be scaled when the answer is wrong",
        "wrong_answer_adjustment",
    )
    config_.yaml_add_eol_comment(
        "How much should the learning be scaled proportional to guess value",
        "guess_adjustment",
    )
    config_.yaml_add_eol_comment(
        "How much the skill mastery should be scaled by in the exponential",
        "mastery_importance",
    )
    config_.yaml_add_eol_comment(
        "Number of answers by student",
        "n_per_student",
    )
    config_["n_per_student"] = add_distribution_comments(config.n_per_student)
    config_.yaml_add_eol_comment(
        "Maximum number of times a question can be repeated "
        + "(to allow unlimited, set to 0)",
        "max_repetitions",
    )
    config_.yaml_add_eol_comment(
        "If a correctly answered question can be asked again",
        "can_repeat_correct",
    )
    config_.yaml_add_eol_comment(
        "random seed to use (set to 0 to have new seed)", "seed"
    )
    config_.yaml_add_eol_comment(
        "hash of the config (automatically modified)", "hash"
    )
    return config_


def generate(
    config: Config,
    students: list[Student],
    questions: list[Question],
    skills: list[Skill],
    echo: bool = True,
) -> list[Answer]:
    load_print("Generating answers...", echo=echo)
    rng = np.random.default_rng(config.seed)
    answers = [
        answer
        for student in load_progress(
            students, "Generating answers...", echo=echo
        )
        for answer in _generate_student_answers(
            config, student, questions, len(skills), rng
        )
    ]
    return [
        {**answer, "id": i} for i, answer in enumerate(answers)  # type: ignore
    ]


############
# internal #
############


def _generate_student_answers(
    config: Config,
    student: Student,
    questions: list[Question],
    n_skills: int,
    rng: np.random.Generator,
) -> list[Answer]:
    n_questions = min(
        len(questions), int(generate_values(1, config.n_per_student, rng)[0])
    )
    skill_state = create_skill_vector(student["skills"], n_skills)

    answers: list[Answer] = []
    for i in range(n_questions):
        question = _choose_question(
            answers,
            questions,
            config.max_repetitions,
            config.can_repeat_correct,
            rng,
        )
        question_ = create_skill_vector(question["skills"], n_skills)
        p_correct = _compute_p_correct(
            skill_state,
            question_,
            student,
            question,
            config.mastery_importance,
        )
        correct = bool(rng.binomial(1, p_correct))
        skill_state = _update_skill_state(
            skill_state,
            question_,
            correct,
            student,
            question,
            config.wrong_answer_adjustment,
            config.guess_adjustment,
        )
        answers.append(
            Answer(
                id=0,
                student=student["id"],
                question=question["id"],
                timestamp=i,
                correct=correct,
                p_correct=p_correct,
                state={i: v for i, v in enumerate(skill_state) if v},
            )
        )
    return answers


def _choose_question(
    answers: list[Answer],
    questions: list[Question],
    max_repetitions: int,
    can_repeat_correct: bool,
    rng: np.random.Generator,
) -> Question:
    freqs = [
        len(
            [
                answer
                for answer in answers
                if answer["question"] == question["id"]
            ]
        )
        for question in questions
    ]
    questions = [
        question
        for question, freq in zip(questions, freqs, strict=True)
        if max_repetitions == 0 or freq < max_repetitions
    ]
    if not can_repeat_correct:
        answered_correctly = {
            answer["question"] for answer in answers if answer["correct"]
        }
        questions = [
            question
            for question in questions
            if question["id"] not in answered_correctly
        ]
    if not len(questions):
        raise RuntimeError("There are no questions left to ask.")
    return rng.choice(questions)  # type: ignore


def _compute_p_correct(
    student_skills: np.ndarray,
    question_skills: np.ndarray,
    student: Student,
    question: Question,
    mastery_importance: float,
) -> float:
    slip, guess = _compute_slip_and_guess(student, question)
    mastery = np.exp(
        mastery_importance
        * (np.dot(student_skills, question_skills) - question["difficulty"])
    )
    return min(guess + (1 - slip) * mastery / (1 + mastery), 1)


def _update_skill_state(
    student_skills: np.ndarray,
    question_skills: np.ndarray,
    correct: bool,
    student: Student,
    question: Question,
    wrong_answer_adjustment: float,
    guess_adjustment: float,
) -> np.ndarray:
    _, guess = _compute_slip_and_guess(student, question)
    guess_adjustment = (1 - guess_adjustment) * (1 - guess)
    return (
        student_skills * (1 - student["forget_rate"])
        + student["learning_rate"]
        * guess_adjustment
        * question_skills
        * (0.5 + question["difficulty"])
        * (1 - wrong_answer_adjustment * (1 - correct))
    ).clip(0, 1)


def _compute_slip_and_guess(
    student: Student, question: Question
) -> tuple[float, float]:
    slip = 1 - np.sqrt((1 - student["slip"]) * (1 - question["slip"]))
    guess = 1 - np.sqrt((1 - student["guess"]) * (1 - question["guess"]))
    return slip, guess
