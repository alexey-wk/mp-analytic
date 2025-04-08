
ADV_PREFIX = 'adv_'
ADV_TRAFFIC_EXTRACT_FIELDS = ['views', 'clicks',
                              'atbs', 'orders', 'shks', 'sum', 'sum_price']
# также доступны для извлечения поля: ctr, cpc и cr


class AdvertFormatter:
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
                        if nm_id in nm_stat:
                            self._update_nm_stat_from_advs(nm_stat, nm_id, nm)
                        else:
                            self._set_nm_stat_from_advs(nm_stat, nm_id, nm)
        return nm_stat

    def _update_nm_stat_from_advs(self, stat, nm_id, nm):
        for field in ADV_TRAFFIC_EXTRACT_FIELDS:
            prefixed_field = ADV_PREFIX + field
            stat[nm_id][prefixed_field] += nm[field]

    def _set_nm_stat_from_advs(self, stat, nm_id, nm):
        stat[nm_id] = {}
        for field in ADV_TRAFFIC_EXTRACT_FIELDS:
            prefixed_field = ADV_PREFIX + field
            stat[nm_id][prefixed_field] = nm[field]
