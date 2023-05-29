# meerkat
[![build status](https://github.com/msaltnet/meerkat/actions/workflows/python-test.yml/badge.svg)](https://github.com/msaltnet/meerkat/actions/workflows/python-test.yml)
[![license](https://img.shields.io/github/license/msaltnet/meerkat.svg?style=flat-square)](https://github.com/msaltnet/meerkat/blob/main/LICENSE)
![language](https://img.shields.io/github/languages/top/msaltnet/meerkat.svg?style=flat-square&colorB=green)
[![codecov](https://codecov.io/gh/msaltnet/meerkat/branch/main/graph/badge.svg?token=BRCH1W1YSN)](https://codecov.io/gh/msaltnet/meerkat)

monitoring and reporting

## Usecase
1. 모니터링을 시작 / 정지 가능하다
2. 모니터링하는 정보를 바탕으로 알림을 생성하는 기능을 켜고 끌수 있다
3. 모니터링 정보와 알리 정보를 저장 및 보고서 생성
4. 모니터/리포터의 변경할 수 있는 설정 정보 조회가 가능하다 (예, 모니터링 날짜)
5. 모니터/리포터의 설정 값을 변경할 수 있다 (에, 모니터링 날짜)

monitor
- get_info, 현재 모니터링하고 있는 정보
- get_heartbeat, 현재 모니터링이 제대로 되고 있는 지
- set_config, 모니터링 설정
- get_config_info, 모니터링 설정 정보

reporter
- get_report_message
- set_config, 모니터링 설정
- get_config_info, 모니터링 설정 정보

analyzer
- put_info
- make_report

operator
- initialize
- start / stop
- get_heartbeat
- excute_monitoring
- get_config_info
- set_config

controller
- 시작 / 정지
- 상태 조회
- 결과 조회
- 설정 변경
- 설정 변경 정보 조회
