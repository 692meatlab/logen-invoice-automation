# 📡 Fiddler를 사용한 로젠택배 API 분석 가이드

이 문서는 로젠택배 클라이언트 프로그램이 사용하는 API를 분석하는 방법을 설명합니다.

---

## 🎯 목표

로젠택배 프로그램이 서버와 통신할 때 사용하는 API 주소와 요청 형식을 찾아냅니다.

---

## 📥 Step 1: Fiddler 설치

### 다운로드 및 설치

1. **Fiddler Everywhere 다운로드**:
   - https://www.telerik.com/download/fiddler/fiddler-everywhere-windows
   - 무료 계정 생성 후 사용 가능

2. **설치 진행**:
   - 다운로드한 설치 파일 실행
   - 기본 설정으로 설치

3. **Fiddler 실행**:
   - 관리자 권한으로 실행 (우클릭 → "관리자 권한으로 실행")
   - 최초 실행 시 계정 로그인 필요

---

## ⚙️ Step 2: Fiddler Everywhere 설정

### HTTPS 트래픽 캡처 설정

많은 프로그램이 HTTPS를 사용하므로 반드시 설정해야 합니다.

1. **좌측 하단의 Settings (톱니바퀴) 아이콘 클릭**
   - 또는 화면 상단의 Settings 메뉴 클릭

2. **Settings 창에서 "HTTPS" 섹션 선택**

3. **HTTPS 설정**:
   - ☑ "Capture HTTPS traffic" 스위치를 ON으로 변경
   - "Trust root certificate" 버튼 클릭
   - 인증서 설치 확인 팝업에서 "Yes" 클릭
   - Windows 보안 경고가 나오면 "예" 클릭

4. **Settings 창 닫기**

---

## 🔍 Step 3: 로젠택배 API 분석

### 3-1. 캡처 시작

1. **Fiddler Everywhere 화면 구성**:
   - 좌측: 세션(요청) 목록
   - 우측: 요청/응답 상세 정보
   - 상단: 캡처 제어 버튼

2. **캡처 시작**:
   - 상단의 **"Live Traffic"** 또는 **"Capturing"** 버튼이 활성화(파란색)되어 있는지 확인
   - 비활성화되어 있으면 클릭하여 캡처 시작
   - 또는 좌측 상단의 **재생 버튼 (▶)** 클릭

---

### 3-2. 로젠택배 프로그램 실행 및 로그인

1. **로젠택배 프로그램 실행**

2. **로그인 진행**:
   - 업체 아이디 입력
   - 비밀번호 입력
   - 로그인 버튼 클릭

3. **Fiddler로 돌아가기**:
   - 좌측 패널에 새로운 HTTP 요청들이 나타남

---

### 3-3. 로그인 API 찾기

**Fiddler Everywhere 좌측 세션 목록**에서 다음을 확인:

#### 찾아야 할 정보:

1. **Host**: 서버 주소 (예: `api.logen.co.kr`)
2. **URL**: API 경로 (예: `/api/auth/login`)
3. **Method**: POST 또는 GET
4. **Status**: 200 (성공)

#### 팁: 로그인 API 찾는 방법

- URL에 "login", "auth", "signin" 등의 단어가 포함된 요청 찾기
- Method가 POST인 요청 찾기
- Status가 200인 요청 찾기

#### 세부 정보 확인:

1. **해당 요청을 클릭** (예: 로그인으로 보이는 POST 요청)

2. **우측 패널의 "Request" 탭 선택**:

   - **Headers 섹션**: 요청 정보 확인
     ```
     Method: POST
     URL: https://api.logen.co.kr/api/v1/auth/login
     Content-Type: application/json
     ```

   - **Body 섹션 → Raw 또는 JSON 뷰**: 실제 전송된 데이터
     ```json
     {
       "id": "33722047",
       "pw": "your_password"
     }
     ```

3. **우측 패널의 "Response" 탭 선택**:

   - **Body 섹션 → JSON 뷰**: 서버 응답
     ```json
     {
       "success": true,
       "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
       "message": "로그인 성공"
     }
     ```

---

### 3-4. 엑셀 다운로드 API 찾기

1. **로젠택배 프로그램에서 엑셀 다운로드**:
   - 송장 조회 메뉴 이동
   - 오늘 날짜 선택
   - 엑셀 다운로드 버튼 클릭

2. **Fiddler Everywhere에서 새로운 요청 확인**:
   - 좌측 세션 목록에서 파일 다운로드 관련 요청 찾기
   - URL에 "export", "excel", "download" 같은 단어가 포함된 요청 찾기
   - Method가 GET이고 Status가 200인 요청

#### 팁: 필터 사용하기

너무 많은 요청이 보이면 필터를 사용하세요:
- 상단의 **Filter** 입력창에 키워드 입력 (예: "logen", "export", "excel")
- Host 별로 필터링 가능

#### 세부 정보 확인:

1. **엑셀 다운로드 요청 클릭**

2. **우측 패널의 "Request" 탭**:
   ```
   Method: GET
   URL: https://api.logen.co.kr/api/v1/invoices/export?date=2025-10-31
   ```

   **Headers 섹션**에서 인증 토큰 확인:
   ```
   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

3. **우측 패널의 "Response" 탭**:
   - **Body 섹션**: 엑셀 파일 바이너리 데이터
   - Content-Type이 `application/vnd.ms-excel` 또는 `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`인지 확인

---

## 📝 Step 4: 정보 정리

수집한 정보를 정리합니다:

### 예시 양식:

```
=== 로그인 API ===
URL: https://api.logen.co.kr/api/v1/auth/login
Method: POST
Content-Type: application/json
Body:
{
  "id": "업체아이디",
  "pw": "비밀번호"
}

