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

# 3. 서버에 요청 보내고 결과 출력하기
res = requests.get(url, params=params, headers=headers)
print(res.json())