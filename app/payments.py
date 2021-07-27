import beyonic
from project.settings import BEYONIC_KEY

beyonic.api_key = BEYONIC_KEY


def initialize_payment(phonenumber, description, metadata, amount=500):
    collection_request = beyonic.CollectionRequest.create(phonenumber=phonenumber,
                                                          amount=amount,
                                                          currency='UGX',
                                                          description=description,
                                                          callback_url='https://my.website/payments/callback',
                                                          metadata=metadata,
                                                          send_instructions=True)
    print(collection_request)
