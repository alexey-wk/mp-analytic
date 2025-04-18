# Рекламные кампании
ADV_PREFIX = 'adv_'
ADV_EXTRACT_FIELDS = ['views', 'clicks', 'atbs', 'orders', 'shks', 'sum', 'sum_price']

# Карточки товара
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

# Финансовые отчеты
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
AVG_POSITIVE_FIELDS = set([
    'retailPrice',                # Цена розничная Пример: 2220
    'nds',                        # НДС Пример: 20
])
# также доступны для извлечения поля: salePercent, supplierSpp, costAmount, customerReward, costPrice,
# productDiscountForReport, supplierPromo, retailCommission, forPayNds,
# is_kgvp_v2, additionalPayment, dlvPrc, rebillLogisticCost, nomenclatureId, srid
# ppvzForPay, goodsIncomeID, currency
# acquiringPercent          # Размер комиссии за эквайринг/Комиссии за организацию платежей, % Пример: 1.7
# deliveryAmount            # Количество доставок Пример: 1
# quantity                  # Кол-во Пример: 3
# ppvzVw                    # Вознаграждение с продаж до вычета услуг поверенного, без НДС Пример:  -131.416666666666666
# retailPriceWithDiscountRub# Цена розничная с учетом согласованной скидки Пример: 1989
# retailAmount              # Вайлдберриз реализовал Товар (Пр) Пример: 1696
