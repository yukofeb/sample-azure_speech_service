#!/usr/bin/env python
# coding: utf-8

from typing import List

import logging
import sys
import requests
import time
import swagger_client as cris_client


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format="%(message)s")

SUBSCRIPTION_KEY = ''

NAME = "Simple transcription"
DESCRIPTION = "Simple transcription description"

LOCALE = "ja-JP"
RECORDINGS_BLOB_URI = ''

# Set subscription information when doing transcription with custom models
ADAPTED_ACOUSTIC_ID = None  # guid of a custom acoustic model
ADAPTED_LANGUAGE_ID = None  # guid of a custom language model


def transcribe():
    logging.info("Starting transcription client...")

    # configure API key authorization: subscription_key
    configuration = cris_client.Configuration()
    configuration.api_key['Ocp-Apim-Subscription-Key'] = SUBSCRIPTION_KEY

    # create the client object and authenticate
    client = cris_client.ApiClient(configuration)

    # create an instance of the transcription api class
    transcription_api = cris_client.CustomSpeechTranscriptionsApi(api_client=client)

    # get all transcriptions for the subscription
    transcriptions: List[cris_client.Transcription] = transcription_api.get_transcriptions()

    logging.info("Deleting all existing completed transcriptions.")

    # delete all pre-existing completed transcriptions
    # if transcriptions are still running or not started, they will not be deleted
    for transcription in transcriptions:
        try:
            transcription_api.delete_transcription(transcription.id)
        except ValueError:
            # ignore swagger error on empty response message body: https://github.com/swagger-api/swagger-core/issues/2446
            pass

    logging.info("Creating transcriptions.")

    # https://docs.microsoft.com/azure/cognitive-services/speech-service/batch-transcription
    properties = {
        'AddWordLevelTimestamps': 'True',
        'AddDiarization': 'True'
    }

    transcription_definition = cris_client.TranscriptionDefinition(
        name=NAME,
        description=DESCRIPTION,
        locale=LOCALE,
        recordings_url=RECORDINGS_BLOB_URI,
        properties=properties
    )

    data, status, headers = transcription_api.create_transcription_with_http_info(transcription_definition)

    # extract transcription location from the headers
    transcription_location: str = headers["location"]

    # get the transcription Id from the location URI
    created_transcription: str = transcription_location.split('/')[-1]

    logging.info("Checking status.")

    completed = False

    while not completed:
        running, not_started = 0, 0

        # get all transcriptions for the user
        transcriptions: List[cris_client.Transcription] = transcription_api.get_transcriptions()

        # for each transcription in the list we check the status
        for transcription in transcriptions:
            if transcription.status in ("Failed", "Succeeded"):
                # we check to see if it was one of the transcriptions we created from this client
                if created_transcription != transcription.id:
                    continue

                completed = True

                if transcription.status == "Succeeded":
                    results_uri = transcription.results_urls["channel_0"]
                    results = requests.get(results_uri)
                    logging.info("Transcription succeeded. Results: ")
                    logging.info(results.content.decode("utf-8"))
                else:
                    logging.info("Transcription failed :{}.".format(transcription.status_message))
            elif transcription.status == "Running":
                running += 1
            elif transcription.status == "NotStarted":
                not_started += 1

        logging.info("Transcriptions status: "
                "completed (this transcription): {}, {} running, {} not started yet".format(
                    completed, running, not_started))

        time.sleep(5)

    sys.exit()


if __name__ == "__main__":
    transcribe()
