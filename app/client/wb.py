import requests
import logging
from urllib3.util import Retry
from requests.adapters import HTTPAdapter
from datetime import datetime
from app.date_formatter import DateFormatter
from app.infrastructure.limitter import limit_calls

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
        self.logger = logging.getLogger(__name__)
        self.headers = {'Authorization': f'Bearer {api_token}'}
        self.cookies = cookies
        
        self.client = requests.Session()
        retry_strategy = Retry(
            total=3,
            status_forcelist=[500, 502, 503, 504],
            backoff_factor=2,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.client.mount("https://", adapter)

    @limit_calls(max_calls=100)
    def get_cards(self):
        res = self.client.post(cards_url, headers=self.headers, json=cards_params)
        res.raise_for_status()
        cards = res.json()['cards']
        return cards

    @limit_calls(max_calls=2)
    def get_cards_stats(self, nm_ids: list[int], report_date: datetime):
        dash_report_date = DateFormatter.get_dash_report_date(report_date)
        cards_stat_period = {
            'begin': f'{dash_report_date} {DAY_START_TIME}',
            'end': f'{dash_report_date} {DAY_END_TIME}'
        }

        params = {
            'nmIDs': nm_ids,
            'period': cards_stat_period,
            'page': 1,
        }

        try:
            res = self.client.post(cards_stats_url, headers=self.headers, json=params)

            res.raise_for_status()
            return res.json()['data']['cards']
        except Exception as e:
            self.logger.error(f'Error getting cards stats: {e}')
            raise e
        
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
        return res.json()['data']

    @limit_calls(max_calls=100)
    def get_adverts(self):
        adv_auto, adv_auction = [], []

        try:
            res_auto = self.client.post(
                adv_url, headers=self.headers, params=adv_auto_parms)
            res_auto.raise_for_status()
        except Exception as e:
            self.logger.error(f'Error getting auto adverts: {e}')
            raise e

        try:
            adv_auto = res_auto.json()
        except:
            pass

        try:
            res_auction = self.client.post(
                adv_url, headers=self.headers, params=adv_auction_parms)
            res_auction.raise_for_status()
        except Exception as e:
            self.logger.error(f'Error getting auction adverts: {e}')
            raise e

        try:
            adv_auction = res_auction.json()
        except:
            pass

        return adv_auto, adv_auction

    @limit_calls(max_calls=1, time_frame=60)
    def get_adverts_stats(self, adv_ids: list[int], report_date: datetime):
        dash_report_date = DateFormatter.get_dash_report_date(report_date)
        params = []

        adv_stat_interval = {
            'begin': dash_report_date,
            'end': dash_report_date,
        }

        for id in adv_ids:
            params.append({
                'id': id,
                'interval': adv_stat_interval,
            })

        res = self.client.post(adv_stats_url, headers=self.headers, json=params)
        if res.status_code == 400:
            return []
        elif res.status_code != 200:
            err = res.json()
            self.logger.error(f'Error code {res.status_code} getting adverts stats: {err}')
            raise Exception(err)
        else:
            return res.json()


    @limit_calls(max_calls=60)
    def get_finreports(self, report_date: datetime):
        dot_report_date = DateFormatter.get_dot_report_date(report_date)
        params = {
            'dateFrom': dot_report_date,
            'dateTo': dot_report_date
        }

        try:
            res = self.client.get(finreports_url, headers=self.headers,
                               params=params, cookies=self.cookies)
            res.raise_for_status()
        except Exception as e:
            self.logger.error(f'Error getting finreports: {e}')
            raise e

        return res.json()['data']['reports']

    @limit_calls(max_calls=60)
    def get_finreport_stat_records(self, report_id: int):
        url = finreport_stat_url.format(report_id=report_id)
        try:
            res = self.client.get(url, headers=self.headers, cookies=self.cookies)
            res.raise_for_status()
        except Exception as e:
            self.logger.error(f'Error getting finreport stat records: {e}')
            raise e

        return res.json()['data']['details']
