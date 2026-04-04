import json
from login_screen import start_app
from main import runTest

with open("settings.json", "r", encoding="utf-8") as file:
    settings = json.load(file)

if settings["logged"] is True:
    runTest()
else:
    if __name__ == "__main__":
        start_app() 