# 원신체크인 (Genshin-CheckIn)

스마트폰에 호요랩 설치하기 싫지만, 매일 웹에서 호요랩 출석체크하기 귀찮은 당신!  
당신을 위한 원신 웹 일일 출석체크 자동화 앱입니다.

---

## 주요 기능

- **간편한 웹 출석체크**: 게임을 켜거나 스마트폰 앱을 설치하지 않고 호요랩(HoYoLAB) 웹 출석을 자동으로 처리합니다.
- **원하는 시간마다 24/7 자동 실행**: GitHub Actions 스케줄러(`cron`)를 이용해 내 컴퓨터가 꺼져 있어도 매일 원하는 시각 또는 원하는 시간 간격마다 자동으로 출석체크를 실행합니다.
- **디스코드(Discord) 실시간 알림**: 출석 성공 여부, 이미 출석 완료 상태, 실패 사유를 개인 디스코드 채널로 실시간 알림 전송합니다.
- **안전한 인증 분리**: 개인 로그인 쿠키(`ltoken_v2`, `ltuid_v2`)와 디스코드 웹후크 URL은 코드에 직접 적지 않고 GitHub Secrets로 분리하여 안전하게 관리합니다.

---

## GitHub Actions & CI란?

이 프로젝트는 사용자의 PC가 아닌 **GitHub의 클라우드 서버** 위에서 자동으로 실행되도록 설계되었습니다.

- **CI (Continuous Integration, 지속적 통합)**
  - 원래 소프트웨어 개발에서 코드가 변경될 때마다 자동으로 빌드·테스트·검증을 수행하여 안정성을 유지하는 개발 방식입니다.
  - 이 프로젝트에서는 CI 파이프라인 인프라를 활용해, 매일 정해진 시간에 깔끔한 새 실행 환경(가상 머신)을 자동으로 띄우고 의존성을 설치한 뒤 출석체크 스크립트를 실행·검증합니다.
- **GitHub Actions**
  - GitHub에서 기본으로 제공하는 **CI/CD 자동화 플랫폼**입니다.
  - 별도의 개인 서버나 클라우드 비용 없이도, [`.github/workflows/checkin.yml`](.github/workflows/checkin.yml)에 정의된 규칙에 따라 다음과 같은 과정이 매일 자동으로 수행됩니다:
    1. 설정된 `cron` 시간(또는 수동 실행 버튼 클릭)에 맞춰 GitHub 클라우드 가상 컴퓨터(`ubuntu-latest`)가 켜집니다.
    2. 저장소 코드를 내려받고(`checkout`) Python 환경과 `requirements.txt` 패키지를 설치합니다.
    3. 암호화된 **GitHub Secrets**에서 쿠키와 웹후크 주소를 안전하게 불러와 `main.py`를 실행합니다.
    4. 출석 결과를 디스코드로 전송한 뒤 가상 컴퓨터를 종료합니다.

---

## 사전 준비 (쿠키 & 디스코드 웹후크)

### 1. 호요랩(HoYoLAB) 쿠키 정보 복사

