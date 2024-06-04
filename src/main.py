# entrypoint, app(), call db connect, api routes.
import os
import json
from flask import Flask
from dotenv import load_dotenv
import weaviate
from weaviate.embedded import EmbeddedOptions

load_dotenv()

client = weaviate.Client(
    embedded_options=EmbeddedOptions(),
    additional_headers = {
        "X-OpenAI-Api-Key": os.environ["OPENAI_APIKEY"]  # Replace with your inference API key
    }
)

def init_weaviate():
    if client.schema.exists("Question"):
        client.schema.delete_class("Question")
    class_obj = {
        "class": "Question",
        "vectorizer": "text2vec-openai",  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
        "moduleConfig": {
            "text2vec-openai": {},
            "generative-openai": {}  # Ensure the `generative-openai` module is used for generative queries
        }
    }

    client.schema.create_class(class_obj)


app = Flask(__name__)
