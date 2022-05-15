# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: sample_single_category_classify.py

DESCRIPTION:
    This sample demonstrates how to classify documents into a single custom category. For example,
    movie plot summaries can be categorized into a single movie genre like "Mystery", "Drama", "Thriller",
    "Comedy", "Action", etc. Classifying documents is available as an action type through
    the begin_analyze_actions API.

    For information on regional support of custom features and how to train a model to
    classify your documents, see https://aka.ms/azsdk/textanalytics/customfunctionalities

USAGE:
    python sample_single_category_classify.py

    Set the environment variables with your own values before running the sample:
    1) AZURE_TEXT_ANALYTICS_ENDPOINT - the endpoint to your Cognitive Services resource.
    2) AZURE_TEXT_ANALYTICS_KEY - your Text Analytics subscription key
    3) SINGLE_CATEGORY_CLASSIFY_PROJECT_NAME - your Text Analytics Language Studio project name
    4) SINGLE_CATEGORY_CLASSIFY_DEPLOYMENT_NAME - your Text Analytics deployed model name
"""


import os
from dotenv import load_dotenv

load_dotenv()

def sample_classify_document_single_category(document):
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import (
        TextAnalyticsClient,
        SingleCategoryClassifyAction
    )
    
    endpoint = os.getenv('LANGUAGE_SERVICE_ENPOINT')
    key = os.getenv('LANGUAGE_SERVICE_KEY')
    # endpoint = os.environ["https://hackathon-language-resource.cognitiveservices.azure.com/"]
    # endpoint = "https://aiprofessorlanguageresource.cognitiveservices.azure.com/"
    
    # key = os.environ["c8cfd7dae3c14fe3911bf353b62267a8"]
    # key = "cc241880669b4a51bec9f2ba1d0b114a"
    # project_name = os.environ["classifytext"]
    project_name = "aiprofessortextclassification"
    # deployed_model_name = os.environ["deployclassfiytext"]
    deployed_model_name = "deployaiprofessortextclassification"
    # path_to_sample_document = os.path.abspath(
    #     os.path.join(
    #         os.path.abspath(__file__),
    #         "..",
    #         "D:/HACKATHON/AI Professor Project/text_samples/b (490).txt",
    #     )
    # )

    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )

    # with open(path_to_sample_document) as fd:
    #     document = [fd.read()]

    # document = ["Rank 'set to sell off film unit'\n\nLeisure group Rank could unveil plans to demerge its film services unit and sell its media business, reports claim.\n\nRank, formerly famous for the Carry On series, will expose the shake-up at the announcement of its results on Friday, the Sunday Telegraph reported. \
    #             Advisors Goldman Sachs are understood to have valued its demerged Deluxe Film unit at Â£300m, the report added. Speculation of a possible shake-up has mounted since Rank announced a study into a possible demerger in September. Since Mike Smith's appointment as chief executive in 1999, the group has focused on fewer \
    #             businesses and embarked on a major cost-cutting programme which has seen it dispose of a number of businesses, including the Odeon cinema chain and the Pinewood studios. The move left the group with three core divisions: gaming, Hard Rock and Deluxe Films, which provides technical services to Hollywood \
    #             studios.\n\nRank now aims to concentrate on its gaming, bars and hotels business, including extending its Hard Rock brand to its casinos - trials of which have been a success. It also owns Deluxe Media, which makes and distributes DVDs and videos. However, that business is seen as less successful. Last year \
    #             it made profits of Â£21.5m on a turnover of Â£392.1m and experts suggest its success in moving to DVDs \
    #             from VHS video could make it an attractive target for a private equity buyer. A spokesman for the firm \
    #             refused to comment on the reports, but said any results from the demerger study were likely to be set out when it unveiled its results on Friday. Analysts predict the firm is likely to report a slight drop \
    #             in annual pre-tax profits to Â£170m from Â£194m last year. Formed in the 1940s the firm was a leading UK film producer and cinema owner for many years. It has now diversified into a range of other leisure activities - mainly in the UK - including hotels, roadside service areas and holiday centres. It now owns 34 Grosvenor casinos, the Mecca Bingo chain and more than 100 Hard Rock Cafes in 38 countries.\n"]
    
    
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
    # for doc, classification_results in zip(document, document_results):
    for result in document_results:
        classification_result = result[0]
        if not classification_result.is_error:
            classification = classification_result.classification
                # print("The document text '{}' was classified as '{}' with confidence score {}.".format(
                #     doc, classification.category, classification.confidence_score)
                # )
            
            return (classification.category, classification.confidence_score)
            
        else:
            print("Document text '{}' has an error with code '{}' and message '{}'".format(
                    classification_result.code, classification_result.message
                ))
            return None


# if __name__ == "__main__":
#     sample_classify_document_single_category()