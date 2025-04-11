from .constant import ADV_METRICS, STOCK_METRICS, CARD_METRICS, FINREP_METRICS

class StatAggregator:
    def combine_stats(self, nm_ids, adv, card, stock, finrep):
        combined_stats = {}

        for id in nm_ids:
            combined_stats[id] = {}

            for metric in ADV_METRICS:
                combined_stats[id][metric] = adv.get(id, {}).get(metric, 0)
                
            for metric in STOCK_METRICS:
                combined_stats[id][metric] = stock.get(id, 0)

            for metric in CARD_METRICS:
                combined_stats[id][metric] = card.get(id, {}).get(metric, 0)

            for metric in FINREP_METRICS:
                combined_stats[id][metric] = finrep.get(id, {}).get(metric, 0)

        return combined_stats
