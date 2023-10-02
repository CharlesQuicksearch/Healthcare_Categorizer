import json
import re
import uvicorn

from Config_Logger import logger
from Config_Logger.logger import logging
from fastapi import FastAPI, HTTPException
from request_and_response import Response, Request
from vocabulary import healthcare_vocabulary, golf_vocabulary

app = FastAPI()

logger.config_logger()

@app.get("/home")
def home():
    return "Categorization. Send a json with a string to categorize. Ex: '{'input': 'Läkare är trevliga'} to /categorize/healthcare or /categorize/golf"


@app.post("/categorize/healthcare", response_model=Response)
async def categorize(request_data: Request):
    try:
        logging.info(f"Request Categorize Healthcare: {request_data.input}")
        output = categorize(request_data.input, healthcare_vocabulary)
        logging.info(f"200 {output}")

        return Response(output=output)

    except Exception as e:
        logging.error(f"500 {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/categorize/golf", response_model=Response)
async def categorize(request_data: Request):
    try:
        logging.info(f"Request Categorize Golf: {request_data.input}")
        output = categorize(request_data.input, golf_vocabulary)
        logging.info(f"200 {output}")

        return Response(output=output)

    except Exception as e:
        logging.error(f"500 {e}")
        raise HTTPException(status_code=500, detail=str(e))


def categorize(text, vocabulary):
    tokens = re.findall(r'\b\w+\b', text.lower())
    mapped_tokens = []

    for token in tokens:
        for common_word, synonyms in vocabulary.items():
            if common_word not in mapped_tokens and token in synonyms:
                mapped_tokens.append(common_word)
                logging.info(f"Added {common_word}")
                break

    return mapped_tokens


if __name__ == "__main__":
    with open("config.json", "r") as f:
        config = json.load(f)
    uvicorn.run(app, host=config.get("host"), port=int(config.get("port")))
