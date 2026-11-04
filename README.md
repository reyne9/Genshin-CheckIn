# 🌌 HoYoLAB Genshin Impact Auto Check-in

> **원신(Genshin Impact) 호요랩 웹 일일 출석체크 24/7 완전 자동화 프로젝트**  
> GitHub Actions를 통해 컴퓨터가 꺼져 있어도 매일 자동으로 출석 보상을 수령하고, Discord로 알림을 받아볼 수 있습니다.

---

## ✨ 주요 기능

- ⚡ **완전 무인 자동화**: GitHub Actions의 Cron 스케줄러로 매일 자동 실행 (기본: KST 오전 06:00)
- 🔒 **보안 우선 설계**: 민감한 인증 정보(쿠키)는 절대 코드에 포함되지 않으며, GitHub Encrypted Secrets 및 `.env`로 격리
- 📢 **Discord 웹훅 알림**: 출석 성공, 획득 보상 아이템, 누적 출석일수, 실패 원인을 깔끔한 임베드(Embed) 메시지로 전송
- 🛡️ **안정적인 예외 처리**: 세션 만료, 중복 출석, 네트워크 지연에 대한 방어 로직 내장

---

## 🔒 보안 안내 (필독)

이 저장소는 **Public(공개) 상태로 Fork하여 사용하여도 안전하도록 설계**되었습니다.
- 사용자의 로그인 쿠키(`HOYOLAB_COOKIES`)는 절대 저장소 코드나 커밋 기록에 남지 않습니다.
- GitHub Actions 실행 시 GitHub의 **양방향 암호화 비밀 저장소(Encrypted Secrets)**를 통해서만 메모리에 일시적으로 로드됩니다.
- **주의**: `.env` 파일은 절대 Git에 커밋하지 마세요. (`.gitignore`에 이미 등록되어 보호 중입니다.)

---

## 🚀 빠른 시작 가이드 (GitHub Actions - 추천)

컴퓨터가 꺼져 있어도 매일 자동으로 실행되는 방식입니다.

### 1단계: 이 저장소 Fork 하기
우측 상단의 **`Fork`** 버튼을 눌러 본인의 GitHub 계정으로 복제합니다.

### 2단계: HoYoLAB 쿠키 추출하기
1. PC 웹 브라우저(Chrome, Edge 등)에서 [호요랩 원신 출석체크 페이지](https://act.hoyolab.com/ys/event/e202102251931481/index.html)에 접속하여 로그인합니다.
2. 키보드의 **`F12`** 키를 눌러 **개발자 도구**를 엽니다.
3. 상단 탭에서 **`애플리케이션(Application)`** (또는 `스토리지`) $\rightarrow$ 좌측 **`쿠키(Cookies)`** $\rightarrow$ `https://act.hoyolab.com`을 클릭합니다.
4. 쿠키 목록 중 아래 두 항목의 값을 확인합니다:
   - `ltoken_v2`: (예: `v2_CAIS...`)
   - `ltuid_v2`: (예: `123456789`)
5. 아래 형식으로 텍스트를 준비합니다:
   ```text
   ltoken_v2=v2_xxxx; ltuid_v2=123456789;
   ```
   > 💡 *팁: `account_id_v2`, `cookie_token_v2`를 포함한 전체 쿠키를 복사해 넣어도 정상 작동합니다.*

### 3단계: GitHub Secrets 등록
1. Fork한 본인의 저장소로 이동합니다.
2. 상단 메뉴의 **`Settings`** $\rightarrow$ 좌측 메뉴의 **`Secrets and variables`** $\rightarrow$ **`Actions`**를 클릭합니다.
3. **`New repository secret`** 버튼을 클릭하여 아래 항목을 등록합니다:

| Secret 이름 | 필수 여부 | 값 예시 | 설명 |
| :--- | :---: | :--- | :--- |
| `HOYOLAB_COOKIES` | **필수** | `ltoken_v2=v2_...; ltuid_v2=...;` | 2단계에서 복사한 쿠키 문자열 |
| `DISCORD_WEBHOOK_URL` | 선택 | `https://discord.com/api/webhooks/...` | 결과를 전송받을 디스코드 웹훅 주소 |
| `HOYOLAB_LANG` | 선택 | `ko-kr` (기본값) | 언어 설정 (`ko-kr`, `en-us`, `ja-jp` 등) |

### 4단계: 동작 테스트 및 활성화
1. Fork한 저장소의 상단 **`Actions`** 탭으로 이동합니다.
2. *"I understand my workflows, go ahead and enable them"* 버튼이 보이면 클릭하여 Actions를 활성화합니다.
3. 좌측 목록에서 **`HoYoLAB Daily Check-in`**을 클릭합니다.
4. 우측의 **`Run workflow`** 드롭다운 버튼을 누르고 초록색 **`Run workflow`**를 클릭해 즉시 테스트합니다.
5. 실행 기록을 클릭하여 초록색 체크(`✔`)와 함께 콘솔 로그에 출석 성공 메시지가 출력되는지 확인합니다.

---

## 💻 로컬 PC에서 직접 실행하기

개발 및 디버깅 목적으로 본인 컴퓨터에서 직접 실행하는 방법입니다.

### 1. 저장소 클론 및 가상환경 설정
```bash
git clone https://github.com/your-username/hoyolab-auto-checkin.git
cd hoyolab-auto-checkin

# 가상환경 생성 및 활성화 (Mac/Linux)
python3 -m venv .venv
source .venv/bin/activate

# (Windows의 경우)
# python -m venv .venv
# .venv\Scripts\activate
```

### 2. 의존성 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 환경변수 파일 설정
`.env.example`을 복사하여 `.env` 파일을 생성하고 본인의 정보를 입력합니다:
```bash
cp .env.example .env
```
`.env` 파일 편집:
```env
HOYOLAB_COOKIES="ltoken_v2=your_token_value; ltuid_v2=your_uid_value;"
HOYOLAB_LANG="ko-kr"
DISCORD_WEBHOOK_URL=""
```

### 4. 스크립트 실행
```bash
python main.py
```

---

## 🛠️ 기술적 세부사항 및 동작 원리

이 프로젝트는 소프트웨어 엔지니어링 관점에서 다음과 같이 설계되었습니다:

1. **호요랩 엔드포인트 파이프라인**:
   - `GET /event/sol/info`: 오늘 이미 출석했는지 여부(`is_sign`) 및 누적 출석일 확인
   - `POST /event/sol/sign`: 출석 체크 트랜잭션 수행 (`act_id=e202102251931481`)
   - `GET /event/sol/home`: 이달의 전체 보상 매핑 테이블을 가져와 오늘의 획득 아이템 명칭 확인
2. **헤더 스푸핑(Header Spoofing)**:
   - 봇 차단을 방지하기 위해 일반 최신 데스크톱 브라우저의 `User-Agent`, `Referer`, `Origin`을 정확히 모사합니다.
3. **무상태(Stateless) & 멱등성(Idempotency)**:
   - 스크립트를 하루에 여러 번 실행하더라도 에러가 발생하지 않으며, 이미 출석한 상태(`-5003`)를 안전하게 처리합니다.

---

## ⚠️ 면책 조항 (Disclaimer)

- 본 프로젝트는 HoYoverse(miHoYo)의 공식 서비스가 아니며, 개인이 학습 및 편의를 위해 제작한 비공식 오픈소스 도구입니다.
- 자동화 스크립트 사용으로 인해 발생하는 계정 관련 불이익에 대해 제작자는 책임을 지지 않습니다.
