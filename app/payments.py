import beyonic
from project.settings import BEYONIC_KEY

beyonic.api_key = BEYONIC_KEY


# def initialize_payment(phonenumber, first_name, last_name, amount, metadata: {}, ):
def initialize_payment():
    collection_request = beyonic.CollectionRequest.create(phonenumber='+256756878460',
                                                          amount='500',
                                                          currency='UGX',
                                                          description='Per diem',
                                                          callback_url='https://my.website/payments/callback',
                                                          metadata={'my_id': '123ASDAsd123'},
                                                          send_instructions=True
                                                          )

    print(collection_request)
