import os
import sys
import requests
from dotenv import load_dotenv

# 1. 환경변수(.env 또는 GitHub Secrets)에서 쿠키와 웹후크 주소 꺼내기
load_dotenv()
my_cookie = os.getenv("HOYOLAB_COOKIES")
webhook_url = os.getenv("DISCORD_WEBHOOK")


def send_discord(message: str) -> None:
    """디스코드 웹후크가 설정되어 있으면 알림을 전송합니다."""
    if not webhook_url:
        return
    try:
        requests.post(webhook_url, json={"content": message}, timeout=15)
        print("디스코드 알림 전송 완료!")
    except requests.RequestException as e:
        print(f"디스코드 알림 전송 실패: {e}")


if not my_cookie:
    err_msg = "hoyolab 원신 출석체크 실패! (사유: HOYOLAB_COOKIES 환경변수가 설정되지 않았습니다.)"
    print(err_msg)
    send_discord(err_msg)
    sys.exit(1)

# 2. 호요랩 출석 요청 헤더 설정
headers = {
    "Cookie": my_cookie,
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://act.hoyolab.com/",
    "Origin": "https://act.hoyolab.com",
}

# 3. 오늘 출석 도장 찍기 (POST 요청)
sign_url = "https://sg-hk4e-api.hoyolab.com/event/sol/sign"

try:
    sign_res = requests.post(
        sign_url,
        params={"lang": "ko-kr"},
        json={"act_id": "e202102251931481"},
        headers=headers,
        timeout=15,
    )
    sign_res.raise_for_status()
    result = sign_res.json()
except (requests.RequestException, ValueError) as e:
    err_msg = f"hoyolab 원신 출석체크 실패! (네트워크/응답 오류: {e})"
    print(err_msg)
    send_discord(err_msg)
    sys.exit(1)

print(result)

# 4. 응답 확인 후 디스코드에 알림 전송
success_message = "hoyolab 원신 출석체크 성공!"
already_message = "hoyolab 원신 출석체크 이미 완료!"
failure_message = "hoyolab 원신 출석체크 실패!"

ret_code = result.get("retcode")

if ret_code == 0:
    msg = success_message
    print(msg)
    send_discord(msg)
elif ret_code == -5003:
    msg = already_message
    print(msg)
    send_discord(msg)
else:
    msg = f"{failure_message} (사유: {result.get('message')})"
    print(msg)
    send_discord(msg)
    sys.exit(1)
