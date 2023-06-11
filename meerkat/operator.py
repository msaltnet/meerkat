"""데이터 소스에서 추출된 데이터를 기반으로 알림을 생성하는 시스템을 운영하는 클래스"""

import threading
from datetime import datetime
from .worker import Worker
from .log_manager import LogManager


class Operator:
    """
    데이터 소스에서 추출된 데이터를 기반으로 알림을 생성하는 시스템을 운영하는 클래스
    """

    def __init__(self, on_exception=None):
        self.monitor = None
        self.reporter = None
        self.alarm_handler = None
        self.analyzer = None
        self.is_running = False
        self.interval = 10
        self.worker = Worker("Operator-Worker")
        self.logger = LogManager.get_logger("Operator")
        self.on_exception = on_exception
        self.timer_expired_time = None
        self.timer = None

    def initialize(self, monitor, reporter, alarm_handler, analyzer):
        """
        monitor와 reporter를 입력받아서 시스템을 초기화
        """
        self.monitor = monitor
        self.reporter = reporter
        self.alarm_handler = alarm_handler
        self.analyzer = analyzer

    def start(self):
        """
        모니터링 알림 시스템을 시작
        """
        if self.monitor is None or self.reporter is None:
            return

        if self.is_running is True:
            return

        self.is_running = True

        self.logger.info("===== Start operating =====")
        self.worker.start()
        self.worker.post_task({"runnable": self._excute_monitoring})

    def _excute_monitoring(self, task):
        """
        모니터링과 알림을 1회 실시
        """

        del task
        self.logger.debug("monitoring is started #####################")

        try:
            target_data = self.monitor.get_info()
            self.analyzer.put_info(target_data)

            result = self.reporter.get_report_message(target_data)
            if result is not None:
                self.analyzer.put_info(result)
                self.alarm_handler(result)

        except Exception as exc:
            if self.on_exception is not None:
                self.on_exception("Something bad happened during trading")
            raise RuntimeError("Something bad happened during trading") from exc
        self._start_timer()

    def _start_timer(self):
        """설정된 간격의 시간이 지난 후 Worker가 모니터링을 수행하도록 타이머 설정"""

        def on_timer_expired():
            self.timer_expired_time = datetime.now()
            self.worker.post_task({"runnable": self._excute_monitoring})

        adjusted_interval = self.interval
        if self.interval > 1 and self.timer_expired_time is not None:
            time_delta = datetime.now() - self.timer_expired_time
            adjusted_interval = self.interval - round(time_delta.total_seconds(), 1)

        self.timer = threading.Timer(adjusted_interval, on_timer_expired)
        self.timer.start()

    def stop(self):
        """
        모니터링 알림 시스템을 중지
        """
        self.logger.info("===== Stop operating =====")
        if self.timer is not None:
            self.timer.cancel()

        def on_terminated():
            self.is_running = False

        self.worker.register_on_terminated(on_terminated)
        self.worker.stop()

    def get_heartbeat(self):
        """
        모니터링이 정상적으로 진행되고 있는지 확인

        return : True or False
        """
        if self.monitor is None:
            return False

        return self.monitor.get_heartbeat()

    def get_config_info(self, monitor_config=True):
        """
        모니터와 리포터의 변경할 수 있는 설정 값의 설정 정보를 조회
        monitor_config이 True이면 모니터의 설정 정보를 조회
        monitor_config이 False이면 리포터의 설정 정보를 조회
        """

    def set_config(self, config, monitor_config=True):
        """
        모니터와 리포터의 변경할 수 있는 설정 값의 설정
        monitor_config이 True이면 모니터의 설정을 변경
        monitor_config이 False이면 리포터의 설정을 변경
        """
