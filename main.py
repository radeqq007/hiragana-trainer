from rich.console import Console
from rich.table import Table
from InquirerPy import inquirer
import os
import json
import random

console = Console()

chars = {
  # Vowels
  "a": "あ",
  "i": "い",
  "u": "う",
  "e": "え",
  "o": "お",

  # K-row
  "ka": "か",
  "ki": "き",
  "ku": "く",
  "ke": "け",
  "ko": "こ",

  # S-row
  "sa": "さ",
  "shi": "し",
  "su": "す",
  "se": "せ",
  "so": "そ",

  # T-row
  "ta": "た",
  "chi": "ち",
  "tsu": "つ",
  "te": "て",
  "to": "と",

  # N-row
  "na": "な",
  "ni": "に",
  "nu": "ぬ",
  "ne": "ね",
  "no": "の",

  # H-row
  "ha": "は",
  "hi": "ひ",
  "fu": "ふ",
  "he": "へ",
  "ho": "ほ",

  # M-row
  "ma": "ま",
  "mi": "み",
  "mu": "む",
  "me": "め",
  "mo": "も",

  # Y-row
  "ya": "や",
  "yu": "ゆ",
  "yo": "よ",

  # R-row
  "ra": "ら",
  "ri": "り",
  "ru": "る",
  "re": "れ",
  "ro": "ろ",

  # W-row
  "wa": "わ",
  "wo": "を",

  # N
  "n": "ん"
}

enabled_chars = list()

STORAGE_FILE = "enabled_chars.json"

def save_state():
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(enabled_chars, f, ensure_ascii=False, indent=2)

def load_state():
    global enabled_chars
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r", encoding="utf-8") as f:
            enabled_chars = json.load(f)


def start():
    if not enabled_chars:
        console.print("[red]No characters are enabled![/red]")
        console.input("Press any key to continue...")
        menu()
        return

    while True:
        char = random.choice(enabled_chars)
        console.print(f"What is the romanji for {chars[char]}?")
        answer = console.input()
        if answer == char:
            console.print("Correct!")
        else:
            console.print(f"Wrong! The correct answer is {char}")
            
        console.print("Press any key to continue...")
        console.input()
        console.clear()

def display_hiragana_table():
    table = Table()
    table.add_column("Hiragana")
    table.add_column("Romanji")
    for char in chars:
        table.add_row(chars[char], char)
    console.print(table)
    console.print("Press any key to continue...")
    console.input()
    menu()

def disable_characters():
    global enabled_chars
    choices = [
        {"name": f"{chars[c]} ({c})", "value": c, "enabled": c in enabled_chars}
        for c in chars.keys()
    ]
    selected = inquirer.checkbox(
        message="Select characters to disable:",
        choices=choices,
        instruction="Use arrows + space to toggle, Enter to confirm",
        cycle=True
    ).execute()
    
    enabled_chars = [c for c in chars.keys() if c in selected]

    save_state()

    console.print(f"[green]Enabled characters updated![/green]")
    console.print("Press any key to continue...")
    console.input()
 
    menu()
        

def menu():
    console.clear()
    option = inquirer.select(
        message="Select an option: ",
        choices=[
            "Start",
            "Disable Characters",
            "Display Hiragana Table",
            "Exit"
        ],
        cycle=True
    ).execute()

    if option == "Start":
        start()
    elif option == "Disable Characters":
        disable_characters()
    elif option == "Display Hiragana Table":
        display_hiragana_table()
    elif option == "Exit":
        exit()
    else:
        console.print("Invalid option")


def main():
    global enabled_chars
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, "r", encoding="utf-8") as f:
                enabled_chars = json.load(f)
        except json.JSONDecodeError:
            enabled_chars = list(chars.keys())
    else:
        enabled_chars = list(chars.keys())

    menu()
            

if __name__ == "__main__":
    main()