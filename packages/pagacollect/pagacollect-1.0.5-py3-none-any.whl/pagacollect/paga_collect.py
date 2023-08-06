import requests
import hashlib
import json

from base64 import b64encode


def _get_basic_auth(client_id, password):
    base64_string = b64encode(str.encode(client_id + ":" + password)).decode("ascii")
    return base64_string


def generate_hash(hash_params):
    """
    Generates hash based on passed
          args
          ----------
          hash_params : string
              A concatenated string of parameters be hashed
    """
    return hashlib.sha512(str(hash_params.strip()).encode("utf-8")).hexdigest().strip()


def post_request(headers, json_data, url):
    """
    Posts request to given url with the given payload
          args
          ----------
          headers : dict
                Holds authentication data for the request
          json_data : json
                The request payload
          url : boolean
                The api url
    """
    return requests.request(method="POST", url=url, headers=headers, data=json_data)


def remove_empty_elements(value):
    """
    Recursively remove all None values from dictionaries and lists, and returns
    the result as a new dictionary or list.
    """
    if isinstance(value, list):
        return [remove_empty_elements(x) for x in value if x is not None]
    elif isinstance(value, dict):
        return {
            key: remove_empty_elements(val)
            for key, val in value.items()
            if val is not None
        }
    else:
        return value


