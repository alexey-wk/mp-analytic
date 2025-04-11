from .constant import ADV_EXTRACT_FIELDS, ADV_PREFIX

class AdvertExtractor:
    def extract_nm_ids_from_cards_res(self, cards_res: dict):
        cards = cards_res['cards']
        nm_ids = [card['nmID'] for card in cards]
        return nm_ids


    def group_nm_ids_by_adverts(self, adv_auto: list[dict], adv_auction: list[dict]):
        adv_nms = {}

        for adv in adv_auto:
            id = adv['advertId']
            adv_nms[id] = adv['autoParams']['nms']

        for adv in adv_auction:
            id = adv['advertId']
            adv_nms[id] = []
            for param in adv['unitedParams']:
                adv_nms[id].extend(param['nms'])

        return adv_nms


    def extract_nm_stats_from_advs(self, advs):
        nm_stat = {}

        for adv in advs:
            for day in adv['days']:
                for app in day['apps']:
                    for nm in app['nm']:
                        nm_id = nm['nmId']
                        if nm_id not in nm_stat:
                            nm_stat[nm_id] = {}

                        for field in ADV_EXTRACT_FIELDS:
                            self._update_field_value(nm, nm_stat, nm_id, field)

        return nm_stat


    def _update_field_value(self, nm, nm_stat, nm_id, field):
        prefixed_field = ADV_PREFIX + field
        val = nm[field]
        nm_stat[nm_id][prefixed_field] = nm_stat[nm_id].get(prefixed_field, 0) + val
