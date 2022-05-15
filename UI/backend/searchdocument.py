import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from dotenv import load_dotenv

load_dotenv()

def search_doc(text):
    index_name = os.getenv('SEARCH_INDEX_NAME')

    # Get the service endpoint and API key from the environment
    searchendpoint = os.getenv('SEARCH_SERVICE_ENDPOINT')
    searchkey = os.getenv('SEARCH_SERVICE_QUERY_KEY')

    # Create a client
    credential = AzureKeyCredential(searchkey)
    client = SearchClient(endpoint=searchendpoint,
                        index_name=index_name,
                        credential=credential)

    results =  client.search(text,
                            search_mode="all",
                                        include_total_count=True,                                        
                                        facets=['locations', 'people' , 'organizations'],
                                        select = "content,locations,keyphrases,people,organizations,metadata_storage_name")
                            
    
                            

    # for result in results:
    #     print(result["content"])
    return results
    