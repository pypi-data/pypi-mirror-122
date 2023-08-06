import json
from enum import IntFlag
from typing import Any
import requests
from toolkit.behaviour.command import Command
from paystack.util import PayStackGatewayFlag, BusinessDataObject, PayStackRestUrl 


__all__ = ('initialize_transaction', 'verify_transaction', 'list_transactions', 'fetch',
           'charge_authorization', 'view_transaction_timeline', 'transaction_totals',
           'export_transactions', 'request_reauthorization', 'check_authorization')


class TransactionCommandRank(IntFlag):
    """
    Define the various phases of the page workflow as command ranks
    """
    INITIALIZE = 2
    VERIFY = 3
    LIST_TRANSACTIONS = 5
    FETCH = 7
    CHARGE_AUTHORIZATION = 11
    VIEW_TRANSACTION_TIMELINE = 13
    TRANSACTION_TOTALS = 17
    EXPORT_TRANSACTIONS = 19
    REQUEST_REAUTHORIZATION = 23
    CHECK_AUTHORIZATION = 29


class TransactionBusinessObject(BusinessDataObject):

    def __init__(self, **kwargs):
        super(TransactionBusinessObject, self).__init__(**kwargs)


def initialize_cmd(**kwargs) -> Any:
    bdo = kwargs.pop('config')
    if not isinstance(bdo, BusinessDataObject):
        raise ValueError('Invalid Business Data Object')
    bdo.update(**kwargs)
    data = bdo.data
    url = bdo.url(PayStackRestUrl.INITIALIZE_TRANSACTION_URL)
    return requests.post(url=url, data=json.dumps(data), headers=bdo.header)


def verify_cmd(**kwargs) -> Any:
    bdo = kwargs.pop('config')
    if not isinstance(bdo, BusinessDataObject):
        raise ValueError('Invalid Business Data Object')
    bdo.update(**kwargs)
    data = bdo.data
    transaction_id = data.get('reference') or data.get('transaction_id')
    url = bdo.url(PayStackRestUrl.VERIFY_TRANSACTION_URL, [('reference', transaction_id)])
    return requests.get(url, headers=bdo.header)


def list_transactions_cmd(**kwargs) -> Any:
    bdo = kwargs.pop('config')
    if not isinstance(bdo, BusinessDataObject):
        raise ValueError('Invalid Business Data Object')
    bdo.update(**kwargs)
    url = bdo.url(PayStackRestUrl.LIST_TRANSACTIONS_URL, params=bdo.data)
    return requests.get(url, headers=bdo.header)


def fetch_cmd(**kwargs) -> Any:
    bdo = kwargs.pop('config')
    if not isinstance(bdo, BusinessDataObject):
        raise ValueError('Invalid Business Data Object')
    bdo.update(**kwargs)
    query = bdo.data
    transaction_id = query.get('transaction_id') or query.get('reference')
    url = bdo.url(PayStackRestUrl.FETCH_TRANSACTION_URL, [('id', transaction_id)])
    return requests.get(url, headers=bdo.header)


def charge_authorization_cmd(**kwargs) -> Any:
    bdo = kwargs.pop('config')
    if not isinstance(bdo, BusinessDataObject):
        raise ValueError('Invalid Business Data Object')
    bdo.update(**kwargs)
    charge = bdo.data
    url = bdo.url(PayStackRestUrl.CHANGE_AUTHORIZATION_URL)
    return requests.post(url=url, data=json.dumps(charge), headers=bdo.header)


def view_transaction_timeline_cmd(**kwargs) -> Any:
    bdo = kwargs.pop('config')
    if not isinstance(bdo, BusinessDataObject):
        raise ValueError('Invalid Business Data Object')
    bdo.update(**kwargs)
    data = bdo.data
    url = bdo.url(PayStackRestUrl.VIEW_TRANSACTION_TIMELINE_URL)
    return requests.post(url=url, data=json.dumps(data), headers=bdo.header)


