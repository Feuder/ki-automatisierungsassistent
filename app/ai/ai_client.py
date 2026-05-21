from config.settings import get_api_key, get_model
from ai.prompts.prompt_reader import zusammenfassenprompt, task_erstellenpromt
import logging
from openai import OpenAI

client = None
gptmodel = None

def get_client():
    global client 

    if client is None:
        client = OpenAI(api_key = get_api_key())

    return client

def get_model_env():
    global gptmodel

    if gptmodel is None:
        gptmodel = get_model()

    return gptmodel

def KI_anfrage(inhalt):
    
    prompt = str(zusammenfassenprompt())

    try:
        client = get_client()

        response = client.responses.create(
            model=get_model_env(),
            instructions=prompt,
            input=inhalt
        )

        return response.output_text
    
    except Exception as f:
        print("Es gab ein Fehler bei dem OpenAI API Aufruf:\n")
        logging.error("Es gab ein Fehler bei dem OpenAI-API Aufruf\n")
        print(f)
        logging.error(f)
        raise SystemExit
    
def ki_task_erstellen(inhalt):

    prompt = str(task_erstellenpromt())

    try:
        client = get_client()

        response = client.responses.create(
            model=get_model_env(),
            instructions=prompt,
            reasoning={"effort": "low"},
            input=inhalt
        )

        return response.output_text

    except Exception as f:  
        print("Es gab ein Fehler bei dem OpenAI API Aufruf:\n")
        logging.error("Es gab ein Fehler bei dem OpenAI-API Aufruf\n")
        print(f)
        logging.error(f)
        raise SystemExit