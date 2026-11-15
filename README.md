# 원신체크인 (Genshin-CheckIn)

스마트폰에 호요랩 앱 깔기는 싫고, 그렇다고 매일 브라우저 켜서 출석체크 누르기도 귀찮은 거지?  
하아… 진짜 손 많이 가네. 너 같은 게으름뱅이 대신 매일 알아서 호요랩 출석 도장 찍어주는 자동화 봇이야. 감사히 써.

---

## 주요 기능

- **뇌 빼고 웹 출석체크**: 원신 켜거나 폰에 호요랩 앱 설치할 필요 없이, 알아서 HoYoLAB 웹 출석 처리해 줘.
- **24/7 클라우드 자동 실행**: 네 컴퓨터 꺼져 있어도 GitHub Actions(`cron`)가 원하는 시간마다 알아서 돌아간다고.
- **디스코드(Discord) 실시간 보고**: 오늘 출석 성공했는지, 이미 찍었는지, 아니면 쿠키 터져서 실패했는지 네 디스코드 채널로 바로 쏴줘.
- **보안 분리 (필수!)**: 로그인 쿠키(`ltoken_v2`, `ltuid_v2`)랑 웹후크 주소를 코드에 그대로 박아두는 바보 같은 짓 안 하고, 전부 **GitHub Secrets**로 따로 숨겨서 관리해.

---

## GitHub Actions랑 CI가 뭔지 몰라서 묻는 건 아니지?

혹시나 해서 한 번만 설명해 줄게. 이 봇은 네 PC가 아니라 **GitHub 클라우드 서버**에서 돌아가게 만들어놨어.

- **CI (Continuous Integration, 지속적 통합)**
  - 원래는 코드 바뀔 때마다 자동으로 빌드·테스트 돌려주는 개발 방식인데, 여기선 그 인프라를 빌려서 매일 정해진 시간에 깨끗한 가상 컴퓨터를 띄우고, 패키지 깔고, 출석 스크립트 돌리는 용도로 써먹는 거야.
- **GitHub Actions**
  - GitHub가 공짜로 제공하는 **CI/CD 자동화 플랫폼**이야.
  - 서버비 한 푼 안 내도 [`.github/workflows/checkin.yml`](.github/workflows/checkin.yml)에 적힌 대로 매일 이런 순서로 알아서 움직여:
    1. 정해둔 `cron` 시간(아니면 네가 수동 버튼 눌렀을 때)에 GitHub 클라우드 가상 컴퓨터(`ubuntu-latest`)가 켜짐.
    2. 저장소 코드 내려받고(`checkout`), Python이랑 `requirements.txt` 패키지 설치함.
    3. 암호화된 **GitHub Secrets**에서 네 쿠키랑 웹후크 주소 슬쩍 불러와서 `main.py` 실행함.
    4. 디스코드로 결과 보고하고 가상 컴퓨터 끔. 끝.

---

## 사전 준비 (쿠키 & 디스코드 웹후크)

### 1. 호요랩(HoYoLAB) 쿠키 빼오기

