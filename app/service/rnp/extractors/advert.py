from .constant import ADV_EXTRACT_FIELDS, ADV_PREFIX

class AdvertExtractor:
    def extract_nm_ids_from_cards_res(self, cards_res: dict):
        cards = cards_res['cards']
        nm_ids = [card['nmID'] for card in cards]
        return nm_ids
    

    def get_all_adv_ids(self, advs: list[dict]):
        all_advs = self._group_nm_ids_by_adverts(advs)
        return list(all_advs.keys())


    def _group_nm_ids_by_adverts(self, advs: list[dict]):
        adv_nms = {}

        for adv in advs:
            id = adv['advertId']

            if 'unitedParams' in adv:
                adv_nms[id] = []
                for param in adv['unitedParams']:
                    adv_nms[id].extend(param['nms'])
                    
            elif 'autoParams' in adv:
                adv_nms[id] = adv['autoParams']['nms']

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
