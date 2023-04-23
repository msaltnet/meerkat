"""Monitor 클래스의 간단한 구현체"""

from .monitor import Monitor
from .log_manager import LogManager


class FakeMonitor(Monitor):
    """
    Monitor 클래스의 간단한 구현체
    """

    AVAILABLE_TYPE = ["A", "B", "C"]

    def __init__(self) -> None:
        self.idx = 0
        self.type = "A"
        self.logger = LogManager.get_logger("FakeMonitor")

    def get_monitor_info(self) -> str:
        """
        현재 모니터링하고 있는 정보를 텍스트로 전달
        """
        return "Monitor를 간단하게 구현한 Fake 객체입니다."

    def get_data(self) -> str:
        """
        현재 모니터링하고 있는 대상 데이터를 텍스트로 전달
        """
        self.idx += 1
        return f"{self.idx}번째 데이터 입니다"

    def get_heartbeat(self) -> str:
        """
        현재 모니터링이 제대로 되고 있는 지 확인해서 결과 전달

        Returns: 확인 결과
        {
            "ok": True
            "message": 확인 결과 문자
        }
        """
        return {"ok": True, "message": "정상적으로 모니터링 되고 있습니다"}

    def set_config(self, config):
        """
        모니터에서 변경할 수 있는 설정 값의 설정
        """
        try:
            if config["type"] in self.AVAILABLE_TYPE:
                self.type = config["type"]
        except (TypeError, KeyError) as error:
            self.logger.info(f"Invalid config {error}")

    def get_config_info(self):
        """
        모니터에서 변경할 수 있는 설정 값의 정보
        """
        type_string = ", ".join(self.AVAILABLE_TYPE)

        return f"type을 {type_string} 중 하나로 설정 할 수 있습니다. 예. {{'type': 'A' }}"
