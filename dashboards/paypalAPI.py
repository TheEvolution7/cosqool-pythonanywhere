import requests
from rest_framework.response import Response
from datetime import datetime
import json

SANDBOX = True
PAYPAL_SANDBOX_URL = 'https://api-m.sandbox.paypal.com/v1'

if SANDBOX:
    PAYPAL_API_URL = PAYPAL_SANDBOX_URL

PAYPAL_AUTH = ('AST_3GZ94quJwZuGehO0ylOSDMWmm65mfOJnWzf3XWIvmh8h9iwniFZOBE0Sm950X8CBfNumg-6FZS9y', 'EBlAPtDZJD7mEAXIDLEOcZxafnlDJizrS1JjtdS5F9F7FN_R2_AGF-mwU53SQZsVhQP3cXLIUs504wfo')
PAYPAL_HEADER = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
def showPlanDetails(id):
    url = PAYPAL_API_URL + f"/billing/plans/{id}"
    response = requests.get(url=url, headers=PAYPAL_HEADER, auth=PAYPAL_AUTH)
    return response.json()

def showSubscriptionDetails(id):
    url = PAYPAL_API_URL + f"/billing/subscriptions/{id}"  
    response = requests.get(url=url, headers=PAYPAL_HEADER, auth=PAYPAL_AUTH)
    return response.json()

def listTransactionsForSubscription(id, start_time):
    url = PAYPAL_API_URL + f"/billing/subscriptions/{id}/transactions"   
    end_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    params = (
        ('start_time', start_time),
        ('end_time', end_time),
    )
    response = requests.get(url=url, headers=PAYPAL_HEADER, auth=PAYPAL_AUTH, params=params)
    return response.json()

def cancelSubscription(id, reason):
    url = PAYPAL_API_URL + f"/billing/subscriptions/{id}/cancel"
    data = {
        'reason': reason
    }
    
    response = requests.post(url=url, headers=PAYPAL_HEADER, auth=PAYPAL_AUTH, data=json.dumps(data))
    return response.json()