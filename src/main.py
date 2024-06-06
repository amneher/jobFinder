# entrypoint, app(), call db connect, api routes.
import os
from flask import Flask
from dotenv import load_dotenv
import weaviate
from weaviate.embedded import EmbeddedOptions

load_dotenv()

client = weaviate.Client(
    embedded_options=EmbeddedOptions(),
    additional_headers={
        "X-OpenAI-Api-Key": os.environ[
            "OPENAI_APIKEY"
        ]  # Replace with your inference API key
    },
)


def init_weaviate():
    if client.schema.exists("Profile"):
        client.schema.delete_class("Profile")
    profile_class_obj = {
        "class": "Profile",
        "vectorizer": "text2vec-openai",  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
        "moduleConfig": {
            "text2vec-openai": {},
            "generative-openai": {},  # Ensure the `generative-openai` module is used for generative queries
        },
    }
    if client.schema.exists("Skill"):
        client.schema.delete_class("Skill")
    skill_class_obj = {
        "class": "Skill",
        "vectorizer": "text2vec-openai",  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
        "moduleConfig": {
            "text2vec-openai": {},
            "generative-openai": {},  # Ensure the `generative-openai` module is used for generative queries
        },
    }
    if client.schema.exists("Resume"):
        client.schema.delete_class("Resume")
    resume_class_obj = {
        "class": "Resume",
        "vectorizer": "text2vec-openai",  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
        "moduleConfig": {
            "text2vec-openai": {},
            "generative-openai": {},  # Ensure the `generative-openai` module is used for generative queries
        },
    }
    if client.schema.exists("User"):
        client.schema.delete_class("User")
    user_class_obj = {
        "class": "User",
        "vectorizer": "text2vec-openai",  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
        "moduleConfig": {
            "text2vec-openai": {},
            "generative-openai": {},  # Ensure the `generative-openai` module is used for generative queries
        },
    }
    if client.schema.exists("JobSeeker"):
        client.schema.delete_class("JobSeeker")
    job_seeker_class_obj = {
        "class": "JobSeeker",
        "vectorizer": "text2vec-openai",  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
        "moduleConfig": {
            "text2vec-openai": {},
            "generative-openai": {},  # Ensure the `generative-openai` module is used for generative queries
        },
    }

    client.schema.create(
        {
            "classes": [
                profile_class_obj,
                skill_class_obj,
                resume_class_obj,
                user_class_obj,
                job_seeker_class_obj,
            ]
        }
    )


app = Flask(__name__)

def start():
    API_PORT_STR = os.environ.get("API_PORT", default=None)
    API_PORT = int(API_PORT_STR) if API_PORT_STR is not None else None
    app.run(port=API_PORT)

if __name__ == "__main__":
    start()