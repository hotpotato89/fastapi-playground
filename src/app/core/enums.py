from enum import Enum


class Genre(str, Enum):
    FANTASY = "fantasy"
    ADVENTURE = "adventure"
    DRAMA = "drama"
    SCIENCE = "science"
