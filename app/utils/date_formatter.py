from datetime import datetime, date, timedelta


DOT_DATE_FORMAT = '%d.%m.%Y'
DASH_DATE_FORMAT = '%Y-%m-%d'


class DateFormatter:
    @staticmethod
    def parse_dot_date(date_str: str):
        return datetime.strptime(date_str, DOT_DATE_FORMAT).date()


    @staticmethod
    def get_dash_date(report_date: datetime):
        return report_date.strftime(DASH_DATE_FORMAT)


    @staticmethod
    def get_dot_date(report_date: datetime):
        return report_date.strftime(DOT_DATE_FORMAT)
    
    @staticmethod
    def get_date_from_iso(report_date: datetime):
        return datetime.fromisoformat(report_date).replace(tzinfo=None).date()


    @staticmethod
    def add_days(report_date: datetime, days: int):
        return report_date + timedelta(days=days)


    @staticmethod
    def generate_date_range(from_date: date, to_date: date) -> list[date]:
        curr_date = datetime.now().date()
        
        if to_date > curr_date:
            to_date = curr_date
        
        if from_date > curr_date:
            to_date = curr_date

        date_list = []
        current_date = from_date
        
        while current_date <= to_date:
            date_list.append(current_date)
            current_date = current_date + timedelta(days=1)
            
        return date_list
