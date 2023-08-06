from enum import IntFlag
from typing import Any
import requests
from toolkit.behaviour.command import Command
from paystack.util import PayStackGatewayFlag, BusinessDataObject, PayStackRestUrl


__all__ = 'list_banks',


class MiscCommandRank(IntFlag):
    LIST_BANKS = 461


def list_banks_cmd(**kwargs) -> Any:
    bdo = kwargs.pop('config')
    if not isinstance(bdo, BusinessDataObject):
        raise ValueError('Invalid Business Data Object')
    bdo.update(**kwargs)
    url = bdo.url(PayStackRestUrl.LIST_BANKS_URL)
    return requests.get(url=url, headers=bdo.header)


list_banks = Command(cmd=list_banks_cmd, group=PayStackGatewayFlag.MISCELLANEOUS,
                     rank=MiscCommandRank.LIST_BANKS, label=None)
