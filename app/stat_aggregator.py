adv_metrics = [
    'adv_views', 'adv_clicks', 'adv_atbs', 'adv_orders', 'adv_shks', 'adv_sum', 'adv_sum_price'
]
card_metrics = ['card_clicks', 'card_atbs', 'card_orders', 'card_shks', 'card_sum_price',
    'buyouts_count', 'buyouts_sum', 'buyouts_percent', 'stock_mp', 'stock_wb'
]
card_total_metrics = ['card_clicks', 'card_atbs', 'card_shks', 'card_sum_price']
finrep_metrics = [
    'commissionPercent', 
    'deliveryRub',
    'penalty',
    'storageFee',
    'returnAmount',
    'acceptance',
    'deduction',

    'acquiringFee',
    'forPay',
    'ppvzKvwPrcBase', 
    'ppvzKvwPrc',
    'ppvzVwNds',
    'ppvzReward',
]

# TODO: столбцы Платная приемка из отчета и Прочие удержания из РНП 


class StatAggregator:
    def combine_stats(self, adv_stats, card_stats, finrep_stats):
        #self._log_nm_ids(adv_stats, card_stats, finrep_stats)

        all_nm_ids = list(set(
            list(adv_stats.keys()) +
            list(card_stats.keys()) +
            list(finrep_stats.keys())
        ))

        combined_stats = {}

        for id in all_nm_ids:
            combined_stats[id] = {}

            for metric in adv_metrics:
                combined_stats[id][metric] = adv_stats.get(
                    id, {}).get(metric, 0)

            for metric in card_metrics:
                field_name = metric if metric in card_total_metrics else metric
                combined_stats[id][field_name] = card_stats.get(
                    id, {}).get(metric, 0)

            for metric in finrep_metrics:
                field_name = metric
                combined_stats[id][field_name] = finrep_stats.get(
                    id, {}).get(metric, 0)

        return combined_stats


    def _log_nm_ids(self, adv_stats, card_stats, finrep_stats):
        print(f"nm from adv_stats: {list(adv_stats.keys())}\n"
              f"nm from card_stats: {list(card_stats.keys())}\n"
              f"nm from finrep_stats: {list(finrep_stats.keys())}")