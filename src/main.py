import click
import openai
import os

# Set your OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

@click.group()
def cli():
    pass





@cli.command(help="saves input to a file")
@click.option('--filename', prompt='Please enter the filename', help='The name of the file to save the input to.')
@click.option('--content', prompt='Please enter the content', help='The content to write to the file.')
def save_input_to_file(filename, content):
    """This is a command line application that saves user input to a file."""
    if os.path.exists(filename):
        click.echo(f'File {filename} already exists.')
        with open(filename, 'a') as file:
            file.write(content)
    else:
        with open(filename, 'w') as file:
            file.write(content)
        click.echo(f'Successfully wrote to {filename}')

if __name__ == '__main__':
    cli()
