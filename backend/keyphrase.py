import os

endpoint = "https://hackathon-language-resource.cognitiveservices.azure.com/"
key = "c8cfd7dae3c14fe3911bf353b62267a8"

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Authenticate the client using your key and endpoint 
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

def key_phrase_extraction_example(client):

    try:
        documents = ["Nokia and Microsoft have agreed a deal to work on delivery of music to handsets, while Sony Ericsson has unveiled its phone Walkman and Motorola is working on an iTunes phone.Can mobile phones replace the MP3 player in your pocket? The music download market has been growing steadily since record firms embraced digital distribution. Ease of use, relative low price and increased access to broadband has helped drive the phenomenal growth of MP3 players.Full-length music downloads on mobile phones have not taken off so quickly - held back by technical challenges as well as issues over music availability. But the mobile music industry is confident that the days of dedicated MP3 players are numbered.Gilles Babinet, chief executive of mobile music firm Musiwave"]

        response = client.extract_key_phrases(documents = documents)[0]

        if not response.is_error:
            print("\tKey Phrases:")
            for phrase in response.key_phrases:
                print("\t\t", phrase)
        else:
            print(response.id, response.error)

    except Exception as err:
        print("Encountered exception. {}".format(err))
        
key_phrase_extraction_example(client)