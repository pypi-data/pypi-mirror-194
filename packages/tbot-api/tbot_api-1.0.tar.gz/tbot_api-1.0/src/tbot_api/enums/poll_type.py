from enum import Enum


class PollType(str, Enum):
    REGULAR = "regular"
    QUIZ = "quiz"
