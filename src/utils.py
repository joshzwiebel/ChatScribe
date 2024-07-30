from openai import OpenAI


def get_embedding(text):
    client = OpenAI()
    response = client.embeddings.create(
        model="text-embedding-3-small", input=text, dimensions=512
    )
    return response.data[0].embedding
