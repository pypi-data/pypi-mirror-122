# Paga Collect Python library

The Paga Collect API allows anyone to initiate a payment request to a third party and automatically get notified when the payment request is fulfilled. This library makes it easier and faster for developers to integrate the API

### 1. Installation

Make sure you have `pip` installed, then run the command below

```sh
pip install pagacollect
```

### 2. Usage

Once installed to use the library see sample code below:

```sh
from pagacollect.paga_collect import Collect

principal = "public_key"
credentials = "private"
hash_key = "hash_key"

collect = Collect(principal, credentials, hash_key, False)
```

### Paga Collect API Operations

Now that you have created a collect api object you easily call its operations

<br>

#### Request Payment

Register a new request for payment between a payer and a payee. Once a payment request is initiated successfully, the payer is notified by the platform (this can be suppressed) and can proceed to authorize/execute the payment. Once the payment is fulfilled, a notification is sent to the supplied callback URL. See the callback notification section for more details.
<br>
To make a payment request see sample code below:

```sh
payment_request_payload = {
    "referenceNumber": "6020000011z",
    "amount": "100",
    "currency": "NGN",
    "payer": {
        "name": "John Doe",
        "phoneNumber": "07033333333",
        "bankId": "3E94C4BC-6F9A-442F-8F1A-8214478D5D86"
    },
    "payee": {
        "name": "Payee Tom",
        "accountNumber": "1188767464",
        "bankId": "40090E2F-7446-4217-9345-7BBAB7043C4C",
        "bankAccountNumber": "0000000000",
        "financialIdentificationNumber": "03595843212"
    },
    "expiryDateTimeUTC": "2021-05-27T00:00:00",
    "isSuppressMessages": "true",
    "payerCollectionFeeShare": "0.5",
    "payeeCollectionFeeShare": "0.5",
    "isAllowPartialPayments": "true",
    "callBackUrl": "http://localhost:9091/test-callback",
    "paymentMethods": ["BANK_TRANSFER", "FUNDING_USSD"],
"displayBankDetailToPayer": False
}

response = collect.payment_request(payment_request_payload)
```

<br>

#### Register Persistent Payment Account

An operation for business to create Persistent Payment Account Numbers that can be assigned to their customers for payment collection.
<br>
To create a persistent payment account see sample code below:

```sh
register_persistent_payment_account_payload = {
    "referenceNumber": "test123451",
    "phoneNumber": "07022222222",
    "accountName": "Joh Doe",
    "firstName": "John",
    "lastName": "Doe",
    "email": "john@doe.com",
    "accountReference": "22222222222220",
    "financialIdentificationNumber": "22182799077",
    "creditBankId": "3E94C4BC-6F9A-442F-8F1A-8214478D5D86",
    "creditBankAccountNumber":"0000000000",
    "callbackUrl": "http://localhost:9091/test-callback"
}

response = collect.register_persistent_payment_account(register_persistent_payment_account_payload)
```

<br>

#### Query Status

Query the current status of a submitted request
<br>
To check the status of a submitted request see sample code below:

```sh
status_payload = {"referenceNumber": "82000001109", }

response = collect.get_status(status_payload)
```

<br>

#### Query History

Get payment requests for a period between given start and end dates. The period window should not exceed 1 month.
<br>
See sample code below:

```sh
history_payload = {
    "referenceNumber": "82000001109",
    "startDateTimeUTC" : "2021-05-13T19:15:22",
    "endDateTimeUTC" : "2021-05-20T19:15:22"
}

response = collect.get_history(history_payload)
```

<br>

#### Get Banks

Retrieve a list of supported banks and their complementary unique ids on the bank. This is required for populating the payer (optional) and payee objects in the payment request model.
<br>
See usage sample code below:

```sh
banks_payload = {"referenceNumber": "0001109"}

response = collect.get_banks(banks_payload)
```



#### Payment Request Refund

This end-point can be used to either cancel or initiate a refund if we were unable to fulfill the request for one reason or the other.
<br>
See usage sample code below:

```sh
refund_payload = 
{
  "referenceNumber" : "12345",
  "refundAmount" : 1000.0,
  "currency" : "NGN",
  "reason" : "no particular reason"
}
response = collect.payment_request_refund(refund_payload)
```


#### Delete Persistent Payment Account

This endpoint allows for deleting a persistent payment account.
<br>
See usage sample code below:

```sh
delete_payload = 
{
  "referenceNumber":"23402359879879997",
  "accountIdentifier":"0830202843",
  "reason":"off-boarded account"
 }
response = collect.delete_persistent_payment_account(delete_payload)
```


#### Get Persistent Payment Account

A method to query the properties associated with an existing persistent payment account.
<br>
See usage sample code below:

```sh
get_payload = 
{
  "referenceNumber":"23402359879879997",
  "accountIdentifier":"2806605308"
 }
response = collect.get_persistent_payment_account(get_payload)
```


#### Update Persistent Payment Account

This endpoint allows for changing any of the account properties except the **accountNumber (NUBAN)** and the **accounReference** properties which cannot be changed.
<br>
See usage sample code below:

```sh
update_payload = 
{
  "referenceNumber":"23402359879879996",
  "accountIdentifier":"0830202843",
  "phoneNumber":"0910220042",
  "firstName":"Renamed",
  "lastName": "Customer",
  "accountName": "Renamed Customer",
  "financialIdentificationNumber": "12345454666",
  "callbackUrl": "http://77d761893689.ngrok.io/persistent/000000000009/Password6",
  "creditBankId":"40090E2F-7446-4217-9345-7BBAB7043C4C",
  "creditBankAccountNumber":"0000000031"
 }
response = collect.update_persistent_payment_account(update_payload)
```
