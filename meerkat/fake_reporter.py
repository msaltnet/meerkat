"""전달 받은 데이터에서 필요한 정보를 추출하여 알림을 생성하는 클래스"""

from .reporter import Reporter
from .log_manager import LogManager


class FakeReporter(Reporter):
    """
    Reporter 클래스의 간단한 구현체
    """

    AVAILABLE_TYPE = ["A", "B", "C"]

    def __init__(self) -> None:
        self.type = "A"
        self.logger = LogManager.get_logger("FakeReporter")

    def get_report_message(self, data):
        """
        전달 받은 데이터에서 정보를 분석하여 알림을 생성하는 클래스
        return:
            {
                'alarm': True,
                'messege': 'An event has occured.'
            }
        """
        result = {"alarm": False, "messege": "No event"}

        try:
            if "event" in data:
                result["alarm"] = True
                result["messege"] = "Data contains events."
        except TypeError:
            self.logger.info(f"Invalid data {data}")
        return result

    def set_config(self, config):
        """
        리포터에서 변경할 수 있는 설정 값의 설정
        """
        try:
            if config["type"] in self.AVAILABLE_TYPE:
                self.type = config["type"]
        except (TypeError, KeyError) as error:
            self.logger.info(f"Invalid config {error}")

    def get_config_info(self) -> str:
        """
        리포터에서 변경할 수 있는 설정 값의 정보
        """
        type_string = ", ".join(self.AVAILABLE_TYPE)

        return f"type을 {type_string} 중 하나로 설정 할 수 있습니다. 예. {{'type': 'A' }}"
