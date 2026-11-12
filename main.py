import os
import requests
from dotenv import load_dotenv

# 1. 방금 만든 .env 파일에서 내 쿠키 꺼내기
load_dotenv()
my_cookie = os.getenv("HOYOLAB_COOKIES")

# 2. 호요랩 출석 정보 조회 주소와 옵션
url = "https://sg-hk4e-api.hoyolab.com/event/sol/info"
params = {"act_id": "e202102251931481", "lang": "ko-kr"}
headers = {"Cookie": my_cookie, "User-Agent": "Mozilla/5.0"}


# 3. 오늘 출석 도장 찍기 (POST 요청)
sign_url = "https://sg-hk4e-api.hoyolab.com/event/sol/sign"
sign_res = requests.post(sign_url, params={"lang": "ko-kr"}, json={"act_id": "e202102251931481"}, headers=headers)
print(sign_res.json())


# 4. 응답 확인 후 디스코드에 알림 전송
webhook_url = os.getenv("DISCORD_WEBHOOK")

success_message = "hoyolab 원신 출석체크 성공!"
alredy_message = "hoyolab 원신 출석체크 이미 완료!"
failure_message = "hoyolab원신 출석체크 실패!"

result = sign_res.json()
ret_code = result.get("retcode")

if ret_code == 0:
    msg = success_message
elif ret_code == -5003:
    msg = already_message
else:
    msg = f"{failure_message} (사유: {result.get('message')})"
# 디스코드 웹후크로 전송
if webhook_url:
    requests.post(webhook_url, json={"content": msg})
    print("디스코드 알림 전송 완료!")