# meerkat
[![build status](https://github.com/msaltnet/meerkat/actions/workflows/python-test.yml/badge.svg)](https://github.com/msaltnet/meerkat/actions/workflows/python-test.yml)
[![license](https://img.shields.io/github/license/msaltnet/meerkat.svg?style=flat-square)](https://github.com/msaltnet/meerkat/blob/main/LICENSE)
![language](https://img.shields.io/github/languages/top/msaltnet/meerkat.svg?style=flat-square&colorB=green)
[![codecov](https://codecov.io/gh/msaltnet/meerkat/branch/main/graph/badge.svg?token=BRCH1W1YSN)](https://codecov.io/gh/msaltnet/meerkat)

monitoring and alarm system

## Usecase
1. 모니터링을 시작/정지 가능하다
2. 모니터링하는 정보를 바탕으로 알림을 생성하는 기능을 켜고 끌수 있다
3. 여러 모니터링을 동시에 사용할 수 있다
4. 모니터링 정보와 알림 정보를 저장 및 보고서 생성

"guide": "0. 조회 - 전체 모니터의 정보 조회",
"guide": "1. 시작 - 모니터의 모니터링 시작",
"guide": "2. 중지 - 모니터의 모니터링 중지",
"guide": "3. 상태 조회 - 모니터들의 Heartbeat 조회",
"guide": "4. 알림 On - 모니터의 알림 기능 활성화",
"guide": "5. 알림 Off - 모니터의 알림 기능 비활성화",
"guide": "6. 모니터링 결과 조회 - 모니터링 결과 조회",

monitor
- do_check, 현재 설정된 모니터링을 수행, 반환 값으로 알림 생성
- get_heartbeat, 현재 모니터링이 제대로 되고 있는 지 확인
- set_alarm, 알림을 켜고 끌 수 있다
- get_analisys, 모니터링 결과를 반환한다

operator
- set_alarm_listener, 모니터의 응답 콜백 등록
- register_monitor, 모니터 등록
- unregister_monitor, 모니터 제거
- start/stop, 모니터링 시작/정지
- get_heartbeat, 모니터링 상태 확인
- excute_checking, 모니터링 수행
- get_monitor_list, 등록된 모니터 목록 조회
- get_analisys, 모니터링 결과 조회
- set_alarm, 모니터링 결과에 따른 알림 설정

controller
- start/stop, 모니터링 시작/정지, 개별 수행
- show_monitor_list, 등록된 모니터 목록 조회
- show_all_monitor_list, 가용한 모든 모니터 목록 조회
- show_status, 상태 조회
- show_result, 결과 조회
