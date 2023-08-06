import datetime
from typing import List, OrderedDict, Optional
from pydash import py_

import zeep
from zeep.wsse.username import UsernameToken

import logging


class Pager:
    pageSize: int
    pageNumber: int


class SoapClient:
    def __init__(self, url: str, login: str, password: str):
        token = UsernameToken(login, password)
        self.client = zeep.Client(url, wsse=token)

    @staticmethod
    def debug_mode():
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger("suds.client").setLevel(logging.DEBUG)

    @staticmethod
    def _convert_to_list_of_dicts(operations: List[OrderedDict]):
        results = []
        for item in operations:
            elm = dict()
            elm["id"] = item.get("id")
            for d in item.get("attribute"):
                elm[d["key"]] = (
                    d["value"] if d["key"] != "sourceamount" else float(d["value"])
                )
            results.append(elm)
        return results

    def get_pager(
        self, page_number: Optional[int] = 1, page_size: Optional[int] = 100
    ) -> Pager:
        assert page_size <= 1000
        factory = self.client.type_factory("ns0")
        return factory.Pager(pageSize=page_size, pageNumber=page_number)

    def _get_operation_list(
        self,
        date_from: datetime.datetime,
        date_to: datetime.datetime,
        page_size: Optional[int] = 1000,
        page_number: Optional[int] = 1,
    ) -> List[OrderedDict]:
        ftr = {"dateFrom": date_from, "dateTo": date_to}
        pager = self.get_pager(page_size=page_size, page_number=page_number)
        response = self.client.service.FindOperationsList(pager=pager, filter=ftr)
        result = zeep.helpers.serialize_object(response)
        return result.get("operation", [])

    def get_operations(
        self,
        date_from: datetime.datetime,
        date_to: datetime.datetime,
        page_size: Optional[int] = 1000,
        page_number: Optional[int] = 1,
    ) -> List[dict]:
        result = self._get_operation_list(
            date_from, date_to, page_size=page_size, page_number=page_number
        )
        return self._convert_to_list_of_dicts(result)

    def get_sum_per_period(
        self, date_from: datetime.datetime, date_to: datetime.datetime
    ) -> int:
        operations = self._get_operation_list(date_from, date_to)
        return (
            py_(operations)
            .map("attribute")
            .flatten()
            .reject(lambda elm: py_.get(elm, ["key"]) != "sourceamount")
            .map_("value")
            .map(float)
            .sum()
            .value()
        )

    def get_operation_sum(self, operation_id: int) -> int:
        # result = self.client.service.
        pass
