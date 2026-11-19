
from drafter import *
from dataclasses import dataclass


hide_debug_information()
set_website_title("Word counter")
set_website_framed(False)
set_site_information(
    "Krutika",
    "Word count",
    ["LLM-Krutika"],
    ["CS1_Final_Project_1_Design-Krutika",
     "CS1_Final_Project_0_Pick_Problem_Krutika"],
    ["https://github.com/kponnala-01/final_project_1"],
    server=None
)


@dataclass
class TextData:
    text: str
    word_count: int


@dataclass
class State:
    texts: list[TextData]
    longest_text: TextData
    total_words: int
    average_word: float


@route
def home_page(state: State) -> Page:
    return Page(state, [
        Header("Home page"),
        Button("Home", "index")
    ])


@route
def index(state: State) -> Page:
    return Page(state, [
        Header("Word counter"),
        Button("Compare", "text_compare"),
        Button("Display", "text_display"),
        Button("Enter text", "text_entry")
    ])


@route
def text_entry(state: State) -> Page:
    if len(state.texts) == 0:
        return Page(state, [
            Header("Enter First Text"),
            Button("Home", "index"),
            TextArea("name"),
            Button("Enter", "enter")
        ])

    elif len(state.texts) == 1:
        return Page(state, [
            Header("Enter Second Text"),
            Button("Home", "index"),
            TextArea("new_text2"),
            Button("Enter", "update")
        ])

    else:
        return text_display(state)


@route
def text_display(state: State) -> Page:
    if len(state.texts) < 2:
        return Page(state, [
            Header("Display"),
            Text("Please enter both texts first."),
            Button("Home", "index")
        ])

    return Page(state, [
        Header("Texts Being Compared"),
        Button("Home", "index"),

        Header("First Text"),
        Text(state.texts[0].text),
        Text("Word Count: " + str(state.texts[0].word_count)),

        Header("Second Text"),
        Text(state.texts[1].text),
        Text("Word Count: " + str(state.texts[1].word_count)),

        Button("Compare Texts", "text_compare")
    ])


@route
def text_compare(state: State) -> Page:
    if len(state.texts) < 2:
        return Page(state, [
            Header("Compare"),
            Text("Please enter both texts first."),
            Button("Home", "index"),
            Button("Enter text", "text_entry")
        ])

    if state.texts[0].word_count > state.texts[1].word_count:
        state.longest_text = state.texts[0]
    else:
        state.longest_text = state.texts[1]

    return Page(state, [
        Header("Compare"),
        Button("Home", "index"),

        Text("First Text:"),
        Text(state.texts[0].text),

        Text("Second Text:"),
        Text(state.texts[1].text),

        Header("Longest Text:"),
        Text(state.longest_text.text),
        Text("Word Count: " + str(state.longest_text.word_count))
    ])


@route
def enter(state: State, name: str) -> Page:
    if len(state.texts) >= 2:
        return text_display(state)

    words = name.split()
    count = min(len(words), 5000)

    new_text = TextData(name, count)
    state.texts.append(new_text)

    state.total_words += count
    state.average_word = state.total_words / len(state.texts)

    if state.longest_text == None:
        state.longest_text = new_text
    elif new_text.word_count > state.longest_text.word_count:
        state.longest_text = new_text

    return text_entry(state)


@route
def update(state: State, new_text2: str) -> Page:
    if len(state.texts) != 1:
        return text_entry(state)

    words = new_text2.split()
    count = min(len(words), 5000)

    second_text = TextData(new_text2, count)
    state.texts.append(second_text)

    state.total_words += count
    state.average_word = state.total_words / len(state.texts)

    return text_compare(state)


start_server(State([], None, 0, 0))



