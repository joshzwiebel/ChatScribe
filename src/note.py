import click
import os
import csv
import json
import datetime

from openai import OpenAI


def get_embedding(text):
    client = OpenAI()
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding


@click.command()
@click.option(
    "--filename",
    default="user_data.csv",
    help="The name of the file to save the input to.",
)
@click.option(
    "--content",
    prompt="Please enter the content",
    help="The content to write to the file.",
)
def save_input_to_file(content, filename):
    """This is a command line application that saves user input to a file."""
    # if the file does not exist put in a header
    if not os.path.exists(filename):
        with open(filename, "w") as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerow(["timestamp", "content", "embedding"])
    with open(filename, "a") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(
            [str(datetime.datetime.now()), content, json.dumps(get_embedding(content))]
        )
    click.echo(f"Successfully wrote to {filename}")
