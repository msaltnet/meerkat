"""데이터 소스에서 추출된 데이터를 기반으로 알림을 생성하는 시스템을 운영하는 클래스"""

import threading
from datetime import datetime
import asyncio
from .worker import Worker
from .log_manager import LogManager
from .monitor import Monitor


class Operator:
    """
    데이터 소스에서 추출된 데이터를 기반으로 알림을 생성하는 시스템을 운영하는 클래스
    """

    def __init__(self, on_exception=None):
        self.monitor = {}
        self.alarm_cb = None
        self.is_running = False
        self.interval = 10
        self.worker = Worker("Operator-Worker")
        self.logger = LogManager.get_logger("Operator")
        self.on_exception = on_exception
        self.timer_expired_time = None
        self.timer = None

    def set_alarm_listener(self, alarm_cb):
        """
        모니터의 응답 콜백 등록
        """
        self.alarm_cb = alarm_cb

    def register_monitor(self, monitor):
        """
        모니터를 등록
        """

        # if monitor is not instance of Monitor, do nothing
        if not isinstance(monitor, Monitor):
            return

        # set monitor to self.monitor dictionary
        self.monitor[monitor.NAME] = monitor

    def unregister_monitor(self, monitor):
        """
        모니터를 제거
        """

        # if monitor is not instance of Monitor, do nothing
        if not isinstance(monitor, Monitor):
            return

        # remove monitor from self.monitor dictionary
        if monitor.NAME in self.monitor:
            del self.monitor[monitor.NAME]

    def start(self):
        """
        모니터링 알림 시스템을 시작
        """
        if self.is_running is True:
            return

        self.is_running = True

        self.logger.info("===== Start operating =====")
        self.worker.start()
        self.worker.post_task({"runnable": self.execute_checking})

    def execute_checking(self, worker_task):
        """
        등록된 모니터로 모니터링을 1회 수행
        """

        del worker_task
        self.logger.debug("monitoring START #####################")

        if len(self.monitor) == 0:
            self.logger.debug("No monitor is registered")
            self._start_timer()
            return

        def _on_monitoring_done(future):
            result = future.result()
            if self.alarm_cb is None:
                return
            if result is None or result["ok"] is False:
                self.alarm_cb("Something bad happened during monitoring: {monitor.NAME}")
            else:
                if result["alarm"] is not None and result["alarm"]["message"] is not None:
                    msg = result["alarm"]["message"]
                    alarm_msg = f"{monitor.NAME} - {msg}"
                    self.alarm_cb(alarm_msg)

        loop = asyncio.new_event_loop()
        tasks = []
        for monitor in self.monitor.values():
            task = loop.create_task(monitor.do_check())
            task.add_done_callback(_on_monitoring_done)
            tasks.append(task)
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
        self._start_timer()
        self.logger.debug("monitoring END #####################")

    def _start_timer(self):
        """설정된 간격의 시간이 지난 후 Worker가 모니터링을 수행하도록 타이머 설정"""

        def on_timer_expired():
            self.timer_expired_time = datetime.now()
            self.worker.post_task({"runnable": self.execute_checking})

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
        """
        if len(self.monitor) == 0:
            self.alarm_cb("No monitor is registered")
            return

        if self.is_running is False:
            self.alarm_cb("Operator is not running")
            return

        self.worker.post_task({"runnable": self._get_heartbeat})

    def _get_heartbeat(self, worker_task):
        del worker_task
        self.logger.debug("heartbeat START #####################")

        def _on_check_heartbeat_done(future):
            result = future.result()
            if self.alarm_cb is None:
                return
            if result is None or result["ok"] is False:
                self.alarm_cb("Something bad happened during heartbeat: {monitor.NAME}")
            else:
                msg = result["message"]
                alarm_msg = f"{monitor.NAME} - {msg}"
                self.alarm_cb(alarm_msg)

        loop = asyncio.new_event_loop()
        tasks = []
        for monitor in self.monitor.values():
            task = loop.create_task(monitor.get_heartbeat())
            task.add_done_callback(_on_check_heartbeat_done)
            tasks.append(task)
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
        self.logger.debug("heartbeat END #####################")

    def get_monitor_list(self):
        """
        등록된 모니터의 리스트를 반환

        return : list
        """
        return list(self.monitor.keys())

    def get_analysis_result(self, monitor_name):
        """
        모니터링 결과를 반환

        return: {
            message: 모니터링 결과
            image_file: 모니터링 결과 이미지 파일
        }
        """
        if monitor_name not in self.monitor:
            return None

        return self.monitor[monitor_name].get_analysis_result()
