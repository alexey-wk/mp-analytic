from datetime import datetime, timedelta

class DateFormatter:
    @staticmethod
    def get_dash_report_date(report_date: datetime):
        return report_date.strftime('%Y-%m-%d')

    @staticmethod
    def get_dot_report_date(report_date: datetime):
        return report_date.strftime('%d.%m.%Y')

    @staticmethod
    def generate_date_range(from_date: datetime, to_date: datetime) -> list[datetime]:
        if from_date > to_date:
            raise ValueError("from_date must be before or equal to to_date")
            
        date_list = []
        current_date = from_date
        
        while current_date <= to_date:
            date_list.append(current_date)
            current_date = current_date + timedelta(days=1)
            
        return date_list
