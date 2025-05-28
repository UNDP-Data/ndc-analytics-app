"""
Functions for interacting with generative models from Azure OpenAI Service.
"""

import json
import os

from openai import AzureOpenAI, Stream

from .entities import Message
from .utils import read_prompts


def get_client() -> AzureOpenAI:
    """
    Get an Azure OpenAI Client object.

    Returns
    -------
    AzureOpenAI
        Azure OpenAI Client object.
    """
    client = AzureOpenAI(
        api_version="2024-02-15-preview",
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_KEY"],
    )
    return client


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Embed texts using an ada model from OpenAI.

    Parameters
    ----------
    texts : list[str]
        List of texts to embed.

    Returns
    -------
    list[list[float]]
        List of text embeddings.
    """
    client = get_client()
    response = client.embeddings.create(
        input=texts,
        model="text-embedding-ada-002",
    )
    return [result.embedding for result in response.data]


def get_response(
    messages: list[Message],
    system_message: str = "You are a helpful assistant",
    stream: bool = False,
) -> str | Stream:
    """
    Get a response from gpt-4o-mini using Azure OpenAI.

    Messages are ordered internally by timestamp.

    Parameters
    ----------
    messages : list[Message]
        A list of Message objects to include as history.
    system_message : str, optional
        System message to customise the behaviour of the model.
    stream : bool, default=False
        Whether to stream the response.

    Returns
    -------

    """
    client = get_client()
    messages = [
        message.model_dump(include={"role", "content"}, by_alias=True)
        for message in sorted(messages)
    ]
    messages.insert(0, {"role": "system", "content": system_message})
    response = client.chat.completions.create(
        model="gpt4o-mini-public",  # "gpt-4o-mini"
        messages=messages[:10],  # 10 last messages only
        temperature=0.0,
        stream=stream,
    )
    if not stream:
        response = response.choices[0].message.content
    return response


def paraphrase(user_message: str, messages: list[Message]) -> str:
    """
    Paraphrase a user message to use it as a query for text search.

    Parameters
    ----------
    user_message : str
        User message.
    messages : list[Message]
        List of Message objects to include as history for additional context.

    Returns
    -------

    """
    prompts = read_prompts()
    system_message = prompts["paraphrase"]
    messages = messages + [Message(role="user", content=user_message)]
    response = get_response(messages, system_message, stream=False)
    return response


def ask_model(
    user_message: str, messages: list[Message], contexts: list[dict]
) -> Stream:
    """
    Send a user message to an Azure OpenAI model together with contexts for RAG.

    Parameters
    ----------
    user_message : str
        User message.
    messages : list[Message]
        List of Message objects to include as history for additional context.
    contexts : list[dict]
        List of contexts for RAG, expected to contain "source" and "text" keys.

    Returns
    -------
    Stream
        Model response as a Stream.
    """
    prompts = read_prompts()
    system_message = prompts["rag"].format(contexts=json.dumps(contexts, indent=4))
    messages = messages + [Message(role="user", content=user_message)]
    response = get_response(messages, system_message, stream=True)
    return response