1. PC 웹 브라우저(Chrome, Whale, Edge 등)에서 [호요랩 원신 출석체크 페이지](https://act.hoyolab.com/ys/event/signin-sea-v3/index.html?act_id=e202102251931481&hyl_auth_required=true&hyl_presentation_style=fullscreen&lang=ko-kr)에 접속해 로그인합니다.
2. 개발자 도구를 엽니다.
   - **Mac**: `Command (⌘) + Option (⌥) + I` (또는 우클릭 $\rightarrow$ `검사`)
   - **Windows**: `F12`
3. 상단 메뉴에서 **`Application` (애플리케이션)** 탭 $\rightarrow$ 왼쪽 **`Cookies` (쿠키)** $\rightarrow$ `https://act.hoyolab.com` (또는 `https://www.hoyolab.com`)을 클릭합니다.
4. 상단 `Filter (필터)` 창에 `lt`를 입력하여 아래 두 가지 값을 찾습니다 (**도메인이 `.hoyolab.com`인 항목**을 선택하세요):
   - `ltoken_v2`: `v2_...`로 시작하는 인증 토큰 값
   - `ltuid_v2`: 숫자로 된 호요랩 통행증 ID

### 2. 디스코드(Discord) 웹후크 URL 생성 (선택 사항)

1. 디스코드에서 알림을 받을 개인 서버 채널의 **채널 편집(⚙️ 톱니바퀴)**으로 이동합니다.
2. **연동(Integrations)** $\rightarrow$ **웹후크(Webhooks)**를 클릭합니다.
3. **새 웹후크 만들기**를 누르고 **웹후크 URL 복사**를 클릭합니다.  
   (`https://discord.com/api/webhooks/...` 형식)

---

## 설치 및 자동 실행 방법 (GitHub Actions)

컴퓨터를 켜두지 않아도 GitHub 클라우드 서버에서 지정한 시간마다 자동으로 실행됩니다.

### 1. 저장소 Fork
우측 상단의 **`Fork`** 버튼을 눌러 이 저장소를 본인의 GitHub 계정으로 복제합니다.

### 2. GitHub Secrets에 인증 정보 등록
복제한 본인 저장소의 **`Settings`** $\rightarrow$ **`Secrets and variables`** $\rightarrow$ **`Actions`** $\rightarrow$ **`New repository secret`** 버튼을 눌러 아래 항목을 추가합니다.

| Name (이름) | Value (값) | 필수 여부 |
| :--- | :--- | :---: |
| `HOYOLAB_COOKIES` | `ltoken_v2=복사한_값; ltuid_v2=복사한_값;` | 필수 |
| `DISCORD_WEBHOOK` | 복사한 디스코드 웹후크 URL | 선택 |

> ⚠️ **주의**: 개인 로그인 쿠키와 웹후크 주소는 절대 코드나 공개 파일에 직접 적지 말고 반드시 **GitHub Secrets**에만 등록하세요.

### 3. 원하는 실행 시간/주기 설정 (`cron` 수정)
[`.github/workflows/checkin.yml`](.github/workflows/checkin.yml) 파일의 `cron` 값을 수정하여 실행 시간이나 주기를 바꿀 수 있습니다.

```yaml
on:
  schedule:
    - cron: '0 21 * * *' # 기본값: 매일 한국 시간(KST) 오전 06:00
```

> ⏰ **시간 계산 주의사항 (UTC vs 한국 시간 KST)**  
> GitHub Actions는 **세계 표준시(UTC)**를 사용하므로, 원하는 한국 시간에서 **9시간을 빼서** 입력해야 합니다. (`KST - 9시간 = UTC`)

| 원하는 한국 시간 / 주기 | 입력할 `cron` 표현식 | 설명 |
| :--- | :--- | :--- |
| 매일 오전 06:00 (KST) | `'0 21 * * *'` | 기본값 (전날 UTC 21:00) |
| 매일 오전 09:00 (KST) | `'0 0 * * *'` | 한국 시간 오전 9시 |
| 매일 오후 12:00 (KST) | `'0 3 * * *'` | 한국 시간 정오 |
| 매일 밤 00:00 (KST) | `'0 15 * * *'` | 한국 시간 자정 |
| 6시간마다 실행 | `'0 */6 * * *'` | 매 6시간 정각마다 실행 |
| 12시간마다 실행 | `'0 */12 * * *'` | 매 12시간 정각마다 실행 |

> 💡 **참고**: GitHub Actions 무료 플랜에서는 서버 트래픽에 따라 예약 실행이 설정한 시각보다 수 분 정도 지연되어 시작될 수 있습니다.

### 4. Actions 활성화 및 수동 실행 테스트
1. 본인 GitHub 저장소 상단의 **`Actions`** 탭으로 이동합니다.
2. 워크플로우 실행 허용 안내가 뜨면 활성화 버튼을 누릅니다.
3. 왼쪽 목록에서 **`Genshin HoYoLAB Auto Check-in`**을 선택한 뒤, **`Run workflow`** 버튼을 눌러 즉시 실행이 잘 되는지 테스트합니다.

---

## 기술 스택

- **Language**: Python 3
- **Libraries**:
  - `requests`: 호요랩 출석체크 REST API 통신 (`POST`) 및 디스코드 웹후크 전송
  - `python-dotenv`: 환경변수 로드 및 설정 분리
- **Automation & CI**:
  - `GitHub Actions`: CI 기반 클라우드 `cron` 스케줄 무인 자동 실행
- **Notification**:
  - `Discord Webhook`: 출석체크 결과 실시간 메시지 전송

---

## 라이선스

MIT License
