from enum import IntFlag
from typing import Any
import requests
from toolkit.behaviour.command import Command
from paystack.util import PayStackGatewayFlag, BusinessDataObject, PayStackRestUrl


__all__ = ('fetch_settlements',)


class SettlementCommandRank(IntFlag):
    FETCH_SETTLEMENTS = 239


def fetch_settlements_cmd(**kwargs) -> Any:
    bdo = kwargs.pop('config')
    if not isinstance(bdo, BusinessDataObject):
        raise ValueError('Invalid Business Data Object')
    bdo.update(**kwargs)
    query = bdo.data
    url = bdo.url(PayStackRestUrl.FETCH_SETTLEMENTS_URL)
    return requests.get(url=url, params=query, headers=bdo.header)


fetch_settlements = Command(cmd=fetch_settlements_cmd,
                            group=PayStackGatewayFlag.SETTLEMENTS,
                            rank=SettlementCommandRank.FETCH_SETTLEMENTS, label=None)
