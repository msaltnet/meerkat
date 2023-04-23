"""전달 받은 데이터에서 필요한 정보를 추출하여 알림을 생성하는 클래스"""

from abc import ABCMeta, abstractmethod


class Reporter(metaclass=ABCMeta):
    """
    전달 받은 데이터에서 필요한 정보를 추출하여 알림을 생성하는 클래스
    """

    @abstractmethod
    def get_report_message(self, data):
        """
        전달 받은 데이터에서 정보를 분석하여 알림을 생성하는 클래스
        return:
            {
                'alarm': True,
                'messege': 'An event has occured.'
            }
        """

    @abstractmethod
    def set_config(self, config):
        """
        리포터에서 변경할 수 있는 설정 값의 설정
        """

    @abstractmethod
    def get_config_info(self) -> str:
        """
        리포터에서 변경할 수 있는 설정 값의 정보
        """
