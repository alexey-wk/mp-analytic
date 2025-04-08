ASIS_FIELDS = set([
    'nomenclatureId', 
    'nds', 
    'srid'
])
SUM_FIELDS = set([
    'deliveryRub',               # Услуги по доставке товара покупателю Пример: 417.18
    'penalty',                   # Общая сумма штрафов
    'storageFee',                # Хранение Пример: 487.81
    'returnAmount',              # Количество возвратов Пример: 1
    'acceptance',                # Стоимость платной приемки Пример: 0
    'deduction',                 # Прочие удержания/выплаты Пример: 0

    'acquiringFee',              # Эквайринг/Комиссии за организацию платежей Пример: 35.55
    'ppvzVwNds',                 # НДС с Вознаграждения Вайлдберриз Пример: -26.28
    'ppvzSalesCommission',       # Вознаграждение с продаж до вычета услуг поверенного, без НДС Пример: -145.58
    'forPay',                    # К перечислению Продавцу за реализованный Товар Пример: 1821.47
    'ppvzReward',                # Возмещение за выдачу и возврат товаров на ПВЗ Пример: 46.996
])
AVG_FIELDS = set([
    'commissionPercent',          # Размер кВВ, % Пример: 16.5
    'ppvzKvwPrcBase',             # Размер  кВВ без НДС, % Базовый Пример:  0.1375
    'ppvzKvwPrc'                  # Итоговый кВВ без НДС, % Пример: -0.0458
])

# также доступны для извлечения поля: salePercent, supplierSpp, costAmount, customerReward, costPrice,
# productDiscountForReport, supplierPromo, retailCommission, forPayNds,
# is_kgvp_v2, additionalPayment, dlvPrc, rebillLogisticCost
# ppvzForPay, goodsIncomeID, currency
# acquiringPercent          # Размер комиссии за эквайринг/Комиссии за организацию платежей, % Пример: 1.7
# deliveryAmount            # Количество доставок Пример: 1
# quantity                  # Кол-во Пример: 3
# ppvzVw                    # Вознаграждение с продаж до вычета услуг поверенного, без НДС Пример:  -131.416666666666666
# retailPrice               # Цена розничная Пример: 2220
# retailPriceWithDiscountRub# Цена розничная с учетом согласованной скидки Пример: 1989
# retailAmount              # Вайлдберриз реализовал Товар (Пр) Пример: 1696


class FinReportFormatter:
    def extract_finreport_ids(self, finrepsorts_res: dict):
        finreps = finrepsorts_res['data']['reports']
        ids = [report['id'] for report in finreps]
        return ids

    def extract_nm_stats_from_finrep_records(self, raw_finrep_records_res: dict):
        raw_finrep_records = raw_finrep_records_res['data']['details']
        finrep_records = self._merge_records_by_srid(raw_finrep_records)

        nm_finrep_stats = {}

        for record in finrep_records:
            id = record['nomenclatureId']
            if id == 0:
                continue

            if id not in nm_finrep_stats:
                nm_finrep_stats[id] = record.copy()
            else:
                for field_name, val in record.items():
                    if field_name in SUM_FIELDS:
                        nm_finrep_stats[id][field_name] += val
                    elif field_name in AVG_FIELDS:
                        nm_finrep_stats[id][field_name] = (
                            nm_finrep_stats[id][field_name] + val) / 2
                    else:
                        nm_finrep_stats[id][field_name] = val

            nm_finrep_stats[id]['nmId'] = id

        return nm_finrep_stats

    def _merge_records_by_srid(self, raw_finrep_records):
        finrep_records_merged = {}

        for record in raw_finrep_records:
            srid = record['srid']
            if srid not in finrep_records_merged:
                finrep_records_merged[srid] = record.copy()
            else:
                for field_name, value in record.items():
                    if field_name in finrep_records_merged[srid]:
                        finrep_records_merged[srid][field_name] = finrep_records_merged[srid][field_name] or value
                    else:
                        finrep_records_merged[srid][field_name] = value

        return list(finrep_records_merged.values())
