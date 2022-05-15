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

results = client.search(search_text="Thoday")

for result in results:
    print(result["content"])

    document =[result['content']]
print(document)

def sample_classify_document_single_category():
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import (
        TextAnalyticsClient,
        SingleCategoryClassifyAction
    )
    
    # endpoint = os.environ["https://hackathon-language-resource.cognitiveservices.azure.com/"]
    endpoint = "https://hackathon-language-resource.cognitiveservices.azure.com/"
    
    # key = os.environ["c8cfd7dae3c14fe3911bf353b62267a8"]
    key = "c8cfd7dae3c14fe3911bf353b62267a8"
    # project_name = os.environ["classifytext"]
    project_name = "classifytext"
    # deployed_model_name = os.environ["deployclassfiytext"]
    deployed_model_name = "deployclassfiytext"

        
    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )

    
    poller = text_analytics_client.begin_analyze_actions(
        document,
        actions=[
            SingleCategoryClassifyAction(
                project_name=project_name,
                deployment_name=deployed_model_name
            ),
        ],
    )

     
    document_results = poller.result()
    for classification_results in document_results:
        classification_result = classification_results[0]  # first document, first result
        
        if not classification_result.is_error:
            classification = classification_result.classification
            print("The document was classified as '{}' with confidence score {}.".format(
                classification.category, classification.confidence_score)
            )
        else:
            print("Document text has an error with code '{}' and message '{}'".format(
                classification_result.code, classification_result.message
            ))


if __name__ == "__main__":
    sample_classify_document_single_category()

