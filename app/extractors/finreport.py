from .constant import SUM_FIELDS, AVG_POSITIVE_FIELDS


class FinReportExtractor:
    def extract_finrep_ids(self, finreps_res: dict):
        finreps = finreps_res['data']['reports']
        ids = [rep['id'] for rep in finreps]
        return ids
    

    def extract_nm_stats_from_finrep_records(self, raw_finrep_records):
        finrep_records = self._merge_records_by_srid(raw_finrep_records)

        nm_stats = {}

        for record in finrep_records:
            id = record['nomenclatureId']
            if id == 0:
                continue

            if id not in nm_stats:
                nm_stats[id] = record.copy()
                nm_stats[id]['nmId'] = id
                continue

            for field_name, val in record.items():
                if field_name in SUM_FIELDS:
                    self._increment(nm_stats, id, field_name, val)
                elif field_name in AVG_POSITIVE_FIELDS:
                    self._average_positive(nm_stats, id, field_name, val)
        return nm_stats



    def _merge_records_by_srid(self, raw_records):
        merged_records = {}

        for record in raw_records:
            srid = record['srid']
            
            if srid not in merged_records:
                merged_records[srid] = record.copy()    # TODO: проверить, что слияние строк отчета происходит корректно
                continue

            for field_name, value in record.items():
                existing_value = merged_records[srid].get(field_name)
                if value and not existing_value:
                    merged_records[srid][field_name] = value

        return list(merged_records.values())


    def _increment(self, stats, id,field_name, val):
        stats[id][field_name] += val


    def _average(self, stats, id, field_name, val):
        stats[id][field_name] = self._get_average(stats, id, field_name, val)


    def _average_positive(self, stats, id, field_name, val):
        if val > 0:
            stats[id][field_name] = self._get_average(stats, id, field_name, val)

    def _get_average(self, stats, id, field_name, val):
        return (stats[id][field_name] + val) / 2