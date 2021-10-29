# ASK2HA
Home Assistant (HA) Add-on for Alexa integration without opening HA to the world.

The Add-on works the same as haaska but the direct communication between HA and the Alexa skill is replaced with a SQS queue for forwarding the requests (Lambda->HA) and a DynamoDB table for the responses (HA->Lambda).

The add-on makes a long pull request every 20 seconds to the Amazon SQS queue. If a request is present is passed to HA, the response is saved in the DynamoDB table using the id of the request as primary key (messageId)

## Setup

For the initial part of the setup you can follow this guide https://github.com/mike-grant/haaska/wiki, you also need to create the SQS queue and the DynamoDB table (use "messageId " as primary key for the table).

For the installation of the add-on follow the guide for third-party add-ons https://www.home-assistant.io/hassio/installing_third_party_addons/.

Remember to change config.py for the lambda function and the configuration of the addon inside HA after the installation.

## Other info

The Add-on was used as is for more than 1 year with no issues or maintenance whatsoever (maybe I could check if some dynamoDB record were not erased because of instabilities in the internet connection)

The code works as intended but may contains bugs, use at your own risk.

The free tier of amazon AWS should cover both the lambda function, the SQS queue and the DynamoDB table. 1 month uses about 15% of SQS free tier and less than 0.1% of the other two services.
