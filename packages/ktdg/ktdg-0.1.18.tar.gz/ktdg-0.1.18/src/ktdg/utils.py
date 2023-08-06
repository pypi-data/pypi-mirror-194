import hashlib
import random
import shutil
from typing import Any, Callable, Iterable, Type

import numpy as np
from pydantic import BaseModel, root_validator, validator
from tqdm import tqdm

############
# external #
############


def load_print(text: str, symbol: str = "*", echo: bool = True) -> None:
    symbol = f"\033[1m[{symbol}]\033[0m"
    if echo:
        print(
            f"\r{symbol} {text}".ljust(shutil.get_terminal_size().columns),
            end="\r",
        )


def done_print(text: str, symbol: str = "+", echo: bool = True) -> None:
    symbol = f"\033[1m\033[92m[{symbol}]\033[0m"
    if echo:
        print(f"\r{symbol} {text}".ljust(shutil.get_terminal_size().columns))


def load_progress(
    iter_: Iterable[Any],
    text: str,
    symbol: str = "*",
    echo: bool = True,
    *args: Any,
    **kwargs: Any,
) -> Iterable[Any]:
    symbol = f"\033[1m[{symbol}]\033[0m"
    if echo:
        return tqdm(
            iter_,
            f"\r{symbol} {text}",
            *args,
            leave=False,
            **kwargs,
        )
    else:
        return iter_


def set_field(field: str, value: Any) -> Callable:
    def fct_(cls: Type[BaseModel], val: Any) -> Any:
        return value

    return validator(field, allow_reuse=True, always=True)(fct_)  # type: ignore # noqa


def set_seed_if_missing(field: str) -> Callable:
    def fct_(val: int) -> int:
        if val == 0:
            return random.randint(0, 100_000)  # nosec
        else:
            return val

    return validator(field, allow_reuse=True, always=True)(fct_)  # type: ignore # noqa


def hash_config(ignore: list[str] = []) -> Callable:
    def fct_(cls: Type[BaseModel], vals: dict[str, Any]) -> dict[str, Any]:
        return {
            **vals,
            "hash": _hash_config(
                {
                    key: val.dict() if isinstance(val, BaseModel) else val
                    for key, val in vals.items()
                    if key not in ignore
                }
            ),
        }

    return root_validator(fct_, allow_reuse=True)  # type: ignore


def parse_config(field: str, fct: Callable) -> Callable:
    def fct_(
        cls: Type[BaseModel], val: dict[str, Any] | BaseModel | None
    ) -> BaseModel:
        if isinstance(val, BaseModel):
            return val
        elif val is None:
            return fct()
        else:
            return fct(val)

    return validator(field, allow_reuse=True, always=True, pre=True)(fct_)  # type: ignore # noqa


def clip_0_1(values: list[float]) -> list[float]:
    return [min(max(v, 0), 1) for v in values]


def create_skill_vector(skills: dict[int, float], n_skills: int) -> np.ndarray:
    return np.array([skills.get(skill, 0) for skill in range(n_skills)])


############
# internal #
############


def _hash_config(config: dict[str, Any]) -> str:
    config = _prepare_config_for_hashing(config)
    return hashlib.sha256(str(config).encode()).hexdigest()[:8]


def _prepare_config_for_hashing(config: Any) -> Any:
    if isinstance(config, dict):
        return {
            key: _prepare_config_for_hashing(config[key])
            for key in sorted(config)
            if key != "hash"
        }
    elif isinstance(config, list):
        return [_prepare_config_for_hashing(x) for x in config]
    else:
        return config
