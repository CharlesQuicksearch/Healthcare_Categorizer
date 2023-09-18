from fastapi import FastAPI, HTTPException
import re

from request_and_response import Response, Request
from vocabulary import custom_vocabulary

app = FastAPI()

@app.get("/")
def home():
    return "Categorization. Send a json with a string to categorize. Ex: '{'input': 'Läkare är trevliga'}"

@app.post("/categorize/", response_model=Response)
async def categorize(request_data: Request):
    try:
        output = categorize(request_data.input)
        return Response(output = output)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def categorize(text):
    tokens = re.findall(r'\b\w+\b', text.lower())
    mapped_tokens = []

    for token in tokens:
        for common_word, synonyms in custom_vocabulary.items():
            if common_word not in mapped_tokens and token in synonyms:
                mapped_tokens.append(common_word)
                break

    return mapped_tokens
