REPORT_FIELDS = {
    'adv_views': {
        'display_text': 'Просмотры (внутр. траф.)',
        'tag': 'adv_views'
    },
    'adv_clicks': {
        'display_text': 'Клики (внутр. траф.)',
        'tag': 'adv_clicks'
    },
    'adv_atbs': {
        'display_text': 'Корзины (внутр. траф.)',
        'tag': 'adv_atbs'
    },
    'adv_orders': {
        'display_text': 'Заказы (внутр. траф.)',
        'tag': 'adv_orders'
    },
    'adv_shks': {
        'display_text': 'Товара в заказах (внутр. траф.)',
        'tag': 'adv_shks'
    },
    'adv_sum': {
        'display_text': 'Затраты (внутр. траф.)',
        'tag': 'adv_sum'
    },
    'adv_sum_price': {
        'display_text': 'Заказов на сумму (внутр. траф.)',
        'tag': 'adv_sum_price'
    },

    'card_clicks': {
        'display_text': 'Клики (карточка)',
        'tag': 'card_clicks'
    },
    'card_atbs': {
        'display_text': 'Корзины (карточка)',
        'tag': 'card_atbs'
    },
    'card_shks': {
        'display_text': 'Товара в заказах (карточка)',
        'tag': 'card_shks'
    },
    'card_orders': {
        'display_text': 'Заказов (карточка)',
        'tag': 'card_orders'
    },
    'card_sum_price': {
        'display_text': 'Заказов на сумму (карточка)',
        'tag': 'card_sum_price'
    },
    'buyouts_count': {
        'display_text': 'Количество выкупов',
        'tag': 'buyouts_count'
    },
    'buyouts_sum': {
        'display_text': 'Сумма выкупов',
        'tag': 'buyouts_sum'
    },
    'buyouts_percent': {
        'display_text': 'Выкупы, %',
        'tag': 'buyouts_percent'
    },
    'stock_count': {
        'display_text': 'Остаток на складах',
        'tag': 'stock_count'
    },
    'deliveryRub': {
        'display_text': 'Услуги по доставке товара покупателю',
        'tag': 'delivery_fee'
    },
    'penalty': {
        'display_text': 'Общая сумма штрафов',
        'tag': 'penalty_fee'
    },
    'storageFee': {
        'display_text': 'Затраты на хранение',
        'tag': 'storage_fee'
    },
    'returnAmount': {
        'display_text': 'Количество возвратов',
        'tag': 'return_amount'
    },
    'commissionPercent': {
        'display_text': 'Размер кВВ, %',
        'tag': 'commission_percent'
    },
    'acceptance': {
        'display_text': 'Стоимость платной приемки',
        'tag': 'acceptance_fee'
    },
    'deduction': {
        'display_text': 'Прочие удержания/выплаты',
        'tag': 'deduction_fee'
    },
    'retailPrice': {
        'display_text': 'Цена розничная',
        'tag': 'retail_price'
    },
    'nds': {
        'display_text': 'НДС',
        'tag': 'nds_percent'
    },

    'acquiringFee': {
        'display_text': 'Эквайринг/Комиссии за организацию платежей',
        'tag': 'acquiring_fee'
    },
    'forPay': {
        'display_text': 'К перечислению Продавцу за реализованный Товар',
        'tag': 'pay_to_seller'
    },
    'ppvzKvwPrcBase': {
        'display_text': 'Размер кВВ без НДС, % Базовый',
        'tag': 'commission_no_vat_base_percent'
    },
    'ppvzKvwPrc': {
        'display_text': 'Итоговый кВВ без НДС, %',
        'tag': 'commission_no_vat_final_percent'
    },
    'ppvzVwNds': {
        'display_text': 'НДС с Вознаграждения Вайлдберриз',
        'tag': 'vat_on_commission'
    },
    'ppvzReward': {
        'display_text': 'Возмещение за выдачу и возврат товаров на ПВЗ',
        'tag': 'pvz_fee'
    },
}

REPORT_FIELDS_ITEMS = REPORT_FIELDS.items()

TAG_TO_FIELD_NAME = {
    val['tag']: key for key, val in REPORT_FIELDS_ITEMS
}

TAG_COL_IDX = 0
DATE_ROW_IDX = 1
NM_ID_ROW_IDX = 1
NM_ID_COL_IDX = 2
DISPLAY_TEXT_MAPPING = {field: info['display_text'] for field, info in REPORT_FIELDS.items()}
