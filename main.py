from bakery import assert_equal
from drafter import *
from dataclasses import dataclass



hide_debug_information()
set_website_title("Word counter")
set_website_framed(False)
set_site_information("Krutika", "Word count", ["LLM-Krutika"], ["CS1_Final_Project_ 1_ Design-Krutika","CS1_Final_Project 0_ Pick_Problem_Krutika"], ["https://github.com/kponnala-01/final_project_1"], server=None)



@dataclass
class State:
    texts: list[Text]
    longest_text: Text
    total_words: int
    average_word: int
    
@dataclass
class Text:
    text:str
    word_count:int

@route
def home_page(state: State)->Page:
    return index(state) #change later
@route
def text_display(state:State)->Page:
    return 1
    
    

@route
def index(state: State) -> Page:
    return Page(state,[
        Header("Word counter"),
        Button("compare","text_compare"),
        Button("Display", "text_display"),
        Button("enter text", "text_entry")
    ])
@route
def text_entry(state:State)->Page:
    return Page(state, [
        Header("Enter"),
        Button("Home", "index"),TextArea("name"),Button("Enter","enter")
        
    ])
@route
def text_compare(state:State)->Page:
    if len(state.texts[-1])>len(state.texts[-2]):
        state.longest_text=state.texts[-1]
    else:
        state.longest_text=state.texts[-2]
    return Page(state,[
        Button("Home","index"),TextArea("name", state.texts), TextArea("name2", state.texts), TextBox("long_text",state.longest_text)])
@route
def update(state:State, new_text:str, new_text2:str)->Page:
    state.texts.append(new_text)
    state.texts.append(new_text2)
    return index(state)
        

@route
def enter(state:State,name:str)->Page:
    words=name.split()
    if len(words)<=5000:
        count = len(words)
    else:
        count = 5000
    new_text = Text(name,count)
    state.texts.append(new_text)
    state.total_words += count
    average_word_count = state.total_words / len(state.texts)
    if state.longest_text == None:
        state.longest_text = new_text
    for text in state.texts:
        if text.word_count > state.longest_text.word_count:
            state.longest_text = text
    return text_entry(state)
    



start_server(State([],None,0,0))
