'''
URL: https://sg-hk4e-api.hoyolab.com/event/sol/info
Method: GET
필수 Query Params: act_id ("e202102251931481"), lang ("ko-kr")
필수 Headers:
Cookie: 브라우저에서 가져온 본인의 쿠키 문자열 ("ltoken_v2=...; ltuid_v2=...;")
User-Agent: 크롬 브라우저 모사 (없으면 봇으로 차단될 수 있음)

기대하는 출력 결과: 서버에서 반환하는 JSON의 retcode가 0이고, data 안에 total_sign_day(누적 일수)와 is_sign(오늘 출석 여부: True/False)이 찍히는지 확인.

'''
import requests

res = requests.get("https://sg-hk4e-api.hoyolab.com/event/sol/info")

print(res.status_code)

print(res.json())

