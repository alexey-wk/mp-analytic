import pandas as pd
from .constant import ADV_METRICS, STOCK_METRICS, CARD_METRICS, FINREP_METRICS

pd.set_option('display.float_format', '{:.2f}'.format)

class WBAggregator:
    def aggregate_stats(self, nm_ids, adv, card, stock, finrep):
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

        return pd.DataFrame(combined_stats).abs()
