import openai
import requests
import os
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()
        
def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


# Read the Google API key and Custom Search Engine ID from files
GOOGLE_SEARCH_API_KEY = os.getenv('GOOGLE_SEARCH_API_KEY')
GOOGLE_SEARCH_CX = os.getenv('GOOGLE_SEARCH_CX')

openai.api_key = os.getenv('OPENAI_KEY')

conversation = []

def fetch_ai_news():
    search_engine = build("customsearch", "v1", developerKey=GOOGLE_SEARCH_API_KEY)
    query = "AI site:news.google.com"
    results = search_engine.cse().list(q=query, cx=GOOGLE_SEARCH_CX, num=6).execute()

    # Extract the titles, snippets, and URLs
    news_items = [{'title': result['title'], 'snippet': result['snippet'], 'url': result['link']} for result in results['items']]
    return news_items


def summarize_headlines(news_items):
    summarized_headlines = []
    for item in news_items:
        headline = item['title']
        snippet = item['snippet']
        url = item['url']
        summary = chatgpt(f"Please summarize the following headline, snippet and include link(url) for each snippet: {headline} - {snippet} - {url}")
        summarized_headlines.append(summary)
    return summarized_headlines



def save_headlines_to_file(filepath, headlines):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        for headline in headlines:
            outfile.write(headline + "\n")


def chatgpt(user_input, temperature=1, frequency_penalty=0.2, presence_penalty=0):
    global conversation

    conversation.append({"role": "user", "content": user_input})
    messages_input = conversation.copy()

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=temperature,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        messages=messages_input)

    chat_response = completion['choices'][0]['message']['content']
    conversation.append({"role": "assistant", "content": chat_response})
    return chat_response
    
# Fetch the latest AI news headlines and summarize them
headlines = fetch_ai_news()
summarized_headlines = summarize_headlines(headlines)

# Save the summarized headlines to a text file
save_headlines_to_file("ai_news_summaries.txt", summarized_headlines)
print("Summarized AI news headlines saved to ai_news_summaries.txt")

