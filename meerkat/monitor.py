"""관심있는 데이터에서 필요한 정보를 모니터링 하는 클래스"""

from abc import ABCMeta, abstractmethod


class Monitor(metaclass=ABCMeta):
    """
    관심있는 데이터에서 필요한 정보를 모니터링 하는 클래스
    """

    @abstractmethod
    def get_monitor_info(self) -> str:
        """
        현재 모니터의 정보 텍스트로 전달
        """

    @abstractmethod
    def get_data(self) -> str:
        """
        현재 모니터링하고 있는 대상 데이터를 텍스트로 전달
        """

    @abstractmethod
    def get_heartbeat(self) -> dict:
        """
        현재 모니터링이 제대로 되고 있는 지 확인해서 결과 전달

        Returns: 확인 결과
        {
            "ok": True
            "message": 확인 결과 문자
        }
        """

    @abstractmethod
    def set_config(self, config):
        """
        모니터링에서 변경할 수 있는 설정 값의 설정
        """

    @abstractmethod
    def get_config_info(self) -> str:
        """
        모니터링에서 변경할 수 있는 설정 값의 정보
        """
