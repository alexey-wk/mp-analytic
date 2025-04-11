from .constant import CARD_TRAFFIC_EXTRACT_FIELDS, CARD_PREFIX, CARD_FIELDS_MAP, BUYOUT_EXTRACT_FIELDS

class CardExtractor:
    def extract_nm_stats_from_cards_stats(self, cards_res: dict):
        nm_stat = {}

        for card in cards_res['data']['cards']:
            nm_id = card['nmID']
            statistics = card['statistics']['selectedPeriod']
            
            if nm_id not in nm_stat:
                nm_stat[nm_id] = {}
            
            for field in CARD_TRAFFIC_EXTRACT_FIELDS:
                prefixed_field = CARD_PREFIX + field
                nm_stat[nm_id][prefixed_field] = nm_stat[nm_id].get(prefixed_field, 0) + statistics[CARD_FIELDS_MAP[field]]
            
            for field in BUYOUT_EXTRACT_FIELDS:
                if field.endswith('_percent'):
                    nm_stat[nm_id][field] = statistics['conversions'][CARD_FIELDS_MAP[field]]
                else:
                    nm_stat[nm_id][field] = nm_stat[nm_id].get(field, 0) + statistics[CARD_FIELDS_MAP[field]]

        return nm_stat
