CARD_PREFIX = 'card_'
CARD_FIELDS_MAP = {
    'clicks': 'openCardCount',
    'atbs': 'addToCartCount',
    'shks': 'ordersCount',
    'orders': 'avgOrdersCountPerDay',
    'sum_price': 'ordersSumRub',
    'buyouts_count': 'buyoutsCount',
    'buyouts_sum': 'buyoutsSumRub',
    'buyouts_percent': 'buyoutsPercent',

}
CARD_TRAFFIC_EXTRACT_FIELDS = ['clicks', 'atbs', 'shks', 'orders', 'sum_price']
BUYOUT_EXTRACT_FIELDS = ['buyouts_count', 'buyouts_sum', 'buyouts_percent']

class CardFormatter:
    def extract_nm_stats_from_cards(self, cards):
        nm_stat = {}

        for card in cards:
            nm_id = card['nmID']
            statistics = card['statistics']['selectedPeriod']
            stocks = card['stocks']

            if nm_id in nm_stat:
                self._update_nm_stat_from_cards(nm_stat, nm_id, statistics, stocks)
            else:
                self._set_nm_stat_from_cards(nm_stat, nm_id, statistics, stocks)

        return nm_stat


    def _update_nm_stat_from_cards(self, stat, nm_id, statistics, stocks):
        for field in CARD_TRAFFIC_EXTRACT_FIELDS:
            prefixed_field = CARD_PREFIX + field
            stat[nm_id][prefixed_field] += statistics[CARD_FIELDS_MAP[field]]
        for field in BUYOUT_EXTRACT_FIELDS:
            if field == 'buyouts_percent':
                continue
            stat[nm_id][field] += statistics[CARD_FIELDS_MAP[field]]


    def _set_nm_stat_from_cards(self, stat, nm_id, statistics, stocks):
        stat[nm_id] = {}
        for field in CARD_TRAFFIC_EXTRACT_FIELDS:
            prefixed_field = CARD_PREFIX + field
            stat[nm_id][prefixed_field] = statistics[CARD_FIELDS_MAP[field]]
        for field in BUYOUT_EXTRACT_FIELDS:
            if field == 'buyouts_percent':
                stat[nm_id][field] = statistics['conversions'][CARD_FIELDS_MAP[field]]
            else:
                stat[nm_id][field] = statistics[CARD_FIELDS_MAP[field]]
