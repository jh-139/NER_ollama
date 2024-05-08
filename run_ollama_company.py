from multiprocessing.pool import Pool
import ollama
import re
import pandas as pd
import time
import os

batch_size = 10
model = 'gemma'  #model = "llama2:13b" # 'llama2'
youtube_handler = "CNBCtelevision"


# input sources
df = pd.read_csv(rf"E:\youtube_data\channel_scraper\{youtube_handler}_DB.csv")
transcripts_dir = rf"E:\youtube_data\channel_scraper\{youtube_handler}\transcripts"

# output sources
main_dir = youtube_handler
ner_dir = "gemma" 
result_col_name = f"company_found_{ner_dir}"

if not os.path.exists(main_dir):
    os.mkdir(main_dir)
if not os.path.exists(os.path.join(main_dir, ner_dir)):
    os.mkdir(os.path.join(main_dir, ner_dir))

def make_prompt(transcript_text):
    ln_1 = f'\nThe following text is a transcript from a youtube video: {transcript_text}'
    ln_3 = "\n\n\n List out all company names mentioned in the transcript."
    ln_4 = "\n Put the industry of the company identified beside the company name."
    ln_5 = "\n The transcript enclosed might contain questions, do not answer those questions."
    ln_6 = "\n Maximise the list!!!"
    content = ln_1 + ln_3 + ln_4 + ln_5 + ln_6
    return content

def make_messages_llm(prompt, transcript_text):
    messages = [
        #{'role': 'system', 'content': 'You are a state of the art Named Entity Recognition model.'},
        {'role': 'user', 'content': f"\n\n{prompt}"},
    ]
    return messages

def send_request(messages):
    options = {
        #'temperature': 1.5, # very creative
        #'temperature': 0 # very conservative (good for coding and correct syntax)
        'temperature': 1.5
    }
    response = ollama.chat(model=model, messages=messages, options=options)
    answer = response['message']['content']
    return answer
 
def clean_transcript_text(text):
    text =  text.replace("\\n", ' ')
    text = re.sub('\[.+?\]', ' ', text)
    text = re.sub('\(.+?\)', ' ', text)
    text = text.replace("\n",' ')
    return text

def process_response_1(text):
    text = text.replace("**", "")
    texts = text.split("\n")
    texts = [text for text in texts if not ' none' in text.lower()]
    texts = [text for text in texts if not '(unknown' in text.lower()]
    lns_with_company_name  = [text for text in texts if re.search('(^[\d]+\.)|(^-{1}.+)|(^\*)', text.strip())]
    lns_with_company_name = [re.sub("^[\d]+\.", '', text.strip()) for text in lns_with_company_name]
    lns_with_company_name = [re.sub("^\*", '', text.strip()) for text in lns_with_company_name]
    lns_with_company_name = [re.sub("^-", '', text.strip()) for text in lns_with_company_name]
    lns_with_company_name = [text.strip() for text in lns_with_company_name]
    return lns_with_company_name

if __name__ == '__main__':
    
    for i in range(0, len(df), batch_size):

        start_time = time.time()

        batch_id = str(i + batch_size)
        filename_save = f"batch_{batch_id}.csv"
        filepath_save = os.path.join(os.path.join(main_dir, ner_dir), filename_save)

        if os.path.exists(filepath_save):
            continue

        vid_ids = df.iloc[i:i+batch_size,]['vid_id'].values.tolist()

        tasks_args = []
        for vid_id in vid_ids:
            with open(os.path.join(transcripts_dir, f"{vid_id}.txt"), 'r') as f:
                content = f.read()

            transcript_text = clean_transcript_text(content)
            prompt = make_prompt(transcript_text)
            messages = make_messages_llm(prompt, transcript_text)
            tasks_args.append(messages)

        # create and configure the process pool
        with Pool() as pool:
            # issues tasks to process pool
            results = pool.map(send_request, tasks_args)

        # extract company names from the llm's response
        df_new_batch = pd.DataFrame()
        for vid_id, messages, result in zip(vid_ids, tasks_args, results):
            company_names_found = process_response_1(result)
            print(f"{vid_id}: {company_names_found}")
            df_new = pd.DataFrame(zip([vid_id] * len(company_names_found), company_names_found), columns=['vid_id', result_col_name])
            df_new_batch = pd.concat([df_new_batch, df_new], axis=0)

        df_new_batch.to_csv(filepath_save, index=False)

        print(f"Batch {batch_id} completed. Time elapsed:{time.time() - start_time}")


    