def transaction_totals_cmd(**kwargs) -> Any:
    bdo = kwargs.pop('config')
    if not isinstance(bdo, BusinessDataObject):
        raise ValueError('Invalid Business Data Object')
    bdo.update(**kwargs)
    query_params = bdo.data
    url = bdo.url(PayStackRestUrl.TRANSACTION_TOTALS_URL)
    return requests.get(url=url, params=query_params, headers=bdo.header)


def export_transactions_cmd(**kwargs) -> Any:
    bdo = kwargs.pop('config')
    if not isinstance(bdo, BusinessDataObject):
        raise ValueError('Invalid Business Data Object')
    bdo.update(**kwargs)
    query_params = bdo.data
    url = bdo.url(PayStackRestUrl.EXPORT_TRANSACTIONS_URL)
    return requests.get(url=url, params=query_params, headers=bdo.header)


def request_reauthorization_cmd(**kwargs) -> Any:
    bdo = kwargs.pop('config')
    if not isinstance(bdo, BusinessDataObject):
        raise ValueError('Invalid Business Data Object')
    bdo.update(**kwargs)
    data = bdo.data
    url = bdo.url(PayStackRestUrl.REQUEST_REAUTHORIZATION_URL)
    return requests.post(url, data=json.dumps(data), headers=bdo.header)


def check_authorization_cmd(**kwargs) -> Any:
    bdo = kwargs.pop('config')
    if not isinstance(bdo, BusinessDataObject):
        raise ValueError('Invalid Business Data Object')
    bdo.update(**kwargs)
    data = bdo.data
    header = bdo.header
    url = bdo.url(PayStackRestUrl.CHECK_AUTHORIZATION_URL)
    return requests.post(url, data=json.dumps(data), headers=header)


initialize_transaction = Command(cmd=initialize_cmd, group=PayStackGatewayFlag.TRANSACTIONS,
                                 rank=TransactionCommandRank.INITIALIZE, label=None)
verify_transaction = Command(cmd=verify_cmd, group=None, rank=TransactionCommandRank.VERIFY,
                             label=None)
list_transactions = Command(cmd=list_transactions_cmd, group=PayStackGatewayFlag.TRANSACTIONS,
                            rank=TransactionCommandRank.LIST_TRANSACTIONS, label=None)
fetch = Command(cmd=fetch_cmd, group=PayStackGatewayFlag.TRANSACTIONS,
                rank=TransactionCommandRank.FETCH, label=None)
charge_authorization = Command(cmd=charge_authorization_cmd,
                               group=PayStackGatewayFlag.TRANSACTIONS,
                               rank=TransactionCommandRank.CHARGE_AUTHORIZATION, label=None)
view_transaction_timeline = Command(cmd=view_transaction_timeline_cmd,
                                    group=PayStackGatewayFlag.TRANSACTIONS,
                                    rank=TransactionCommandRank.VIEW_TRANSACTION_TIMELINE,
                                    label=None)
transaction_totals = Command(cmd=transaction_totals_cmd,
                             group=PayStackGatewayFlag.TRANSACTIONS,
                             rank=TransactionCommandRank.TRANSACTION_TOTALS, label=None)
export_transactions = Command(cmd=export_transactions_cmd,
                              group=PayStackGatewayFlag.TRANSACTIONS,
                              rank=TransactionCommandRank.EXPORT_TRANSACTIONS, label=None)
request_reauthorization = Command(cmd=request_reauthorization_cmd,
                                  group=PayStackGatewayFlag.TRANSACTIONS,
                                  rank=TransactionCommandRank.REQUEST_REAUTHORIZATION,
                                  label=None)
check_authorization = Command(cmd=check_authorization_cmd, group=PayStackGatewayFlag,
                              rank=TransactionCommandRank.CHECK_AUTHORIZATION, label=None)
