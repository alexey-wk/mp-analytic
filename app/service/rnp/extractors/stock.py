class StockExtractor:
    def extract_nm_stats_from_stocks(self, stocks_res: dict):
        stocks = stocks_res['data']
        nm_stat = {}

        for item in stocks['groups'][0]['items']:
            nm_id = item['nmID']
            nm_stat[nm_id] = item['metrics']['stockCount']
        
        return nm_stat
