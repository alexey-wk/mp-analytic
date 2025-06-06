cards_url = 'https://content-api.wildberries.ru/content/v2/get/cards/list'
cards_params = {'settings': {
    'filter': {'withPhoto': -1},
    'cursor': {'limit': 100}
}}

cards_stats_url = 'https://seller-analytics-api.wildberries.ru/api/v2/nm-report/detail'

stocks_url = 'https://seller-content.wildberries.ru/ns/analytics-api/content-analytics/api/v2/stocks-report/report'
stocks_base_params = {
    'stockType': '',
    'skipDeletedNm': False,
    'availabilityFilters': [],
    'orderBy': {
        'field': 'ordersCount',
        'mode': 'desc'
    }
}


adv_url = 'https://advert-api.wildberries.ru/adv/v1/promotion/adverts'
adv_auto_parms = {'status': 8}
adv_auction_parms = {'status': 9}

adv_stats_url = 'https://advert-api.wildberries.ru/adv/v2/fullstats'

finreports_day_url = 'https://seller-services.wildberries.ru/ns/reports/seller-wb-balance/api/v1/reports'
finreports_week_url = 'https://seller-services.wildberries.ru/ns/reports/seller-wb-balance/api/v1/reports-weekly'
finreport_stat_url = "https://seller-services.wildberries.ru/ns/reports/seller-wb-balance/api/v1/reports/{report_id}/details"

DAY_START_TIME = '00:00:00'
DAY_END_TIME = '23:59:59'
