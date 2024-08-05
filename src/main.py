import csv
import datetime
import json
import os

import openai
import pandas as pd
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.logger import Logger, LOG_LEVELS
from openai import OpenAI

from funcs.utils import get_embedding, get_top_n_related_strings

# Set your OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")
class ChatScribe(App):
    def build(self):
        layout = BoxLayout(orientation="vertical")
        self.label = Label(text="Test Label")
        self.label.size_hint_y = 0.7
        button = Button(text="Read my data")
        button.size_hint_y = 0.2
        button.bind(on_press=self.on_press_button)
        layout.add_widget(self.label)
        layout.add_widget(button)
        Logger.info("The app has been built")
        return layout

    def on_press_button(self,other):
        Logger.setLevel(LOG_LEVELS["debug"])
        self.label.text = self.read_my_data()

    def save_input_to_file(self, content, filename):
        """This is a command line application that saves user input to a file."""
        # if the file does not exist put in a header
        if not os.path.exists(filename):
            with open(filename, "w") as file:
                writer = csv.writer(file, delimiter=",")
                writer.writerow(["timestamp", "content", "embedding"])
        with open(filename, "a") as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerow(
                [
                    str(datetime.datetime.now()),
                    content,
                    json.dumps(get_embedding(content)),
                ]
            )
        return f"Successfully wrote to {filename}"

    def read_my_data(self):
        """This is a command line application that reads user data from a file."""
        filename = "user_data.csv"
        Logger.debug("in the function")
        if not os.path.exists(filename):
            print(f"{filename} does not exist.")
            return "No data"
        user_data = pd.read_csv(filename)
        return user_data[["content", "timestamp"]].to_markdown()

    def ask(self, question):
        client = OpenAI()
        if not os.path.exists("user_data.csv"):
            print("user_data.csv does not exist.")
            return
        user_data = pd.read_csv("user_data.csv")
        related_strings = get_top_n_related_strings(question, user_data["content"])

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant who answers concisely and directly.",
                },
                {
                    "role": "user",
                    "content": f"Use the below notes to answer the question about my life, if the answer cannot be found in the notes please answer with I do not know {related_strings}, Question: {question} ",
                },
            ],
        )

        return completion.choices[0].message.content


if __name__ == "__main__":
    # cli()
    ChatScribe().run()
    # note.save_input_to_file(["--content", "Hello, World!"])
