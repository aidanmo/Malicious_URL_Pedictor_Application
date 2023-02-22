
import uvicorn

import pickle

import os

import tldextract

import re

from urllib.parse import urlparse

import urllib.parse

from pydantic import BaseModel, validator, ValidationError

from fastapi import FastAPI, HTTPException

from fastapi.middleware.cors import CORSMiddleware

import url_extractor as urlex

import url_features as urlfe

import validators


app = FastAPI()

origins = [

"http://localhost.tiangolo.com",

"https://localhost.tiangolo.com",

"http://localhost",

"http://localhost:8080",

"http://localhost:3000",

]

app.add_middleware(

CORSMiddleware,

allow_origins=origins,

allow_credentials=True,

allow_methods=["*"],

allow_headers=["*"],

)



model = pickle.load(open('/Users/aidanmorrison/Desktop/predictive/maliciousUrl.pkl', 'rb'))


class URL(BaseModel):
    url: str


def extract_features(url: str) -> dict:

    hostname, domain, path = urlex.get_domain(url)
    extracted_domain = tldextract.extract(url)
    domain = extracted_domain.domain+'.'+extracted_domain.suffix
    subdomain = extracted_domain.subdomain
    tmp = url[url.find(extracted_domain.suffix):len(url)]
    pth = tmp.partition("/")
    path = pth[1] + pth[2]
    words_raw, words_raw_host, words_raw_path= urlex.words_raw_extraction(extracted_domain.domain, subdomain, pth[2])
    tld = extracted_domain.suffix
    parsed = urlparse(url)
    scheme = parsed.scheme


    features = {}

    # extraction codes
    features['length_url'] = urlfe.url_length(url)
    features['length_hostname'] = urlfe.url_length(hostname)
    features['length_words_raw'] = urlfe.length_word_raw(words_raw)
    features['char_repeat'] = urlfe.char_repeat(words_raw)
    features['shortest_words_raw'] = urlfe.shortest_word_length(words_raw)
    features['shortest_word_host'] = urlfe.shortest_word_length(words_raw_host)
    features['shortest_word_path'] = urlfe.shortest_word_length(words_raw_path)
    features['longest_words_raw'] = urlfe.longest_word_length(words_raw)
    features['longest_word_host'] = urlfe.longest_word_length(words_raw_host)
    features['longest_word_path'] = urlfe.longest_word_length(words_raw_path)
    features['avg_words_raw'] = urlfe.average_word_length(words_raw)
    features['avg_word_host'] = urlfe.average_word_length(words_raw_host)
    features['avg_word_path'] = urlfe.average_word_length(words_raw_host)
    features['phish_hints'] = urlfe.phish_hints(url)
    features['https_token'] = urlfe.https_token(scheme)
    features['nb_hyphens'] = urlfe.count_hyphens(url)

    return features



@app.get("/")

def read_root():

    return {"data": "Welcome to online malicious URL identifier"}


@app.post("/prediction/")

async def get_predict(data: URL):
    
    try:
        url_features = extract_features(data.url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    sample = [[
        url_features.get('length_url', 0),
        url_features.get('length_hostname', 0),
        url_features.get('length_words_raw', 0),
        url_features.get('char_repeat', 0),
        url_features.get('shortest_words_raw', 0),
        url_features.get('shortest_word_host', 0),
        url_features.get('shortest_word_path', 0),
        url_features.get('longest_words_raw', 0),
        url_features.get('longest_word_host', 0),
        url_features.get('longest_word_path', 0),
        url_features.get('avg_words_raw', 0),
        url_features.get('avg_word_host', 0),
        url_features.get('avg_word_path', 0),
        url_features.get('phish_hints', 0),
        url_features.get('https_token', 0),
        url_features.get('nb_hyphens', 0)
    ]]

    prediction = model.predict(sample).tolist()[0]

    return {

    "data": {
    'prediction': prediction,
    'interpretation': 'The URL provided is safe.' if prediction == 'legitimate' else 'The URL provided is malicious.'
    }

    }

if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')