class Collect(object):
    """
    Base class for paga Collect api library
    """

    _CONTENT_TYPE = "application/json"
    test_server = "https://beta-collect.paga.com"
    live_Server = "https://collect.paga.com"

    def __init__(self, client_id, password, api_key, is_test_env):
        """
              args
              ----------
              client_id : string
                  your public ID gotten from Paga
              password : string
                  your account password
              is_test_env : boolean
                  indicates whether application is in test or live mode
              """
        self.client_id = client_id
        self.password = password
        self.api_key = api_key
        self.is_test_env = is_test_env

    def build_header(self, hash_params):
        """
        Builds the HTTP request header 
              args
              ----------
              hash_params : string
                  A concatenated string of parameters be hashed
        """
        basic_auth = _get_basic_auth(self.client_id, self.password)

        hash_params = hash_params + self.api_key
        hash_data = generate_hash(hash_params)

        headers = {
            "Content-Type": self._CONTENT_TYPE,
            "Authorization": "Basic " + basic_auth,
            "hash": hash_data
        }

        return headers

    def get_url(self, is_test_env):
        """
        Gets the api url   
              args
              ----------
              is_test_env : boolean
                  A flag to determine if the requested url is test or live
        """
        if is_test_env:
            return self.test_server
        else:
            return self.live_Server

    def get_history(self, payload):
        """
        Calls Collect API to get the history of transactions done over time  
              args
              ----------
              payload : json
                  A request body for the history endpoint of the Collect API
        """
        endpoint = "/history"
        hash_params = ''
        url = self.get_url(self.is_test_env)
        server_url = url + endpoint

       

        data = json.dumps(payload)
        load_json = json.loads(data)

        
        hash_json = {
            "referenceNumber": load_json.get('referenceNumber') or None
        }

       

        request_data = {
            "referenceNumber": load_json.get('referenceNumber') or None,
            "startDateTimeUTC":  load_json.get("startDateTimeUTC"),
            "endDateTimeUTC":  load_json.get("endDateTimeUTC") or None,

        }
        hash_data = json.dumps(remove_empty_elements(hash_json)) 
        hash_params = ''.join(list(json.loads(hash_data).values()))
        headers = self.build_header(hash_params)
        json_data = json.dumps(remove_empty_elements(request_data))
    
    
        response = post_request(headers, json_data, server_url)
        return response.text

    def payment_request_refund(self, payload):
        """
        Calls Collect API to cancel or initiate a refund if we were unable to fulfill 
        the request for one reason or the other
              ----------
              payload : json
                  A request body for the paymentRequestRefund endpoint of the Collect API
        """
        endpoint = "/refund"
        hash_params = ''.join([payload["referenceNumber"], payload["refundAmount"]])


        url = self.get_url(self.is_test_env)
        server_url = url + endpoint

        headers = self.build_header(hash_params)

        data = json.dumps(payload)
        load_json = json.loads(data)

        request_data = {
            "referenceNumber": load_json.get('referenceNumber'),
            "refundAmount":  load_json.get("refundAmount"),
            "currency":  load_json.get("currency"),
            "reason":  load_json.get("reason") or None,

        } 
        json_data = json.dumps(remove_empty_elements(request_data))
    
    
        response = post_request(headers, json_data, server_url)
        return response.text
    

    def delete_persistent_payment_account(self, payload):
        """
        Calls Collect API to delete a persistent payment account. 
       
              ----------
              payload : json
                  A request body for the deletePersistentPaymentAccount endpoint of the Collect API
        """
        endpoint = "/deletePersistentPaymentAccount"
        hash_params = ''.join([payload["referenceNumber"], payload["accountIdentifier"]])


        url = self.get_url(self.is_test_env)
        server_url = url + endpoint

        headers = self.build_header(hash_params)

        data = json.dumps(payload)
        load_json = json.loads(data)

        request_data = {
            "referenceNumber": load_json.get('referenceNumber'),
            "accountIdentifier":  load_json.get("accountIdentifier"),
            "reason":  load_json.get("endDateTimeUTC") or None,

        } 
        json_data = json.dumps(remove_empty_elements(request_data))
    
    
        response = post_request(headers, json_data, server_url)
        return response.text

    def get_persistent_payment_account(self, payload):
        """
        Calls Collect API to to query the properties associated with an existing persistent payment account. 
       
              ----------
              payload : json
                  A request body for the getPersistentPaymentAccount endpoint of the Collect API
        """
        endpoint = "/getPersistentPaymentAccount"
        hash_params = ''.join([payload["referenceNumber"], payload["accountIdentifier"]])


        url = self.get_url(self.is_test_env)
        server_url = url + endpoint

        headers = self.build_header(hash_params)

        data = json.dumps(payload)
        load_json = json.loads(data)

        request_data = {
            "referenceNumber": load_json.get('referenceNumber'),
            "accountIdentifier":  load_json.get("accountIdentifier"),

        } 
        json_data = json.dumps(request_data)
    
    
        response = post_request(headers, json_data, server_url)
        return response.text


    def update_persistent_payment_account(self, payload):
        """
        This endpoint allows for changing any of the account properties except the accountNumber (NUBAN) and the accounReference properties which cannot be changed. 
       
              ----------
              payload : json
                  A request body for the updatePersistentPaymentAccount endpoint of the Collect API
        """
        endpoint = "/updatePersistentPaymentAccount"


        url = self.get_url(self.is_test_env)
        server_url = url + endpoint

        data = json.dumps(payload)
        load_json = json.loads(data)

        request_data = {
            "referenceNumber": load_json.get('referenceNumber'),
            "accountIdentifier":  load_json.get("accountIdentifier"),
            "phoneNumber":  load_json.get("phoneNumber") or None,
            "firstName":  load_json.get("firstName") or None,
            "lastName":  load_json.get("endDateTimeUTC") or None,
            "accountName":  load_json.get("lastName") or None,
            "financialIdentificationNumber":  load_json.get("financialIdentificationNumber") or None,
            "callbackUrl":  load_json.get("callbackUrl") or None,
            "creditBankId":  load_json.get("creditBankId") or None,
            "creditBankAccountNumber":  load_json.get("creditBankAccountNumber") or None,


        } 

        hash_json = {
            "referenceNumber": load_json.get('referenceNumber'),
            "accountIdentifier":  load_json.get("accountIdentifier"),
            "financialIdentificationNumber":  load_json.get("financialIdentificationNumber") or None,
            "creditBankId":  load_json.get("creditBankId") or None,
            "creditBankAccountNumber":  load_json.get("creditBankAccountNumber") or None,
            "callbackUrl":  load_json.get("callbackUrl") or None,
        }

        hash_data = json.dumps(remove_empty_elements(hash_json))
        hash_params = ''.join(list(json.loads(hash_data).values()))
        print(hash_params)
        headers = self.build_header(hash_params)
        json_data = json.dumps(remove_empty_elements(request_data))
    
    
        response = post_request(headers, json_data, server_url)
        return response.text

    




    def get_status(self, payload):
        """
        Calls Collect API to get the status of a transaction
              args
              ----------
              payload : json
                  A request body for the status endpoint of the Collect API
        """
        endpoint = "/status"
        hash_params = ''

        if payload.get("referenceNumber"):
            hash_params += payload["referenceNumber"]

        url = self.get_url(self.is_test_env)
        server_url = url + endpoint

        headers = self.build_header(hash_params)

        json_data = json.dumps(payload)
        response = post_request(headers, json_data, server_url)
        return response.text

    def get_banks(self, payload):
        """
        Calls Collect API to get all banks   
              args
              ----------
              payload : json
                  A request body for the getBanks endpoint of the Collect API
        """
        endpoint = "/banks"
        hash_params = payload["referenceNumber"]

        url = self.get_url(self.is_test_env)
        server_url = url + endpoint

        headers = self.build_header(hash_params)

        json_data = json.dumps(payload)
        response = post_request(headers, json_data, server_url)
        return response.text

    def payment_request(self, payload):
        """
        Calls Collect API to make a payment request   
              args
              ----------
              payload : json
                  A request body for the paymentRequest endpoint of the Collect API
        """
        endpoint = "/paymentRequest"

        url = self.get_url(self.is_test_env)
        server_url = url + endpoint
        data = json.dumps(payload)
        load_json = json.loads(data)

        payee = {
            "name": load_json.get("payee").get("name"),
            "accountNumber": load_json.get("payee").get("accountNumber") or None,
            "phoneNumber": load_json.get("payee").get("phoneNumber") or None,
            "bankId": load_json.get("payee").get("bankId") or None,
            "bankAccountNumber": load_json.get("payee").get("bankAccountNumber") or None,
            "financialIdentificationNumber": load_json.get("payee").get("financialIdentificationNumber") or None,

        }

        payer = {
            "name": load_json.get("payer").get("name"),
            "phoneNumber": load_json.get("payer").get("phoneNumber") or None,
            "email": load_json.get("payer").get("email") or None,
            "bankId": load_json.get("payee").get("bankId") or None,
        }

        payment_request_payload = {
            "referenceNumber": load_json.get("referenceNumber"),
            "amount": str(load_json.get("amount")),
            "currency": load_json.get("currency"),
            "payer": payer,
            "payee": payee,
            "expiryDateTimeUTC": load_json.get("expiryDateTimeUTC") or None,
            "isSuppressMessages": load_json.get("isSuppressMessages"),
            "payerCollectionFeeShare": load_json.get("payerCollectionFeeShare"),
            "payeeCollectionFeeShare": load_json.get("payeeCollectionFeeShare"),
            "isAllowPartialPayments": load_json.get("isAllowPartialPayments") or None,
            "callBackUrl": load_json.get("callBackUrl"),
            "paymentMethods": load_json.get("paymentMethods"),
            "displayBankDetailToPayer": load_json.get("displayBankDetailToPayer") or None
        }

        request_hash = {
            "referenceNumber": load_json.get("referenceNumber"),
            "amount": str(load_json.get("amount")),
            "currency": load_json.get("currency"),
        }

        payee_hash = {
            "accountNumber": load_json.get("payee").get("accountNumber") or None,
            "phoneNumber": load_json.get("payee").get("phoneNumber") or None,
            "bankId": load_json.get("payee").get("bankId") or None,
            "bankAccountNumber": load_json.get("payee").get("bankAccountNumber") or None,

        }


        payer_hash = {
            "phoneNumber": load_json.get("payer").get("phoneNumber") or None,
            "email": load_json.get("payer").get("email") or None,
        }
        
        payee_hash_data = json.dumps(remove_empty_elements(payee_hash))
        request_hash_data = json.dumps(request_hash)

        payer_hash_data = json.dumps(remove_empty_elements(payer_hash))
        hash_params = ''.join(list(json.loads(request_hash_data).values())) + ''.join(list(json.loads(payer_hash_data).values())) + ''.join(list(json.loads(payee_hash_data).values()))
        print(hash_params)
        headers = self.build_header(hash_params)
        json_data = json.dumps(remove_empty_elements(payment_request_payload))
    
    
        response = post_request(headers, json_data, server_url)
        return response.text

    def register_persistent_payment_account(self, payload):
        """
        Calls Collect API to create persistent payment account
              args
              ----------
              payload : json
                  A request body for the register payment persistent account endpoint of the Collect API
        """
        endpoint = "/registerPersistentPaymentAccount"
        url = self.get_url(self.is_test_env)
        server_url = url + endpoint

        data = json.dumps(payload)
        load_json = json.loads(data)

        request_data = {
            "referenceNumber": load_json.get("referenceNumber"),
            "phoneNumber": load_json.get("phoneNumber"),
            "firstName": load_json.get("firstName"),
            "lastName": load_json.get("lastName") or None,
            "accountName": load_json.get("accountName"),
            "email": load_json.get("email"),
            "financialIdentificationNumber": load_json.get("financialIdentificationNumber") or None,
            "accountReference": load_json.get("accountReference"),
            "creditBankId": load_json.get("creditBankId") or None,
            "creditBankAccountNumber": load_json.get("creditBankAccountNumber") or None,
            "callbackUrl": load_json.get("callbackUrl") or None,
        }

        hash_json = {
            "referenceNumber": load_json.get("referenceNumber"),
            "accountReference": load_json.get("accountReference"),
            "financialIdentificationNumber": load_json.get("financialIdentificationNumber") or None,
            "creditBankId": load_json.get("creditBankId") or None,
            "creditBankAccountNumber": load_json.get("creditBankAccountNumber") or None,
            "callbackUrl": load_json.get("callbackUrl") or None,
        }

        hash_data = json.dumps(remove_empty_elements(hash_json))
        hash_params = ''.join(list(json.loads(hash_data).values()))
        headers = self.build_header(hash_params)
        json_data = json.dumps(remove_empty_elements(request_data))
    
    
        response = post_request(headers, json_data, server_url)
        return response.text

