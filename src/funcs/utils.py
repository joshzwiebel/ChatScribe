import pandas as pd
from openai import OpenAI


def get_embedding(text):
    client = OpenAI()
    response = client.embeddings.create(
        model="text-embedding-3-small", input=text, dimensions=512
    )
    return response.data[0].embedding


def get_cosine_similarity(embedding1, embedding2):
    """Get the cosine similarity between two embeddings."""
    return sum(a * b for a, b in zip(embedding1, embedding2))


def get_top_n_related_strings(string, strings: pd.Series, n=3):
    """Get the top n related strings to the input embedding as a list"""
    embedding = get_embedding(string)
    similarities = strings.apply(
        lambda x: get_cosine_similarity(embedding, get_embedding(x))
    )
    return strings[similarities.argsort()[::-1][:n]].tolist()
