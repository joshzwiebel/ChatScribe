import click
import note
import openai
import os

# Set your OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")


@click.group()
def cli():
    pass


cli.add_command(note.save_input_to_file)
cli.add_command(note.read_my_data)

if __name__ == "__main__":
    cli()
    # note.save_input_to_file(["--content", "Hello, World!"])
