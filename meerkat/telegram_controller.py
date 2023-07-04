"""텔래그램 챗봇을 활용한 Meerkat 시스템 운영 사용자 인터페이스 TelegramController 클래스"""

import os
import signal
import time
import threading
import json
from urllib import parse
import requests
from dotenv import load_dotenv
from .log_manager import LogManager
from .worker import Worker
from .operator import Operator
from .monitor_factory import MonitorFactory

load_dotenv()


class TelegramController:
    """Meerkat 시스템 탤래그램 챗봇 컨트롤러"""

    API_HOST = "https://api.telegram.org/"
    TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "telegram_token")
    CHAT_ID = int(os.environ.get("TELEGRAM_CHAT_ID", "123456"))
    POLLING_TIMEOUT = 10
    INTERVAL_SEC = 10
    GUIDE_READY = "명령어를 입력해주세요.\n\n"

    def __init__(self, interval=INTERVAL_SEC):
        self.logger = LogManager.get_logger("TelegramController")
        self.post_worker = Worker("Chatbot-Post-Worker")
        self.post_worker.start()
        # chatbot variable
        self.terminating = False
        self.last_update_id = 0
        self.sub_process = None
        self.sub_process_step = 0
        self.main_keyboard = None
        self.setup_list = []
        self.score_query_list = []
        # meerkat variable
        self.operator = Operator()
        self.operator.set_alarm_listener(self._send_text_message)
        self.operator.interval = interval
        self.monitor = None
        self.command_list = []
        self.all_monitor_codes = []
        self._create_command()

    def _create_command(self):
        """명령어 정보를 생성한다"""
        self.command_list = [
            {
                "guide": "0. 조회 - 전체 모니터의 정보 조회",
                "cmd": ["조회", "0", "0. 모니터 목록 조회"],
                "action": self.show_all_monitor,
            },
            {
                "guide": "1. 시작 - 모니터의 모니터링 시작",
                "cmd": ["시작", "1", "1. 시작"],
                "action": self.start_monitoring,
            },
            {
                "guide": "2. 중지 - 모니터의 모니터링 중지",
                "cmd": ["중지", "2", "2. 중지"],
                "action": self.stop_monitoring,
            },
            {
                "guide": "3. 상태 조회 - 모니터들의 Heartbeat 조회",
                "cmd": ["상태", "3", "3. 상태 조회", "상태 조회"],
                "action": self.check_heartbeat,
            },
            {
                "guide": "4. 알림 On - 모니터의 알림 기능 활성화",
                "cmd": ["4", "알림 On", "4. 알림 On"],
                "action": self.set_alarm_on,
            },
            {
                "guide": "5. 알림 Off - 모니터의 알림 기능 비활성화",
                "cmd": ["5", "알림 Off", "5. 알림 Off"],
                "action": self.set_alarm_off,
            },
            {
                "guide": "6. 모니터링 결과 조회 - 모니터링 결과 조회",
                "cmd": ["6", "모니터링 결과 조회", "6. 모니터링 결과 조회"],
                "action": self.get_analysis_result,
            },
        ]
        main_keyboard = {
            "keyboard": [
                [{"text": "0. 모니터 목록 조회"}],
                [{"text": "1. 시작"}, {"text": "2. 중지"}],
                [{"text": "3. 상태 조회"}, {"text": "4. 알림 On"}, {"text": "5. 알림 Off"}],
                [{"text": "6. 모니터링 결과 조회"}],
            ]
        }
        main_keyboard = json.dumps(main_keyboard)
        self.main_keyboard = parse.quote(main_keyboard)

        all_monitor_info = MonitorFactory.get_all_monitor_info()
        for monitor_info in all_monitor_info:
            self.all_monitor_codes.append(monitor_info["code"])
        self.all_monitor_keyboard = self._make_1_n_keyboard_markup(self.all_monitor_codes)

    @staticmethod
    def _make_1_n_keyboard_markup(item_list):
        markup = {"keyboard": []}
        for item in item_list:
            markup["keyboard"].append([{"text": item}])
        markup = json.dumps(markup)
        return parse.quote(markup)

    def main(self):
        """main 함수"""
        print("##### meerkat telegram controller is started #####")

        signal.signal(signal.SIGINT, self._terminate)
        signal.signal(signal.SIGTERM, self._terminate)

        self._start_get_updates_loop()
        while not self.terminating:
            try:
                time.sleep(0.5)
            except EOFError:
                break

    def _start_get_updates_loop(self):
        """반복적 텔레그램 메세지를 확인하는 쓰레드 관리"""

        def looper():
            self.logger.debug(f"start get updates thread: {threading.get_ident()}")
            while not self.terminating:
                self._handle_message()

        get_updates_thread = threading.Thread(target=looper, name="get updates", daemon=True)
        get_updates_thread.start()

    def _handle_message(self):
        """텔레그램 메세지를 확인해서 명령어를 처리"""
        updates = self._get_updates()
        try:
            if updates is not None and updates["ok"]:
                for result in updates["result"]:
                    self.logger.debug(f'result: {result["message"]["chat"]["id"]} : {self.CHAT_ID}')
                    if result["message"]["chat"]["id"] != self.CHAT_ID:
                        continue
                    if "text" in result["message"]:
                        self._execute_command(result["message"]["text"])
                    self.last_update_id = result["update_id"]
        except (ValueError, KeyError) as err:
            self.logger.error(f"Invalid data from server: {err}")

    def _execute_command(self, command):
        self.logger.debug(f"_execute_command: {command}")
        found = False

        try:
            if self.sub_process is not None:
                self.sub_process(command)
                return
        except TypeError as err:
            self.logger.debug(f"invalid in_progress: {err}")

        for item in self.command_list:
            if command in item["cmd"]:
                found = True
                item["action"](command)

        if not found:
            message = self.GUIDE_READY

            for item in self.command_list:
                message += item["guide"] + "\n"
            self._send_text_message(message, self.main_keyboard)

    def _send_text_message(self, text, keyboard=None):
        encoded_text = parse.quote(text)
        if keyboard is not None:
            url = f"{self.API_HOST}{self.TOKEN}/sendMessage?chat_id={self.CHAT_ID}&text={encoded_text}&reply_markup={keyboard}"
        else:
            url = f"{self.API_HOST}{self.TOKEN}/sendMessage?chat_id={self.CHAT_ID}&text={encoded_text}"

        def send_message(task):
            self._send_http(task["url"])

        self.post_worker.post_task({"runnable": send_message, "url": url})

    def _send_image_message(self, file):
        url = f"{self.API_HOST}{self.TOKEN}/sendPhoto?chat_id={self.CHAT_ID}"

        def send_image(task):
            self._send_http(task["url"], True, task["file"])

        self.post_worker.post_task({"runnable": send_image, "url": url, "file": file})

    def _get_updates(self):
        """getUpdates API로 새로운 메세지를 가져오기"""
        offset = self.last_update_id + 1
        return self._send_http(
            f"{self.API_HOST}{self.TOKEN}/getUpdates?offset={offset}&timeout={self.POLLING_TIMEOUT}"
        )

    def _send_http(self, url, is_post=False, file=None):
        try:
            if is_post:
                if file is not None:
                    with open(file, "rb") as image_file:
                        response = requests.post(url, files={"photo": image_file})
                else:
                    response = requests.post(url)
            else:
                response = requests.get(url)
            response.raise_for_status()
            result = response.json()
        except ValueError as err:
            self.logger.error(f"Invalid data from server: {err}")
            return None
        except requests.exceptions.HTTPError as msg:
            self.logger.error(msg)
            return None
        except requests.exceptions.RequestException as msg:
            self.logger.error(msg)
            return None

        return result

    def _terminate(self, signum=None, frame=None):
        """프로그램 종료"""
        del frame
        self.terminating = True
        self.post_worker.stop()
        if signum is not None:
            print("강제 종료 신호 감지")
        print("프로그램 종료 중.....")
        print("Good Bye~")

    def on_exception(self, msg):
        self._send_text_message(f"시스템 문제가 발생하여 모니터링이 중단되었습니다! {msg}", self.main_keyboard)

    def show_all_monitor(self, command):
        """모든 모니터를 보여줌
        사용 가능한 모든 모니터 목록을 보여줌
        현재 사용중인 모니터는 사용중 표시
        """
        self._send_text_message(self._get_all_monitor(), self.main_keyboard)

    def _get_all_monitor(self):
        all_monitor = MonitorFactory.get_all_monitor_info()
        active_monitor = self.operator.get_monitor_list()

        monitor_info = []
        for monitor in all_monitor:
            if monitor['code'] in active_monitor:
                monitor_info.append(f"{monitor['name']}, {monitor['code']} (사용중)")
            else:
                monitor_info.append(f"{monitor['name']}, {monitor['code']}")
        return "\n".join(monitor_info)

    def start_monitoring(self, command):
        """
        모니터링 시작, sub command로 모니터 코드를 입력받음
        """
        self.sub_process = self.start_monitoring_sub_process
        self.sub_process_step = 1

        message = self._get_all_monitor()
        message += "\n\n모니터링을 시작할 모니터의 코드를 입력하세요."

        self._send_text_message(message, self.all_monitor_keyboard)

    def start_monitoring_sub_process(self, code):
        """
        모니터링 시작 sub process
        """
        self.sub_process = None
        self.sub_process_step = 0

        if code not in self.all_monitor_codes:
            self._send_text_message("잘못된 모니터 코드입니다.")
            return

        if code in self.operator.get_monitor_list():
            self._send_text_message("이미 모니터링 중인 모니터입니다.")
            return

        monitor = MonitorFactory.create(code)
        self.operator.register_monitor(monitor)
        self.operator.start()
        self._send_text_message(f"{monitor.NAME} 모니터링을 시작(등록) 하였습니다.", self.main_keyboard)

    def stop_monitoring(self, command):
        """
        모니터링 중지, sub command로 현재 활성화 되어 있는 모니터 코드를 입력받음
        """
        active_monitor = self.operator.get_monitor_list()
        if len(active_monitor) == 0:
            self._send_text_message("현재 모니터링 중인 모니터가 없습니다.")
            return

        monitor_info = []
        for monitor_code in active_monitor:
            monitor_info.append(f"{MonitorFactory.get_name(monitor_code)}, {monitor_code}")

        self.sub_process = self.stop_monitoring_sub_process
        self.sub_process_step = 1

        message = "\n".join(monitor_info)
        message += "\n\n모니터링을 중지할 모니터의 코드를 입력하세요."
        active_monitor_keyboard = self._make_1_n_keyboard_markup(active_monitor)

        self._send_text_message(message, active_monitor_keyboard)

    def stop_monitoring_sub_process(self, code):
        """
        모니터링 중지 sub process
        """
        self.sub_process = None
        self.sub_process_step = 0

        if code not in self.operator.get_monitor_list():
            self._send_text_message("잘못된 모니터 코드입니다.")
            return

        self.operator.unregister_monitor(code)
        if len(self.operator.get_monitor_list()) == 0:
            self.operator.stop()

        self._send_text_message(f"{MonitorFactory.get_name(code)} 모니터링을 중지(제거) 하였습니다.", self.main_keyboard)

    def set_alarm_on(self, command):
        """
        알람 설정
        """
        active_monitor = self.operator.get_monitor_list()
        if len(active_monitor) == 0:
            self._send_text_message("현재 모니터링 중인 모니터가 없습니다.")
            return

        monitor_info = []
        for monitor_code in active_monitor:
            monitor_info.append(f"{MonitorFactory.get_name(monitor_code)}, {monitor_code}")

        self.sub_process = self.set_alarm_on_sub_process
        self.sub_process_step = 1

        message = "\n".join(monitor_info)
        message += "\n\n알림을 켤 모니터의 코드를 입력하세요."
        active_monitor_keyboard = self._make_1_n_keyboard_markup(active_monitor)

        self._send_text_message(message, active_monitor_keyboard)

    def set_alarm_on_sub_process(self, code):
        """
        알람 설정 sub process
        """
        self.sub_process = None
        self.sub_process_step = 0

        if code not in self.operator.get_monitor_list():
            self._send_text_message("잘못된 모니터 코드입니다.")
            return

        self.operator.set_alarm(code, on_off=True)
        self._send_text_message(f"{MonitorFactory.get_name(code)} 알림을 켰습니다.", self.main_keyboard)

    def set_alarm_off(self, command):
        """
        알람 해제
        """
        active_monitor = self.operator.get_monitor_list()
        if len(active_monitor) == 0:
            self._send_text_message("현재 모니터링 중인 모니터가 없습니다.")
            return

        monitor_info = []
        for monitor_code in active_monitor:
            monitor_info.append(f"{MonitorFactory.get_name(monitor_code)}, {monitor_code}")

        self.sub_process = self.set_alarm_off_sub_process
        self.sub_process_step = 1

        message = "\n".join(monitor_info)
        message += "\n\n알림을 끌 모니터의 코드를 입력하세요."
        active_monitor_keyboard = self._make_1_n_keyboard_markup(active_monitor)

        self._send_text_message(message, active_monitor_keyboard)
    
    def set_alarm_off_sub_process(self, code):
        """
        알람 해제 sub process
        """
        self.sub_process = None
        self.sub_process_step = 0

        if code not in self.operator.get_monitor_list():
            self._send_text_message("잘못된 모니터 코드입니다.")
            return

        self.operator.set_alarm(code, on_off=False)
        self._send_text_message(f"{MonitorFactory.get_name(code)} 알림을 껐습니다.", self.main_keyboard)

    def check_heartbeat(self, command):
        """
        heartbeat 확인
        """
        self.operator.get_heartbeat()
        self._send_text_message("heartbeat 확인이 시작되었습니다.", self.main_keyboard)

    def get_analysis_result(self, command):
        """
        분석 결과 확인
        """
        active_monitor = self.operator.get_monitor_list()
        if len(active_monitor) == 0:
            self._send_text_message("현재 모니터링 중인 모니터가 없습니다.")
            return

        monitor_info = []
        for monitor_code in active_monitor:
            monitor_info.append(f"{MonitorFactory.get_name(monitor_code)}, {monitor_code}")

        self.sub_process = self.get_analysis_result_sub_process
        self.sub_process_step = 1

        message = "\n".join(monitor_info)
        message += "\n\n모니터링 결과를 확인 할 모니터의 코드를 입력하세요."
        active_monitor_keyboard = self._make_1_n_keyboard_markup(active_monitor)

        self._send_text_message(message, active_monitor_keyboard)

    def get_analysis_result_sub_process(self, code):
        """
        분석 결과 확인 sub process
        """
        self.sub_process = None
        self.sub_process_step = 0

        if code not in self.operator.get_monitor_list():
            self._send_text_message("잘못된 모니터 코드입니다.")
            return

        result = self.operator.get_analysis_result(code)
        if "message" in result:
            self._send_text_message(result["message"], self.main_keyboard)
            return