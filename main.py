"""
HoYoLAB Genshin Impact Daily Check-in Automation
================================================
원신 호요랩 웹 일일 출석체크 자동화 스크립트.
민감 정보(쿠키, 토큰 등)는 환경변수(.env 및 GitHub Secrets)로 주입받습니다.
"""

import os
import sys
import json
import logging
from typing import Dict, Any, Optional
import requests
from dotenv import load_dotenv

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("HoYoLAB-CheckIn")

# 원신 글로벌 출석체크 상수
ACT_ID = "e202102251931481"
API_BASE_URL = "https://sg-hk4e-api.hoyolab.com/event/sol"
INFO_URL = f"{API_BASE_URL}/info"
SIGN_URL = f"{API_BASE_URL}/sign"
HOME_URL = f"{API_BASE_URL}/home"


class HoYoLABCheckIn:
    def __init__(self, cookies: str, lang: str = "ko-kr", discord_webhook: Optional[str] = None):
        self.cookies = cookies.strip()
        self.lang = lang
        self.discord_webhook = discord_webhook.strip() if discord_webhook else None
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Referer": "https://act.hoyolab.com/",
            "Origin": "https://act.hoyolab.com",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cookie": self.cookies,
        })

    def get_info(self) -> Dict[str, Any]:
        """현재 출석 상태 및 누적 출석 일수 조회"""
        params = {"act_id": ACT_ID, "lang": self.lang}
        response = self.session.get(INFO_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_reward_list(self) -> list:
        """이달의 출석 보상 목록 조회"""
        params = {"act_id": ACT_ID, "lang": self.lang}
        response = self.session.get(HOME_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("retcode") == 0:
            return data.get("data", {}).get("awards", [])
        return []

    def perform_checkin(self) -> Dict[str, Any]:
        """출석 체크 수행 요청"""
        params = {"lang": self.lang}
        payload = {"act_id": ACT_ID}
        response = self.session.post(SIGN_URL, params=params, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()

    def send_discord_webhook(self, title: str, description: str, is_success: bool = True):
        """Discord Webhook 알림 전송 (선택 사항)"""
        if not self.discord_webhook:
            return

        color = 0x2ECC71 if is_success else 0xE74C3C  # 초록색 / 빨간색
        payload = {
            "embeds": [
                {
                    "title": title,
                    "description": description,
                    "color": color,
                    "footer": {"text": "HoYoLAB Auto Check-in Bot"}
                }
            ]
        }
        try:
            res = requests.post(self.discord_webhook, json=payload, timeout=5)
            if res.status_code == 204:
                logger.info("Discord 알림 전송 완료.")
            else:
                logger.warning(f"Discord 알림 전송 실패: HTTP {res.status_code}")
        except Exception as e:
            logger.error(f"Discord 알림 전송 중 예외 발생: {e}")

    def run(self) -> bool:
        """전체 출석체크 프로세스 실행"""
        logger.info("=== 원신 HoYoLAB 일일 출석체크 자동화 시작 ===")

        # 1. 출석 정보 조회
        try:
            info_res = self.get_info()
        except requests.RequestException as e:
            msg = f"네트워크 요청 실패 (info): {e}"
            logger.error(msg)
            self.send_discord_webhook("출석체크 실패 (네트워크 오류)", msg, is_success=False)
            return False

        retcode = info_res.get("retcode")
        if retcode != 0:
            msg = f"인증 실패: {info_res.get('message')} (retcode: {retcode})\n쿠키가 만료되었거나 올바르지 않습니다."
            logger.error(msg)
            self.send_discord_webhook("출석체크 인증 실패", msg, is_success=False)
            return False

        info_data = info_res.get("data", {})
        is_sign = info_data.get("is_sign", False)
        total_days = info_data.get("total_sign_day", 0)

        # 2. 이미 출석한 경우
        if is_sign:
            result_msg = f"오늘 이미 출석체크를 완료했습니다! (이번 달 누적 출석: {total_days}일)"
            logger.info(result_msg)
            self.send_discord_webhook("호요랩 출석체크 알림", result_msg, is_success=True)
            return True

        # 3. 출석체크 시도
        try:
            sign_res = self.perform_checkin()
        except requests.RequestException as e:
            msg = f"출석 요청 중 네트워크 오류: {e}"
            logger.error(msg)
            self.send_discord_webhook("출석체크 요청 실패", msg, is_success=False)
            return False

        sign_retcode = sign_res.get("retcode")
        sign_message = sign_res.get("message", "")

        # 0: 성공, -5003: 이미 출석 완료
        if sign_retcode in (0, -5003):
            # 최신 보상 정보 조회
            rewards = self.get_reward_list()
            today_reward = "알 수 없음"
            next_day_index = total_days  # 0-indexed로 다음 보상
            if 0 <= next_day_index < len(rewards):
                award = rewards[next_day_index]
                today_reward = f"{award.get('name')} x{award.get('cnt')}"

            final_days = total_days + (1 if sign_retcode == 0 else 0)
            status_text = "출석체크 성공!" if sign_retcode == 0 else "이미 출석 완료됨"
            msg = (
                f"✅ **{status_text}**\n"
                f"• 누적 출석일: {final_days}일차\n"
                f"• 오늘의 보상: {today_reward}"
            )
            logger.info(f"{status_text} - 누적: {final_days}일차, 보상: {today_reward}")
            self.send_discord_webhook("호요랩 원신 출석체크 결과", msg, is_success=True)
            return True
        else:
            msg = f"출석체크 실패: {sign_message} (retcode: {sign_retcode})"
            logger.error(msg)
            self.send_discord_webhook("호요랩 출석체크 실패", msg, is_success=False)
            return False


def main():
    # .env 파일이 존재하는 경우 환경변수 로드
    load_dotenv()

    cookies = os.getenv("HOYOLAB_COOKIES")
    lang = os.getenv("HOYOLAB_LANG", "ko-kr")
    discord_webhook = os.getenv("DISCORD_WEBHOOK_URL")

    if not cookies or cookies.strip() == "" or "your_ltoken_v2_here" in cookies:
        logger.error(
            "오류: HOYOLAB_COOKIES 환경변수가 설정되지 않았거나 예시 값입니다.\n"
            ".env 파일을 생성하거나 환경변수를 설정해주세요. (.env.example 참고)"
        )
        sys.exit(1)

    bot = HoYoLABCheckIn(cookies=cookies, lang=lang, discord_webhook=discord_webhook)
    success = bot.run()
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
