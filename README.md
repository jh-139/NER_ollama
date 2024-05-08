# Named Entity Recognition (NER) using Large language models (LLMs)

## Using LLM to get the model to perform NER task
This project attempts to make use of LLMs to perform NER task, instead of the conventional approach of using neural networks.

First ask a prompt to the LLM, providing the text in the prompt for the LLM to analyse.
Next, use regular expression to extract the company names. Reponse of LLMs may come in various forms. Examples: '1. Apple', '-Apple',  '*Apple' . 
For each of the company name identified by the LLM, use semantic search match the name with the list of company names in our sample.

## Textual Data source
 - Youtube transcripts from channels like: Wall Street Journal, 'CNBCtelevision'
 - Transcript text collected using Youtube Transcript API 
 - Metadata for each video collected using Youtube Data API

## Models 
- Gemma via Ollama
- Textual embedding, cross encoders models and vector search engine by sbert 

## Using the code in this project for your own uses

- Sample codes are provided in 'samples' .
- Exploratory Data Analysis on the NER results are in 'eda' .

## Limitation/Improvements

- Terms "FANG companies", "Big Oil", "Big Pharma" are not identified by the language models, though this can be circumvented by prompt engineering and by compiling a list of all such terms.
- The semantic search step caused quite a few false positive cases. Perhaps this would require fine-tuning a dedicated embedding, cross encoder model for the task of disambiguating the entities.
- Involve LLM on the semantic search, i.e use the semantic search to retrieve top k similar companies and ask the LLM to decide which one is a better match.
