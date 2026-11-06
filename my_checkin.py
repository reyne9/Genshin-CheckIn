'''
URL: https://sg-hk4e-api.hoyolab.com/event/sol/info
Method: GET
필수 Query Params: act_id ("e202102251931481"), lang ("ko-kr")
필수 Headers:
Cookie: 브라우저에서 가져온 본인의 쿠키 문자열 ("ltoken_v2=...; ltuid_v2=...;")
User-Agent: 크롬 브라우저 모사 (없으면 봇으로 차단될 수 있음)

기대하는 출력 결과: 서버에서 반환하는 JSON의 retcode가 0이고, data 안에 total_sign_day(누적 일수)와 is_sign(오늘 출석 여부: True/False)이 찍히는지 확인.

'''
import os
import requests
from dotenv import load_dotenv  # .env 파일에서 민감 정보를 안전하게 읽어오는 도구

# 1. .env 파일 로드 (공개 Repo 보안 원칙!)
load_dotenv()
my_cookie = os.getenv("HOYOLAB_COOKIES")

# 2. 질문 상세 내용 (Query Params)
url = "https://sg-hk4e-api.hoyolab.com/event/sol/info"
params = {
    "act_id": "e202102251931481",
    "lang": "ko-kr"
}

# 3. 내 신분증 및 명함 (Headers)
headers = {
    "Cookie": my_cookie,
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

# 4. 요청 보내기
res = requests.get(url, params=params, headers=headers)

# 5. 결과 확인
print("상태 코드:", res.status_code)
print("응답 내용:", res.json())

