import csv
import datetime
import json
import os

import click
import pandas as pd

from utils import get_embedding


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


@click.command()
def read_my_data():
    """This is a command line application that reads user data from a file."""
    filename = "user_data.csv"
    if not os.path.exists(filename):
        click.echo(f"{filename} does not exist.")
        return
    user_data = pd.read_csv(filename)
    click.echo(user_data[["content", "timestamp"]])
