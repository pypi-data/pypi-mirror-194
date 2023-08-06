[![Pipeline](https://gitlab.com/antoinelb/ktdg/badges/main/pipeline.svg)](https://gitlab.com/antoinelb/ktdg/commits/main)
[![coverage report](https://gitlab.com/antoinelb/ktdg/badges/main/coverage.svg)](https://gitlab.com/antoinelb/ktdg/commits/main)
[![Pypi version](https://img.shields.io/pypi/v/ktdg)](https://pypi.org/project/ktdg/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)

# ktdg (Knowledge tracing data generator)

Library used to create synthetic knowledge tracing data.
Example configs can be found in `config`.

[__Usage__](#usage)
| [__Setup__](#setup)
| [__Documentation__](#documentation)

## Usage

To create a new config or complete an existing one:

```
$ ktdg create --help
Usage: ktdg create [OPTIONS] CONFIG

  (c) Creates a config or completes it, saving it to the given file.

Arguments:
  CONFIG  Path of the config to complete or create  [required]

Options:
  -h, --help  Show this message and exit.
```

To generate the synthetic data from the config:

```
$ ktdg generate --help
Usage: ktdg generate [OPTIONS] CONFIG

  (g) Generates the data for the given config, saving it as a json file named
  "data.json".

Arguments:
  CONFIG  Configuration file to use  [required]

Options:
  -h, --help  Show this message and exit.
```

## Setup

1. Install [`poetry`](https://github.com/python-poetry/poetry)

2. `poetry config virtualenvs.in-project true`

3. `poetry install`

4. `source .venv/bin/activate`

## Documentation

### Generation

#### Skills

Skills are generated with the following parameters:

$n^K$ / `n`: number of skills to generate

`difficulty (float)`: by how much to scale question difficulties for questions needing this skill sampled from a distribution

`seed (int)`: random seed to use when generating the skills

#### Students

Students are generated with the following parameters:

`n`: number of students to generate

$n_i \sim N^S, n_i \in \{0,...,n^K\}$ / `n_skills (int)`: number of skills per student sampled from a distribution

$m_{ik} \sim M^Q, m_{ik} \in [0,1]$ / `skill_mastery (float)`: mastery for a given student and skill sampled from a distribution

$s_i^S \sim S^S, s_i^S \in [0,1]$ / `slip (float)`: slip rate for a given student sampled from a distribution

$g_i^S \sim G^S, g_i^S \in [0,1]$ / `guess (float)`: guess rate for a given student sampled from a distribution

$l_i^S \sim L^S, l_i^S \in [0,1]$ / `learning_rate (float)`: rate of learning for a given student sampled from a distribution

$f_i^S \sim F^S, f_i^S \in [0,1]$ / `forget_rate (float)`: rate of forgetting for a given student sampled from a distribution

`binary_learning (bool)`: if a skill should be considered known ($=1$) or not ($=0$) instead of being continuous between 0 and 1

`seed (int)`: random seed to use when generating the students

#### Questions

Questions are generated with the following parameters:

`n`: number of questions to generate

$n_j \sim N^Q, n_j \in \{0,...,n^K\}$ / `n_skills (int)`: number of skills per question sampled from a distribution

$m_{ik} \sim M^Q, m_{ik} \in [0,1]$ / `skill_mastery (float)`: mastery for a given question and skill sampled from a distribution

$d_j^Q \sim D^Q, d_j^Q \in [0,1]$ / `difficulty (float)`: difficulty for a given question sampled from a distribution

$s_j^Q \sim S^Q, s_j^Q \in [0,1]$ / `slip (float)`: slip rate for a given question sampled from a distribution

$g_j^Q \sim G^Q, g_j^Q \in [0,1]$ / `guess (float)`: guess rate for a given question sampled from a distribution

`seed (int)`: random seed to use when generating the questions

#### Answers

Answers are generated using the following formulas:

$$\boldsymbol{q}_j = \left(q_{jk}\right)_{k=1,...,n^K}$$

$$s_{ij} = 1 - \sqrt{(1 - s_i) \cdot (1 - s_j)}$$

$$g_{ij} = 1 - \sqrt{(1 - g_i) \cdot (1 - g_j)}$$

$$\boldsymbol{s}_i^0 = \left(s_{ik}\right)_{k=1,...,n^K}$$

$$\boldsymbol{s}_i^t = \underbrace{f_i \cdot \boldsymbol{s}_i^{t-1}}_{\text{skill forgetting}} + l_i \cdot \underbrace{(1 - g_a) \cdot (1 - g_{ij})}_{\text{adjustment for guessing}} \cdot \underbrace{(0.5 + d_j)}_{\text{adjustment for difficulty}} \cdot \underbrace{(1 - w_a \cdot (1 - a_i^t))}_{\text{adjustment for correctness}} \cdot \boldsymbol{q}_j$$

$$a_i^t = g_{ij} + (1 - s_{ij}) \cdot \frac{m_{ij}}{1 + m_{ij}}$$

$$m_{ij} = \exp\left(m_a \cdot (\boldsymbol{q}_j^T\boldsymbol{s}_i^t - d_j)\right)$$


for question $j$ asked at time $t$ and with the following parameters:

$n_i^A \sim N^A, n_i^A \in \mathbb{N}$ / `n_per_student (int)`: number of questions asked per student sampled from a distribution

$w_a \in \mathbb{R}^+$ / `wrong_answer_adjustment (float)`: by how much should the learning be scaled for a wrong answer

$g_a \in \mathbb{R}^+$ / `guess_adjustment (float)`: by how much should the learning be scaled proportional to the guess parameter

$m_a \in \mathbb{R}^+$ / `mastery_importance (float)`: by how much should the mastery importance part in the exponential be scaled by

`max_repetitions (int)`: maximum number of repetition of a given question allowed per student

`can_repeat_correct (bool)`: if a question answered correctly can be repeated

`seed (int)`: random seed to use when generating the answers

### Distributions

__constant__: All samples have the same value `value`.

__normal__: Samples are taken from a normal distribution with mean `mu` and standard deviation `sigma`.

__binomial__: Samples are taken from a binomial distribution with number of possible successes `n` and probability of success `p`.
