# ASK2HA
Home Assistant (HA) Add-on for Alexa integration without opening HA to the world.

The Add-on works the same as haaska but the direct communication between HA and the Alexa skill is replaced with a SQS queue for forwarding the requests (Lambda->HA) and a DynamoDB table for the responses (HA->Lambda).

For the initial part of the setup you can follow this guide https://github.com/mike-grant/haaska/wiki
