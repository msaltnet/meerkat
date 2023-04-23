"""데이터 소스에서 추출된 데이터를 기반으로 알림을 생성하는 시스템을 운영하는 클래스"""


class Operator:
    """
    데이터 소스에서 추출된 데이터를 기반으로 알림을 생성하는 시스템을 운영하는 클래스
    """

    def __init__(self):
        self.monitor = None
        self.reporter = None
        self.alarm_handler = None
        self.analyzer = None

    def initialize(self, monitor, reporter, alarm_handler, analyzer=None):
        """
        monitor와 reporter를 입력받아서 시스템을 초기화
        """
        self.monitor = monitor
        self.reporter = reporter
        self.alarm_handler = alarm_handler
        if analyzer is not None:
            self.analyzer = analyzer

    def start(self):
        """
        모니터링 알림 시스템을 시작
        """

    def stop(self):
        """
        모니터링 알림 시스템을 중지
        """

    def get_heartbeat(self):
        """
        모니터링이 정상적으로 진행되고 있는지 확인
        """

    def check(self):
        """
        모니터링 알림을 1회 실시
        """

    def get_config_info(self, monitor_config=True):
        """
        모니터와 리포터의 변경할 수 있는 설정 값의 설정 정보를 조회
        """

    def set_config(self, config, monitor_config=True):
        """
        모니터와 리포터의 변경할 수 있는 설정 값의 설정
        """
