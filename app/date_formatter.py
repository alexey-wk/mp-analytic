from datetime import datetime

class DateFormatter:
    @staticmethod
    def get_dash_report_date(report_date: datetime):
        return report_date.strftime('%Y-%m-%d')

    @staticmethod
    def get_dot_report_date(report_date: datetime):
        return report_date.strftime('%d.%m.%Y')
