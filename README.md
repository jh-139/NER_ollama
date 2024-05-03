# Named Entity Recognition (NER) using Large language models (LLMs)

## Using LLM to get the model to perform NER task
This project showcases how with prompt engineering and selecting the correct LLM model, use LLMfor NER task, as compared to using the conventional approach of using neural networks.

First ask a prompt to the LLM, providing the text in the prompt for the LLM to analyse.
Next, use regular expression to extract the company names, which may come in various variants. Examples: '1. Apple', '-Apple',  '*Apple' . 
For each of the company name identified by the LLM, use semantic search match the name with the list of company names in our sample.

## Textual Data source
 - Youtube transcripts from channels like: Wall Street Journal, 'CNBCtelevision'
 - Metadata for each video collected using Youtube Data API
 - Transcript text collected using Youtube Transcript API 

## Models 
- LLMs from Ollama
- textual embeddings and cross encoders from sbert library

## Tweak this project for your own uses

Sample codes are provided in 'samples' .
