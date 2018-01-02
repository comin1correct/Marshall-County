#set credentials
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="Tutorial Project-3fbc76548285.json"

import io
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
class myVision:

    def detect_document_uri(self,uri):
        """Detects document features in the file located in Google Cloud
        Storage."""
        client = vision.ImageAnnotatorClient()
        image = types.Image()
        image.source.image_uri = uri

        response = client.document_text_detection(image=image)
        document = response.full_text_annotation.text
        print(document)
        return True
                    
    #detect_document_uri('https://i.stack.imgur.com/t3qWG.png')


"""
~~~~~~~~~~~~~~~~~~~~~~~~~~NOTE~~~~~~~~~~~~~~~~~~~~~~~~~~

    Retrieving image url:

        document.images[50].getAttribute('src')

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Three Oil and Gas Leases:
    
  -  Lessor
  -  Lessee
  -  Tax id#
  -  Effective date


"""
