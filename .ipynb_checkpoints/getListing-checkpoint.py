import requests
from bs4 import BeautifulSoup
from openai import OpenAI


def llm_reformat(text):
    system_prompt = '''You are a web scraping helper.
    Your take in raw text from the web and output the information the user requests.
    Do not be conversational and only output information directly copied from the web scrape dump.
    Never paraphrase or summarize information. Always copy the relevant information as is.
    When possible, be biased toward including too much information from the document rather than too little.
    Do not write any additional text not found in the web scrape no matter what.
    '''
    user_prompt = '''The following text is scraped from a job listing.
    Please get rid of any artifacts from the scraping process and only return information relevant to the job listing.
    Please remove any website headers, footers, or references to other jobs that may be found on the listing page.
    SCRAPED TEXT:
    '''

    final_prompt = user_prompt + text

    client = OpenAI()

    response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": final_prompt},
            ]
        )
    generation = response.choices[0].message.content #usage as of Dec 2023

    return generation


def get_listing(url):
    response = requests.get(url)#, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    scraped_text = ' '

    for item in soup.find_all('p'):
        scraped_text += item.text
    for item in soup.find_all('a'):
        scraped_text += item.text

    max_len = 15000
    scraped_text = scraped_text[:max_len] #limit context window

    listing = llm_reformat(scraped_text)

    return listing
