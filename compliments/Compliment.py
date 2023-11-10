import requests
from bs4 import BeautifulSoup

import openai
import constants


def generate_generic_compliment(company_name, city, state):
      # Determine the location phrase based on the availability of city and state information
    if city and state:
        location_phrase = f"the talk of {city}, {state}, with glowing reviews that make your service shine."
    else:
        location_phrase = "earning glowing reviews and establishing you as a beloved pillar of healthcare in the community."

    # Construct the compliment with corrected grammar
    compliment = (
        f"Your exceptional dedication to patient care at {company_name} is {location_phrase} "
        f"It's your commitment that truly distinguishes you."
    )

    return compliment

def generate_compliment(content, company_name, custom_prompt='', temperature=0.7 ,engine="text-davinci-003"):
    openai.api_key = "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"

    # Trim the content if it's too long
    if len(content) > 1000:
        content = content[:1000] + "..."  # Shorten the content
    try:
        if custom_prompt:
            prompt = custom_prompt.format(company_name=company_name, content=content)  # Use the custom prompt
        else:
            prompt = f"Craft a compliment that highlights the exceptional qualities of {company_name}, focusing on elements like patient care, innovation, or community involvement. The compliment should be directed towards the business itself and use 'your' to reference the CEO and the company name to personalize the message. Draw inspiration from this website content:\n\n{content}\n\nCompliment to the Medical Practice:"
    except KeyError as e:
            return f"Error in custom prompt: {e}"

    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=temperature,
    ).choices[0].text.strip()

    return response



def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # will raise an HTTPError if the HTTP request returned an unsuccessful status code
        soup = BeautifulSoup(response.content, 'html.parser')
        # You can customize the content you scrape here, this is just an example to get all text
        return soup.get_text()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return ""