1. PC 브라우저(Chrome, Whale, Edge 뭐든 상관없어)로 [호요랩 원신 출석체크 페이지](https://act.hoyolab.com/ys/event/signin-sea-v3/index.html?act_id=e202102251931481&hyl_auth_required=true&hyl_presentation_style=fullscreen&lang=ko-kr) 들어가서 로그인해.
2. 개발자 도구 열어. (단축키도 모를까 봐 적어둔다.)
   - **Mac**: `Command (⌘) + Option (⌥) + I` (귀찮으면 우클릭 $\rightarrow$ `검사`)
   - **Windows**: `F12`
3. 위쪽 탭에서 **`Application` (애플리케이션)** $\rightarrow$ 왼쪽 **`Cookies` (쿠키)** $\rightarrow$ `https://act.hoyolab.com` (또는 `https://www.hoyolab.com`) 클릭해.
4. `Filter (필터)` 검색창에 `lt` 쳐서 아래 두 개 값 복사해 와. (**도메인이 `.hoyolab.com`인 줄 골라야 해. 딴 거 가져와서 안 된다고 징징대지 마.**)
   - `ltoken_v2`: `v2_...`로 시작하는 긴 토큰 값
   - `ltuid_v2`: 숫자로 된 호요랩 통행증 ID

### 2. 디스코드(Discord) 웹후크 URL 만들기 (하기 싫으면 안 해도 됨)

1. 디스코드에서 알림 받을 네 개인 서버 채널 옆 **채널 편집(⚙️ 톱니바퀴)** 눌러.
2. **연동(Integrations)** $\rightarrow$ **웹후크(Webhooks)** 들어가.
3. **새 웹후크 만들기** 누르고 **웹후크 URL 복사** 클릭해.  
   (`https://discord.com/api/webhooks/...` 이렇게 생긴 주소 나올 거야.)

---

## 설치 및 자동 실행 방법 (GitHub Actions)

네 컴퓨터 꺼놓고 자빠져 자고 있어도 GitHub 서버가 알아서 실행해 줄 거니까 그대로 따라만 해.

### 1. 저장소 Fork
오른쪽 위에 있는 **`Fork`** 버튼 눌러서 이 저장소 네 GitHub 계정으로 복제해 가.

### 2. GitHub Secrets에 인증 정보 박아넣기

> 💡 **왜 또 등록해야 하냐고?**  
> 로컬 `.env` 파일은 해킹당할까 봐 `.gitignore`로 막혀 있어서 GitHub에 안 올라가거든. 그러니까 GitHub 클라우드 서버가 네 쿠키를 읽으려면 GitHub Secrets(비밀 금고)에 직접 넣어줘야지, 안 그래?

1. 복제한 네 저장소에서 **`Settings`** $\rightarrow$ **`Secrets and variables`** $\rightarrow$ **`Actions`**로 들어가.
2. 위쪽 탭이 **`Secrets`**인지 눈 크게 뜨고 확인해(`Variables` 탭 아니야). 그다음 **`Repository secrets`**에 있는 **`New repository secret`** 버튼 눌러. (`Environment secrets`도 아니라고, 헷갈리지 마.)
3. 아래 두 개 똑바로 입력해.

| Name (이름) | Secret (값) | 필수 여부 |
| :--- | :--- | :---: |
| `HOYOLAB_COOKIES` | `ltoken_v2=복사한_값; ltuid_v2=복사한_값;` | 필수 |
| `DISCORD_WEBHOOK` | `https://discord.com/api/webhooks/복사한_값` | 선택 |

> ⚠️ **제발 이것 좀 틀리지 마**:
> - **`Secret` 칸에 양쪽 큰따옴표(`"`) 붙이지 마!** `.env`랑 다르게 GitHub Secrets는 네가 친 글자 그대로 넘겨버린단 말이야.
> - `Name` 대소문자랑 철자(`HOYOLAB_COOKIES`, `DISCORD_WEBHOOK`) 한 글자라도 틀리거나 빼먹으면 `HOYOLAB_COOKIES 환경변수가 설정되지 않았습니다.` 뜨면서 `exit code 1`로 바로 터지니까 똑바로 확인해.
> - 쿠키랑 웹후크 주소 코드에 직접 적었다가 계정 털려도 난 책임 안 져. 무조건 **GitHub Secrets**에만 넣어.

### 3. 원하는 실행 시간/주기 바꾸기 (`cron` 수정)
[`.github/workflows/checkin.yml`](.github/workflows/checkin.yml) 파일 열어서 `cron` 값 고치면 네가 원하는 시간에 돌릴 수 있어.

```yaml
on:
  schedule:
    - cron: '0 21 * * *' # 기본값: 매일 한국 시간(KST) 오전 06:00
```

> ⏰ **시간 계산 못 할까 봐 알려주는 팁 (UTC vs 한국 시간 KST)**  
> GitHub Actions는 **세계 표준시(UTC)** 기준이라서, 네가 원하는 한국 시간에서 **9시간 빼고** 적어야 해. (`KST - 9시간 = UTC`)

| 원하는 한국 시간 / 주기 | 입력할 `cron` 표현식 | 설명 |
| :--- | :--- | :--- |
| 매일 오전 06:00 (KST) | `'0 21 * * *'` | 기본값 (전날 UTC 21:00) |
| 매일 오전 09:00 (KST) | `'0 0 * * *'` | 한국 시간 오전 9시 |
| 매일 오후 12:00 (KST) | `'0 3 * * *'` | 한국 시간 정오 |
| 매일 밤 00:00 (KST) | `'0 15 * * *'` | 한국 시간 자정 |
| 6시간마다 실행 | `'0 */6 * * *'` | 매 6시간 정각마다 실행 |
| 12시간마다 실행 | `'0 */12 * * *'` | 매 12시간 정각마다 실행 |

> 💡 **참고해**: GitHub Actions 무료 플랜은 전 세계 사람들이 몰리는 **정각(`0`분)**에 걸어두면 대기열에 밀려서 수십 분에서 심하면 3~4시간씩 늦게 돌 수도 있어. 정시에 딱 돌았으면 좋겠으면 `0 21` 대신 `'23 21 * * *'`처럼 어중간한 분으로 바꿔두는 게 낫고, 하루 한 번만 되면 장땡이면 그냥 써도 상관없어.

### 4. Actions 켜고 테스트 한번 돌려보기
1. 네 GitHub 저장소 위쪽 **`Actions`** 탭 들어가.
2. 워크플로우 실행 허용하겠냐고 물어보면 당연히 켜는 버튼 눌러.
3. 왼쪽에서 **`Genshin HoYoLAB Auto Check-in`** 고르고 **`Run workflow`** 눌러서 당장 잘 돌아가는지 확인해 봐. 초록색 체크 뜨고 디스코드 알람 오면 성공이야.

---

## 기술 스택

- **Language**: Python 3
- **Libraries**:
  - `requests`: 호요랩 출석체크 REST API 통신 (`POST`) & 디스코드 웹후크 전송
  - `python-dotenv`: 환경변수 로드 및 설정 분리
- **Automation & CI**:
  - `GitHub Actions`: CI 기반 클라우드 `cron` 스케줄 무인 자동 실행
- **Notification**:
  - `Discord Webhook`: 출석체크 결과 실시간 메시지 전송

---

## 라이선스

MIT License
