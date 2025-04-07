class StockFormatter:
    def extract_nm_stats_from_stocks(self, stocks):
        nm_stat = {}

        for item in stocks['groups'][0]['items']:
            nm_id = item['nmID']
            nm_stat[nm_id] = item['metrics']['stockCount']
        
        return nm_stat
