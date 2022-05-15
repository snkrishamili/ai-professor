import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

index_name = "hackathon-index"
# Get the service endpoint and API key from the environment
searchendpoint = "https://hackathoncognitivesearch.search.windows.net"
searchkey = "9EC71A46548D1B103907A76B6F5CB7EC"

# Create a client
credential = AzureKeyCredential(searchkey)
client = SearchClient(endpoint=searchendpoint,
                      index_name=index_name,
                      credential=credential)

results = client.search(search_text="music")

for result in results:
    print(result["content"])    
    document = [result["content"]]
    


    
summarizeendpoint = "https://hackathon-language-resource.cognitiveservices.azure.com/"
summarizekey = "c8cfd7dae3c14fe3911bf353b62267a8"

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Authenticate the client using your key and endpoint 
def authenticate_client():
    ta_credential = AzureKeyCredential(summarizekey)
    text_analytics_client = TextAnalyticsClient(
            endpoint=summarizeendpoint, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

# Example method for summarizing text
def sample_extractive_summarization(client):
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import (
        TextAnalyticsClient,
        ExtractSummaryAction
    ) 

    
    poller = client.begin_analyze_actions(
        document,
        actions=[
            ExtractSummaryAction(max_sentence_count=4)
        ],
    )

    document_results = poller.result()
    for result in document_results:
        extract_summary_result = result[0]  # first document, first result
        if extract_summary_result.is_error:
            print("...Is an error with code '{}' and message '{}'".format(
                extract_summary_result.code, extract_summary_result.message
            ))
        else:
            print("Summary extracted: \n{}".format(
                " ".join([sentence.text for sentence in extract_summary_result.sentences]))
            )

sample_extractive_summarization(client)
    