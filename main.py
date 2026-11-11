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
success_message = "✅ 원신 출석 도장 찍기 성공!"
failure_message = "❌ 원신 출석 도장 찍기 실패!"


