# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: sample_recognize_custom_entities.py

DESCRIPTION:
    This sample demonstrates how to recognize custom entities in documents.
    Recognizing custom entities is available as an action type through the begin_analyze_actions API.

    For information on regional support of custom features and how to train a model to
    recognize custom entities, see https://aka.ms/azsdk/textanalytics/customentityrecognition

USAGE:
    python sample_recognize_custom_entities.py

    Set the environment variables with your own values before running the sample:
    1) AZURE_TEXT_ANALYTICS_ENDPOINT - the endpoint to your Cognitive Services resource.
    2) AZURE_TEXT_ANALYTICS_KEY - your Text Analytics subscription key
    3) CUSTOM_ENTITIES_PROJECT_NAME - your Text Analytics Language Studio project name
    4) CUSTOM_ENTITIES_DEPLOYMENT_NAME - your Text Analytics deployed model name
"""

from dotenv import load_dotenv
import os

load_dotenv()


def sample_recognize_custom_entities(document):
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import (
        TextAnalyticsClient,
        RecognizeCustomEntitiesAction,
    )

    endpoint = os.getenv('LANGUAGE_SERVICE_ENPOINT')
    key = os.getenv('LANGUAGE_SERVICE_KEY')
    project_name = "aiprofessorentityrecognition"
    deployed_model_name = "deployaiprofessorentityrecognition1"
    
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
    

    poller = text_analytics_client.begin_analyze_actions(
        document,
        actions=[
            RecognizeCustomEntitiesAction(
                project_name=project_name, deployment_name=deployed_model_name
            ),
        ],
    )

    document_results = poller.result()
    for result in document_results:
        custom_entities_result = result[0]  # first document, first result
        if not custom_entities_result.is_error:
            for entity in custom_entities_result.entities:
                # print(
                #     "Entity '{}' has category '{}' with confidence score of '{}'".format(
                #         entity.text, entity.category, entity.confidence_score
                #     )
                # )
                
                return entity.text, entity.category, entity.confidence_score
        else:
            print(
                "...Is an error with code '{}' and message '{}'".format(
                    custom_entities_result.code, custom_entities_result.message
                )
            )


# if __name__ == "__main__":
#     sample_recognize_custom_entities()