import requests
from datetime import datetime

cards_url = 'https://content-api.wildberries.ru/content/v2/get/cards/list'
cards_params = {'settings': {
    'filter': {'withPhoto': -1},
    'cursor': {'limit': 100}
}}
cards_stats_url = 'https://seller-analytics-api.wildberries.ru/api/v2/nm-report/detail'

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
        self.headers = {'Authorization': f'Bearer {api_token}'}
        self.cookies = cookies

    def get_cards(self):
        res = requests.post(cards_url, headers=self.headers, json=cards_params)
        cards = res.json()['cards']
        return cards

    def get_cards_stats(self, nm_ids: list[int], report_date: datetime):

        dash_report_date = self._get_dash_report_date(report_date)
        cards_stat_period = {
            'begin': f'{dash_report_date} {DAY_START_TIME}',
            'end': f'{dash_report_date} {DAY_END_TIME}'
        }

        params = {
            'nmIDs': nm_ids,
            'period': cards_stat_period,
            'page': 1,
        }

        res = requests.post(cards_stats_url, headers=self.headers, json=params)
        return res.json()['data']['cards']

    def get_adverts(self):
        adv_auto, adv_auction = [], []

        res_auto = requests.post(
            adv_url, headers=self.headers, params=adv_auto_parms)
        try:
            adv_auto = res_auto.json()
        except:
            print('нет авто кампаний')

        res_auction = requests.post(
            adv_url, headers=self.headers, params=adv_auction_parms)
        try:
            adv_auction = res_auction.json()
        except:
            print('нет аукционных кампаний')

        return adv_auto, adv_auction

    def get_adverts_stats(self, adv_ids: list[int], report_date: datetime):
        dash_report_date = self._get_dash_report_date(report_date)
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

        res = requests.post(adv_stats_url, headers=self.headers, json=params)
        res = res.json()
        
        if 'error' in res and 'there are no companies with correct intervals' in res['error']:
            print(f'в указанный период не было рекламных кампаний')
            return []
        else:
            return res

    def get_finreports(self, report_date: datetime):
        dot_report_date = self._get_dot_report_date(report_date)
        params = {
            'dateFrom': dot_report_date,
            'dateTo': dot_report_date
        }

        res = requests.get(finreports_url, headers=self.headers,
                           params=params, cookies=self.cookies)
        return res.json()['data']['reports']

    def get_finreport_stat_records(self, report_id: int):
        url = finreport_stat_url.format(report_id=report_id)
        res = requests.get(url, headers=self.headers, cookies=self.cookies)
        return res.json()['data']['details']

    def _get_dash_report_date(self, report_date: datetime):
        return report_date.strftime('%Y-%m-%d')

    def _get_dot_report_date(self, report_date: datetime):
        return report_date.strftime('%d.%m.%Y')
