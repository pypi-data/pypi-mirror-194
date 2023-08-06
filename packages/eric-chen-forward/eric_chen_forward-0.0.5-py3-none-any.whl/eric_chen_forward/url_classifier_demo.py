from eric_chen_forward import util
import streamlit as st
import pickle
import requests
from bs4 import BeautifulSoup
import pandas as pd
from trafilatura import fetch_url, extract
from trafilatura.settings import use_config
from transformers import AutoTokenizer, BartForConditionalGeneration

def Demo(max_summary_length=100):
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)

    def extract_paragraphs(url, use_trafilatura=False):
        if use_trafilatura:
            config = use_config()
            config.set("DEFAULT", "EXTRACTION_TIMEOUT", "0")
            downloaded = fetch_url(url)
            result = extract(downloaded, config=config)
            return result
        else:
            data = requests.get(url).text
            soup = BeautifulSoup(data, 'lxml')
            h = soup.find('header')
            if h:
                h.decompose()
            f = soup.find('footer')
            if f:
                f.decompose()
            if soup.body is None:
                return None
            
            paragraphs = []
            for p in soup.find_all('p'):
                if len(p) > 0 and 'block' not in p:
                    text = p.get_text(strip=True, separator='\n')
                    if len(paragraphs) > 0 and len(paragraphs[-1].split()) < 100:
                        paragraphs[-1] += text
                    else:
                        paragraphs.append(text)
            return paragraphs



    title = st.text_input(label="Enter url", placeholder='url')

    tab1, tab2, tab3, tab4 = st.tabs(['BeautifulSoup', 'Trafilatura', 'BeautifulSoup + Summarization', 'Trafilatura + Summarization'])

    bart_model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
    tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")

    if title:
        paragraphs1 = extract_paragraphs(title, use_trafilatura=False)
        paragraphs2 = extract_paragraphs(title, use_trafilatura=True)
        with tab1:
            for paragraph in paragraphs1:
                cleaned_text = util.clean_document(paragraph)
                if len(cleaned_text) == 0:
                    continue
                temp = pd.DataFrame()
                temp['cleaned_text'] = [cleaned_text]
                temp['num_years'] = [util.num_years(paragraph)]
                pred = model.predict(temp[['cleaned_text', 'num_years']])
                
                st.write("Predicted Category: " + pred[0])
                st.write(paragraph)
                st.markdown('''---''')
        with tab2:
            cleaned_text = util.clean_document(paragraphs2)
            temp = pd.DataFrame()
            temp['cleaned_text'] = [cleaned_text]
            temp['num_years'] = [util.num_years(paragraphs2)]
            pred = model.predict(temp[['cleaned_text', 'num_years']])
            
            st.write("Predicted Category: " + pred[0])
            st.write(paragraphs2)
            st.markdown('''---''')
        with tab3:
            for paragraph in paragraphs1:
                inputs = tokenizer([paragraph], max_length=1024, return_tensors="pt")
                summary_ids = bart_model.generate(inputs["input_ids"], num_beams=2, min_length=0, max_length=max_summary_length)
                summary = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False, truncation=True)[0]
                cleaned_text = util.clean_document(summary)
                if len(cleaned_text) == 0:
                    continue
                temp = pd.DataFrame()
                temp['cleaned_text'] = [cleaned_text]
                temp['num_years'] = [util.num_years(summary)]
                pred = model.predict(temp[['cleaned_text', 'num_years']])
                
                st.write("Predicted Category: " + pred[0])
                st.write(summary)
                st.markdown('''---''')
        with tab4:
            inputs = tokenizer([paragraphs2], max_length=1024, return_tensors="pt")
            summary_ids = bart_model.generate(inputs["input_ids"], num_beams=2, min_length=0, max_length=max_summary_length)
            summary = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False, truncation=True)[0]
            cleaned_text = util.clean_document(summary)
            temp = pd.DataFrame()
            temp['cleaned_text'] = [cleaned_text]
            temp['num_years'] = [util.num_years(summary)]
            pred = model.predict(temp[['cleaned_text', 'num_years']])
            
            st.write("Predicted Category: " + pred[0])
            st.write(summary)
            st.markdown('''---''')