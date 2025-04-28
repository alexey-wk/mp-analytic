from datetime import datetime
from app.utils.date_formatter import DateFormatter
from app.infrastructure.limitter import limit
from app.client.client import get_client_with_retries, get_auth_headers
from app.client.wb.constant import cards_url, cards_params, cards_stats_url, stocks_url, adv_url, adv_auto_parms, adv_auction_parms, adv_stats_url, finreports_day_url, finreports_week_url, finreport_stat_url, DAY_START_TIME, DAY_END_TIME, stocks_base_params
from app.server.model import WBAuthCookies

class WBClient:
    def __init__(self, cookies: WBAuthCookies, api_token: str):
        self.client = get_client_with_retries()
        self.headers = get_auth_headers(api_token, cookies.authorizev3)
        self.cookies = {
            'wbx-validation-key': cookies.wbxValidationKey,
            'x-supplier-id-external': cookies.xSupplierIdExternal,
            'WBTokenV3': cookies.wbTokenV3,
        }

    @limit(100)
    def get_cards(self):
        res = self.client.post(cards_url, headers=self.headers, json=cards_params)
        res.raise_for_status()
        return res.json()


    @limit(2)
    def get_cards_stats(self, nm_ids: list[int], report_date: datetime):
        params = self._create_card_stats_params(nm_ids, report_date)
        res = self.client.post(cards_stats_url, headers=self.headers, json=params)
        res.raise_for_status()
        return res.json()
        

    @limit(100)
    def get_stocks(self, nm_ids: list[int], report_date: datetime):
        params = self._create_stocks_params(nm_ids, report_date)
        res = self.client.post(stocks_url, cookies=self.cookies, json=params)
        res.raise_for_status()
        return res.json()


    @limit(100)
    def get_adverts(self):
        adv_auto, adv_auction = [], []

        res_auto = self.client.post(adv_url, headers=self.headers, params=adv_auto_parms)
        res_auto.raise_for_status()
        if res_auto.status_code != 204:
            adv_auto = res_auto.json()

        res_auction = self.client.post(adv_url, headers=self.headers, params=adv_auction_parms)
        res_auction.raise_for_status()
        if res_auction.status_code != 204:
            adv_auction = res_auction.json()

        return [*adv_auto, *adv_auction]


    @limit(1)
    def get_adverts_stats(self, adv_ids: list[int], report_date: datetime):
        params = self._create_adv_stats_params(adv_ids, report_date)
        res = self.client.post(adv_stats_url, headers=self.headers, json=params)
        if res.status_code == 400:
            return []

        res.raise_for_status()
        advs = res.json()
        return advs or []


    @limit(60)
    def get_dayly_finreports(self, from_date: datetime, to_date: datetime):
        params = self._create_finreport_params(from_date, to_date)
        res = self.client.get(finreports_day_url, cookies=self.cookies, params=params)
        res.raise_for_status()
        return res.json()


    @limit(60)
    def get_weekly_finreports(self, from_date: datetime, to_date: datetime):
        params = self._create_finreport_params(from_date, to_date)
        res = self.client.get(finreports_week_url, cookies=self.cookies, params=params)
        res.raise_for_status()
        return res.json()


    def get_finreport_stat_records(self, report_id: int):
        url = finreport_stat_url.format(report_id=report_id)
        res = self.client.get(url, cookies=self.cookies)
        res.raise_for_status()
        return res.json()['data']['details']


    def _create_card_stats_params(self, nm_ids: list[int], report_date: datetime):
        dash_report_date = DateFormatter.get_dash_report_date(report_date)

        return {
            'nmIDs': nm_ids,
            'page': 1,
            'period': {
                'begin': f'{dash_report_date} {DAY_START_TIME}',
                'end': f'{dash_report_date} {DAY_END_TIME}'
            },
        }


    def _create_stocks_params(self, nm_ids: list[int], report_date: datetime):
        dash_report_date = DateFormatter.get_dash_report_date(report_date)

        return {
            'nmIDs': nm_ids,
            'currentPeriod': {
                'start': dash_report_date,
                'end': dash_report_date
            },
            **stocks_base_params
        }


    def _create_adv_stats_params(self, adv_ids: list[int], report_date: datetime):
        dash_report_date = DateFormatter.get_dash_report_date(report_date)
        adv_stat_interval = {
            'begin': dash_report_date,
            'end': dash_report_date,
        }

        params = []
        for id in adv_ids:
            params.append({
                'id': id,
                'interval': adv_stat_interval,
            })

        return params

    
    def _create_finreport_params(self, from_date: datetime, to_date: datetime):
        dot_from_date = DateFormatter.get_dot_report_date(from_date)
        dot_to_date = DateFormatter.get_dot_report_date(to_date)

        return {
            'dateFrom': dot_from_date,
            'dateTo': dot_to_date
        }
