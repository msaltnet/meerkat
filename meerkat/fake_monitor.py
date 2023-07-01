"""Monitor 클래스의 간단한 구현체"""

from .monitor import Monitor
from .log_manager import LogManager


class FakeMonitor(Monitor):
    """
    Monitor 클래스의 간단한 구현체
    """

    AVAILABLE_TYPE = ["A", "B", "C"]

    def __init__(self) -> None:
        self.is_running = False
        self.alarm_on = False
        self.logger = LogManager.get_logger("FakeMonitor")

    async def do_check(self) -> dict:
        """
        현재 설정된 모니터링을 수행, 반환 값으로 알림 생성
        return: {
            "ok": True,
            "alarm": {
                "message": 알림 메시지
            }
        }
        """
        response = {"ok": True}
        if self.alarm_on:
            response["alarm"] = {"message": "Fake Monitor Alarm"}

        return response

    async def get_heartbeat(self) -> str:
        """
        현재 모니터링이 제대로 되고 있는 지 확인해서 결과 전달

        Returns: 확인 결과
        {
            "ok": True
            "message": 확인 결과 문자
        }
        """
        response = {"ok": True}
        if self.alarm_on:
            response["message"] = "정상적으로 모니터링 되고 있습니다. 알림이 켜져 있습니다"
        else:
            response["ok"] = False
            response["message"] = "정상적으로 모니터링 되고 있습니다. 알림이 꺼져 있습니다"
        return response

    def set_alarm(self, on):
        """
        알림을 켜고 끌 수 있다
        on: True, False on/off
        """
        if on:
            self.alarm_on = True
            self.logger.info("알림이 켜졌습니다")
        else:
            self.alarm_on = False
            self.logger.info("알림이 꺼졌습니다")

    def get_analysis(self) -> dict:
        """
        모니터링 결과를 반환한다
        return: {
            message: 모니터링 결과
            image_file: 모니터링 결과 이미지 파일
        }
        """
        return {"message": "Fake Monitor Analysis", "image_file": None}