=== 송장 조회 API ===
URL: https://api.logen.co.kr/api/v1/invoices/list
Method: GET
Query Parameters: ?date=2025-10-31&status=printed
Headers:
  Authorization: Bearer {token}

=== 엑셀 다운로드 API ===
URL: https://api.logen.co.kr/api/v1/invoices/export
Method: GET
Query Parameters: ?date=2025-10-31
Headers:
  Authorization: Bearer {token}
Response: 엑셀 파일 (binary)
```

---

## 🔧 Step 5: config.json 업데이트

수집한 정보를 바탕으로 `config.json`을 수정합니다.

```json
{
  "logen_credentials": {
    "user_id": "실제_업체아이디"
  },
  "api_endpoints": {
    "base_url": "https://api.logen.co.kr",
    "login": "/api/v1/auth/login",
    "invoices": "/api/v1/invoices/list",
    "excel_download": "/api/v1/invoices/export"
  }
}
```

---

## 💻 Step 6: Python 코드 수정

`logen_api.py`의 `login()` 메서드를 실제 API에 맞게 수정합니다.

### 예시 1: JSON 형식

```python
response = self.session.post(
    login_url,
    json={
        "id": credentials['user_id'],
        "pw": password
    },
    headers={
        "Content-Type": "application/json"
    },
    timeout=self.config['settings']['timeout']
)
```

### 예시 2: Form Data 형식

만약 Fiddler에서 `Content-Type: application/x-www-form-urlencoded`로 표시되면:

```python
response = self.session.post(
    login_url,
    data={  # json 대신 data 사용
        "id": credentials['user_id'],
        "pw": password
    },
    timeout=self.config['settings']['timeout']
)
```

### 예시 3: 인증 토큰 사용

로그인 후 받은 토큰을 다른 API 호출 시 사용:

```python
def login(self, password: str) -> bool:
    # ... 로그인 요청 ...

    if response.status_code == 200:
        data = response.json()
        # 토큰 저장
        self.token = data.get('token')
        # 이후 모든 요청에 사용
        self.session.headers.update({
            'Authorization': f'Bearer {self.token}'
        })
        return True
```

---

## 🐛 문제 해결

### Q1: Fiddler Everywhere에 아무 요청도 안 나타남

**해결**:
1. **캡처가 활성화되어 있는지 확인**:
   - 상단의 "Live Traffic" 버튼이 파란색(활성화)인지 확인
   - 비활성화되어 있으면 클릭

2. **로젠택배 프로그램 재시작**:
   - 프로그램 종료 후 다시 실행
   - Fiddler가 실행 중인 상태에서 프로그램 시작

3. **Fiddler를 관리자 권한으로 실행**:
   - Fiddler 종료
   - 우클릭 → "관리자 권한으로 실행"

4. **Windows 방화벽 확인**

---

### Q2: HTTPS 요청이 암호화되어 내용을 볼 수 없음

**해결**:
1. **좌측 하단 Settings (톱니바퀴) 클릭**
2. **HTTPS 섹션 선택**
3. **"Capture HTTPS traffic" 스위치 ON**
4. **"Trust root certificate" 버튼 클릭**
5. **Windows 보안 경고에서 "예" 클릭**
6. **Fiddler 재시작**

---

### Q3: 로그인 API를 찾을 수 없음

**팁**:
1. **세션 목록 초기화**:
   - 좌측 상단의 쓰레기통 아이콘 클릭 또는 Ctrl + X

2. **필터 사용**:
   - 상단 필터 입력창에 "logen" 입력
   - POST 요청만 보기

3. **천천히 로그인**:
   - 세션 초기화 후
   - 아이디 입력 → 비밀번호 입력 → 로그인 버튼 클릭
   - 새로 생긴 POST 요청 확인
   - "login", "auth", "signin" 등의 단어가 URL에 포함된 것 찾기

---

### Q4: 너무 많은 요청이 나타남

**해결**:
1. Fiddler 우측 상단 **Filters 탭** 클릭
2. "Use Filters" 체크
3. **Hosts** 섹션:
   - "Show only the following Hosts" 선택
   - 로젠택배 도메인만 입력 (예: `*.logen.co.kr`)
4. Actions → "Run Filterset now"

---

## 📌 체크리스트

분석이 완료되었는지 확인:

- [ ] 로그인 API URL 확인
- [ ] 로그인 요청 Method (POST/GET) 확인
- [ ] 로그인 요청 Body 형식 (JSON/Form Data) 확인
- [ ] 엑셀 다운로드 API URL 확인
- [ ] 필요한 헤더 (Authorization 등) 확인
- [ ] config.json 업데이트 완료
- [ ] logen_api.py 수정 완료

---

## 🚀 다음 단계

1. **테스트 실행**:
   ```bash
   cd D:\share\logen-invoice-automation
   python logen_api.py
   ```

2. **로그 확인**:
   - 성공: `downloads` 폴더에 엑셀 파일 생성됨
   - 실패: `logs` 폴더의 로그 파일 확인

3. **디버깅**:
   - 로그 파일에서 오류 메시지 확인
   - Fiddler로 다시 분석
   - 코드 수정 후 재시도

---

## 💡 유용한 팁

### 1. Fiddler AutoResponder로 테스트

API 응답을 임시로 조작해서 테스트 가능:
- Tools → AutoResponder
- 특정 URL에 대해 미리 준비한 JSON 응답 반환

### 2. 요청 재전송

- 요청 우클릭 → "Replay" → "Reissue Request"
- 같은 요청을 다시 보내서 결과 확인

### 3. 요청 저장

- File → Export Sessions → Selected Sessions
- 나중에 참고용으로 저장

---

**문서 작성일**: 2025-10-31
**작성자**: Claude Code Assistant
