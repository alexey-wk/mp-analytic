import logging
from datetime import datetime
from app.date_formatter import DateFormatter
from app.infrastructure.limitter import limit_calls
from app.client.client import get_client_with_retries, get_auth_headers

cards_url = 'https://content-api.wildberries.ru/content/v2/get/cards/list'
cards_params = {'settings': {
    'filter': {'withPhoto': -1},
    'cursor': {'limit': 100}
}}
cards_stats_url = 'https://seller-analytics-api.wildberries.ru/api/v2/nm-report/detail'

stocks_url = 'https://seller-content.wildberries.ru/ns/analytics-api/content-analytics/api/v2/stocks-report/report'

adv_url = 'https://advert-api.wildberries.ru/adv/v1/promotion/adverts'
adv_auto_parms = {'status': 8}
adv_auction_parms = {'status': 9}
adv_stats_url = 'https://advert-api.wildberries.ru/adv/v2/fullstats'

finreports_url = 'https://seller-services.wildberries.ru/ns/reports/seller-wb-balance/api/v1/reports'
finreport_stat_url = "https://seller-services.wildberries.ru/ns/reports/seller-wb-balance/api/v1/reports/{report_id}/details"

DAY_START_TIME = '00:00:00'
DAY_END_TIME = '23:59:59'


class WBClient:
    def __init__(self, cookies: dict, api_token: str):
        self.client = get_client_with_retries()
        self.logger = logging.getLogger(__name__)
        self.headers = get_auth_headers(api_token)
        self.cookies = cookies


    @limit_calls(max_calls=100)
    def get_cards(self):
        res = self.client.post(cards_url, headers=self.headers, json=cards_params)
        res.raise_for_status()
        return res.json()


    @limit_calls(max_calls=2)
    def get_cards_stats(self, nm_ids: list[int], report_date: datetime):
        dash_report_date = DateFormatter.get_dash_report_date(report_date)
        params = {
            'nmIDs': nm_ids,
            'page': 1,
            'period': {
                'begin': f'{dash_report_date} {DAY_START_TIME}',
                'end': f'{dash_report_date} {DAY_END_TIME}'
            },
        }

        res = self.client.post(cards_stats_url, headers=self.headers, json=params)
        res.raise_for_status()
        return res.json()
        

    @limit_calls(max_calls=100)
    def get_stocks(self, nm_ids: list[int], report_date: datetime):
        dash_report_date = DateFormatter.get_dash_report_date(report_date)

        stocks_params = {
            'nmIDs': nm_ids,
            'currentPeriod': {
                'start': dash_report_date,
                'end': dash_report_date
            },
            'stockType': '',
            'skipDeletedNm': False,
            'availabilityFilters': [],
            'orderBy': {
                'field': 'ordersCount',
                'mode': 'desc'
            }
        }

        res = self.client.post(stocks_url, cookies=self.cookies, json=stocks_params)
        res.raise_for_status()
        return res.json()


    @limit_calls(max_calls=100)
    def get_adverts(self):
        adv_auto, adv_auction = [], []

        res_auto = self.client.post(adv_url, headers=self.headers, params=adv_auto_parms)
        res_auto.raise_for_status()
        try:
            adv_auto = res_auto.json()
        except:
            pass

        res_auction = self.client.post(adv_url, headers=self.headers, params=adv_auction_parms)
        res_auction.raise_for_status()
        try:
            adv_auction = res_auction.json()
        except:
            pass

        return adv_auto, adv_auction


    @limit_calls(max_calls=1, time_frame=60)
    def get_adverts_stats(self, adv_ids: list[int], report_date: datetime):
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

        res = self.client.post(adv_stats_url, headers=self.headers, json=params)
        if res.status_code == 400:
            return []
        elif res.status_code != 200:
            res.raise_for_status()
            return []
        
        return res.json()


    @limit_calls(max_calls=60)
    def get_finreports(self, report_date: datetime):
        dot_report_date = DateFormatter.get_dot_report_date(report_date)
        params = {
            'dateFrom': dot_report_date,
            'dateTo': dot_report_date
        }

        res = self.client.get(finreports_url, headers=self.headers, params=params, cookies=self.cookies)
        res.raise_for_status()
        return res.json()


    @limit_calls(max_calls=60)
    def get_finreport_stat_records(self, report_id: int):
        url = finreport_stat_url.format(report_id=report_id)

        res = self.client.get(url, headers=self.headers, cookies=self.cookies)
        res.raise_for_status()
        return res.json()
