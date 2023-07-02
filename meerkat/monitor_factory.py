from .fake_monitor import FakeMonitor

class MonitorFactory:
    MONITOR_LIST = [FakeMonitor]

    @staticmethod
    def create(code):
        """code에 해당하는 Monitor 객체를 생성하여 반환"""
        for monitor in MonitorFactory.MONITOR_LIST:
            if monitor.CODE == code:
                return monitor()
        return None

    @staticmethod
    def get_name(code):
        """code에 해당하는 Monitor 이름을 반환"""
        for monitor in MonitorFactory.MONITOR_LIST:
            if monitor.CODE == code:
                return monitor.NAME
        return None

    @staticmethod
    def get_all_monitor_info():
        """전체 Monitor 정보를 반환"""
        all_monitor = []
        for monitor in MonitorFactory.MONITOR_LIST:
            all_monitor.append({"name": monitor.NAME, "code": monitor.CODE, "class": monitor})
        return all_monitor
