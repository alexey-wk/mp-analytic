from datetime import datetime, timedelta

class DateFormatter:
    @staticmethod
    def get_dash_report_date(report_date: datetime):
        return report_date.strftime('%Y-%m-%d')

    @staticmethod
    def get_dot_report_date(report_date: datetime):
        return report_date.strftime('%d.%m.%Y')

    @staticmethod
    def generate_date_range(from_date_src: str, to_date_src: str) -> list[datetime]:
        from_date = datetime.strptime(from_date_src, '%d.%m.%Y')
        to_date = datetime.strptime(to_date_src, '%d.%m.%Y')
        curr_date = datetime.now()
        
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
