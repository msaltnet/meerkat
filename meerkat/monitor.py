"""관심있는 데이터소스에서 필요한 데이터를 추출하여 알람 정보를 제공하는 클래스"""

from abc import ABCMeta, abstractmethod


class Monitor(metaclass=ABCMeta):
    """
    관심있는 데이터소스에서 필요한 데이터를 추출하여 알람 정보를 제공하는 클래스
    """

    NAME = "Unique Monitor Name"
    CODE = "FMC"

    @abstractmethod
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

    @abstractmethod
    async def get_heartbeat(self) -> dict:
        """
        현재 모니터링이 제대로 되고 있는 지 확인해서 결과 전달

        Returns: 확인 결과
        {
            "ok": True
            "message": 확인 결과 문자
        }
        """

    @abstractmethod
    def set_alarm(self, on):
        """
        알림을 켜고 끌 수 있다
        on: True, False on/off
        """

    @abstractmethod
    def get_analysis(self) -> dict:
        """
        모니터링 결과를 반환한다
        return: {
            message: 모니터링 결과
            image_file: 모니터링 결과 이미지 파일
        }
        """
