from bakery import assert_equal
from drafter import *
from dataclasses import dataclass



hide_debug_information()
set_website_title("Word counter")
set_website_framed(False)



@dataclass
class State:
    list: list[str]
    list_two: list[str]
    longest_text: list[str]
    Total_words: int
    Average_word: int


@route
def index(state: State) -> Page:
    return Page(state, ["Hello World!"])

assert_equal(index(State()), Page(State(), ["Hello World!"]))

start_server(State())
