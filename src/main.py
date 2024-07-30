import os

import click
import openai

import note
import ask

# Set your OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")


@click.group()
def cli():
    pass


cli.add_command(note.save_input_to_file)
cli.add_command(note.read_my_data)
cli.add_command(ask.ask)

if __name__ == "__main__":
    cli()
    # note.save_input_to_file(["--content", "Hello, World!"])
