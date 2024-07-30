import os

import click
import pandas as pd
from openai import OpenAI

from utils import get_embedding


def get_cosine_similarity(embedding1, embedding2):
    """Get the cosine similarity between two embeddings."""
    return sum(a * b for a, b in zip(embedding1, embedding2))


def get_top_n_related_strings(string, strings: pd.Series, n=10):
    """Get the top n related strings to the input embedding as a list"""
    embedding = get_embedding(string)
    similarities = strings.apply(
        lambda x: get_cosine_similarity(embedding, get_embedding(x))
    )
    return strings[similarities.argsort()[::-1][:n]].tolist()


@click.command()
@click.option(
    "--question",
    prompt="Please enter the question",
    help="The question to ask the model.",
)
def ask(question):
    client = OpenAI()
    if not os.path.exists("user_data.csv"):
        click.echo("user_data.csv does not exist.")
        return
    user_data = pd.read_csv("user_data.csv")
    related_strings = get_top_n_related_strings(question, user_data["content"])

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who answers concisely and directly."},
            {
                "role": "user",
                "content": f"Use the below notes to answer the question about my life, if the answer cannot be found in the notes please answer with I do not know {related_strings}, Question: {question} ",
            },
        ],
    )

    click.echo(completion.choices[0].message.content)
