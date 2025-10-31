# 로젠택배 송장 자동화 프로그램 개발 기록

## 📋 프로젝트 개요

**목적**: 로젠택배 클라이언트 프로그램에서 자동으로 송장 데이터를 추출하여 고객에게 회신

**개발 기간**: 2025-10-31 ~

**개발 방법**: 네트워크 패킷 분석 → API 직접 호출

---

## 💬 개발 과정 대화 내역

### Step 1: 문제 정의 (2025-10-31)

**사용자 요구사항**:
> "우리회사에서 온라인으로 물건 주문한 고객에게 (이메일 주문 포함) 송장번호를 회신해 줘야 하는데, 택배사는 로젠택배를 쓰고있어. 근데 얘네는 api를 제공 안하는것 같고, 로젠택배 프로그램 아이디(업체에서 제공한 숫자) 비밀번호로 로그인해서, 오늘 발송된 애들(송장출력 완료)의 엑젤자료를 가지고 오는걸 만들고 싶어."

**문제 분석**:
- 로젠택배는 공식 API를 제공하지 않음
- 클라이언트 프로그램(설치형)을 통해 데이터 접근 필요
- 매일 발송된 송장 데이터를 자동으로 추출해야 함

---

### Step 2: 해결 방법 탐색

**제안된 방법들**:

#### 방법 A: 네트워크 패킷 분석 ✅ (선택됨)
- Fiddler/Wireshark로 클라이언트 프로그램의 HTTP 요청 분석
- 실제 API 엔드포인트를 찾아서 Python으로 직접 호출
- **장점**: 빠르고 안정적, 서버 자원 적게 사용
- **단점**: 초기 분석 필요

#### 방법 B: UI 자동화 (pywinauto)
- Windows 프로그램의 UI 요소를 직접 제어
- **장점**: 별도 분석 없이 바로 구현 가능
- **단점**: 느리고 불안정, 프로그램 UI 변경 시 수정 필요

#### 방법 C: 웹 자동화 (Selenium/Playwright)
- 웹 기반일 경우에만 해당
- **로젠택배는 설치 프로그램이므로 해당 없음**

---

### Step 3: 중계 업체 분석

**질문**:
> "어떤 온라인 중계 업체들(네이버 스마트스토어, 플레이오토) 이런곳들은 보면 우리가 회원가입을하고, 우리 택배사 정보(아이디 비번)을 넣으면 우리 회사(그 택배사 아이디)로 보낸 정보들을다 긁어와서 보여주는데 어떤형태로 하는건지 잘 모르겠네."

**답변**:
중계 업체들의 방식:
1. **공식 API 계약**: 택배사와 직접 계약하여 특별 API 키 발급 (대량 처리용)
2. **서버 기반 스크래핑**: 고객 계정 정보를 받아서 서버에서 대신 로그인/크롤링
3. **업체용 전용 솔루션**: 택배사가 제공하는 중계업체 전용 프로그램/FTP 사용

→ **일반 업체는 네트워크 패킷 분석이 현실적인 최선의 방법**

---

### Step 4: 프로젝트 구조 결정

**사용자 요청**:
> "그럼 A로 하고 이 PC 뿐만 아니라 다른 PC에서도 설치해서 사용할 수 있게 절대경로로 작성해주고, 별도 프로젝트 폴더 만들어서 우리가 어떤대화들을 나누면서 스탭바이 스탭으로 프로그램 결과물까지 나올 수 있었는지도 저장해줘."

**결정 사항**:
- 방법 A (네트워크 패킷 분석) 채택
- 다중 PC 지원 (설정 파일로 관리)
- 프로젝트 위치: `D:\share\logen-invoice-automation`
- 개발 과정 문서화

---

## 📂 프로젝트 구조

```
D:\share\logen-invoice-automation\
├── logen_api.py              # 메인 스크립트 (API 호출)
├── config.json                # 설정 파일 (아이디/비번/경로)
├── requirements.txt           # Python 패키지 목록
├── README.md                  # 사용 가이드
├── DEVELOPMENT_LOG.md         # 이 문서 (개발 기록)
├── docs/
│   └── FIDDLER_GUIDE.md      # Fiddler 사용법
├── logs/                      # 실행 로그
└── downloads/                 # 다운로드된 엑셀 파일
```

---

## 🔧 기술 스택

- **언어**: Python 3.8+
- **핵심 라이브러리**:
  - `requests`: SOAP API 호출
  - `pythonnet`: .NET DLL 호출 (복호화 핵심)
  - `pandas`: 데이터 처리
  - `openpyxl`: 엑셀 파일 저장
- **분석 도구**: Fiddler (패킷 분석)
- **외부 의존성**:
  - 로젠택배 클라이언트 프로그램 (`C:\iLOGEN`)
  - `Logen.Framework.BaseUtil.dll` (복호화 DLL)

---

### Step 5: 비밀번호 보안 강화 (2025-10-31)

**사용자 제안**:
> "로젠택배는 일정주기가 지나면 비밀번호를 무조건 바꿔야 하니까 프로그램 실행할때 비밀번호는 직접 입력하는게 나을것 같아."

**구현 결정**:
- 비밀번호를 `config.json`에 저장하지 않음
- 프로그램 실행 시 `getpass` 모듈로 비밀번호 입력받기
- 입력 시 화면에 표시되지 않아 보안 강화

**변경 사항**:
1. `logen_api.py`:
   - `import getpass` 추가
   - `login()` 메서드에 `password` 매개변수 추가
   - `run()` 메서드에 `password` 매개변수 추가
   - `main()` 함수에서 `getpass.getpass()`로 비밀번호 입력받기

2. `config.json` / `config.example.json`:
   - `password` 필드 제거
   - `_password_note` 추가하여 실행 시 입력받는다는 안내

3. **장점**:
   - 비밀번호 주기적 변경에 유연하게 대응
   - 설정 파일이 노출되어도 비밀번호는 안전
   - 보안 강화

---

### Step 6: Fiddler 패킷 분석 (2025-10-31)

**사용자 작업**:
- Fiddler로 로젠택배 프로그램의 네트워크 요청 캡처
- SOAP API 호출 발견: `http://ilogen.ilogen.com`
- 로그인 API: `W_COMM_NTx_LoginEncrypt`
- 조회 API: `W_FC0073T_NTx_SelectEnc`

**핵심 발견**:
1. **SOAP 프로토콜 사용**: REST가 아닌 SOAP 방식
2. **암호화된 파라미터**: 로그인 시 암호화된 비밀번호, IP, MAC 주소 전송
3. **암호화된 응답**: 조회 결과가 Base64 + 암호화된 상태로 반환

---

### Step 7: SOAP API 클라이언트 작성 (2025-10-31)

**구현 내용**:
- `logen_soap_api.py` 작성
- SOAP Envelope 구조 생성
- 로그인 API 호출 성공 확인
- 로그 파일 생성 (`logs/logen_20251031.log`)

**테스트 결과**:
```
2025-10-31 19:16:27 [INFO] 로그인 시도: http://ilogen.ilogen.com/iLOGEN.COMM.WebService/W_COMM.asmx
2025-10-31 19:16:27 [INFO] ✓ 로그인 성공
```

---

### Step 8: 암호화 문제 발견 (2025-10-31)

**문제**:
- 송장 데이터 조회 시 응답이 암호화되어 있음
- Base64 디코딩만으로는 해독 불가
- 클라이언트 측에서 복호화 수행하는 것으로 추정

**사용자 확인**:
> "내가 보기엔 암호화 해서 보여주는것 같아. 그래서 실제로 내보내기 버튼을 누를때 복호화해서 값들이 보이는것 같고"

**분석**:
- 내보내기 버튼 클릭 시 별도 API 호출 없음
- **시나리오 B 확정**: 클라이언트가 직접 복호화

---

### Step 9: 로젠 DLL 분석 (2025-10-31)

**로젠 프로그램 위치 확인**:
```
C:\iLOGEN\
├── BIN\
│   ├── iLOGEN.exe
│   └── Logen.Framework.BaseUtil.dll  ← 핵심 DLL
└── Assembly\
    ├── LILIS.PROXY.COMM.dll
    ├── LILIS.PROXY.FC.dll
    └── LILIS.UI.FC01.dll
```

**DLL 분석**:
1. `pythonnet` 라이브러리로 .NET DLL 로드
2. `Logen.Framework.BaseUtil.EncryptSeed` 클래스 발견
3. 복호화 메서드 발견:
   - `SetDecrypt(byte[])` → DataSet 반환
   - `SetDecryptArray(byte[])` → String[] 반환

---

### Step 10: 복호화 성공! (2025-10-31)

**복호화 프로세스**:
```python
# 1. Base64 디코딩
encrypted_bytes = base64.b64decode(encrypted_base64)

# 2. .NET DLL 로드
asm = Assembly.LoadFrom('C:\\iLOGEN\\BIN\\Logen.Framework.BaseUtil.dll')
encrypt_seed_type = asm.GetType('Logen.Framework.BaseUtil.EncryptSeed')
instance = Activator.CreateInstance(encrypt_seed_type)

# 3. 복호화
net_bytes = Array[Byte](encrypted_bytes)
dataset = instance.SetDecrypt(net_bytes)
```

**결과**:
- ✅ 65,136 bytes 복호화 성공
- ✅ DataSet 5개 테이블 추출
- ✅ Table 2 (DT6): 60개 송장 데이터, 96개 컬럼

---

### Step 11: 엑셀 저장 구현 (2025-10-31)

**데이터 추출**:
- DataSet → Pandas DataFrame 변환
- 컬럼명: 운송장번호, 수하인명, 주소, 전화번호, 물품명 등
- Excel 파일 저장: `downloads/logen_invoices_YYYYMMDD_HHMMSS.xlsx`

**테스트**:
- ✅ 실제 엑셀 파일과 비교 검증 완료
- ✅ 데이터 일치 확인

---

### Step 12: 통합 스크립트 작성 (2025-10-31)

**`logen_invoice_downloader.py` 완성**:
1. SOAP API 로그인
2. 암호화된 송장 데이터 조회
3. Base64 디코딩
4. .NET DLL로 복호화
5. 엑셀 파일 저장
6. 로그 기록

**배치 파일 작성**:
- `run_downloader.bat` - 실행 스크립트
- `install_requirements.bat` - 라이브러리 설치

---

## 📝 최종 개발 진행 상황

### ✅ 완료
- [x] 프로젝트 폴더 생성 및 구조 설정
- [x] Fiddler 패킷 분석 완료
- [x] SOAP API 엔드포인트 발견
- [x] 로그인 기능 구현 및 테스트 성공
- [x] 암호화 메커니즘 파악
- [x] 로젠 DLL 분석 및 복호화 메서드 발견
- [x] Base64 디코딩 + DLL 복호화 구현
- [x] DataSet → Excel 변환 구현
- [x] 통합 스크립트 완성 (`logen_invoice_downloader.py`)
- [x] 실행 배치 파일 작성
- [x] requirements.txt 업데이트 (pythonnet, pandas 추가)
- [x] README.md 업데이트
- [x] DEVELOPMENT_LOG.md 업데이트
- [x] 실제 데이터로 검증 완료

### ⚠️ 제한사항 (향후 개선 필요)
- [ ] 조회 파라미터 자동 생성 (현재: 수동 입력 필요)
- [ ] 날짜 기반 자동 조회
- [ ] 이메일 자동 발송
- [ ] 스케줄러 (매일 자동 실행)

---

## 🎯 최종 목표

1. **사용자가 Fiddler로 로젠택배 API를 분석**
2. **분석된 API 정보를 바탕으로 Python 스크립트 완성**
3. **어떤 PC에서든 설정 파일만 수정하면 바로 실행 가능**
4. **매일 자동으로 송장 데이터를 다운로드**

---

## 📌 참고사항

- 로젠택배 프로그램은 **설치형 클라이언트**
- API가 공식 제공되지 않으므로 **역엔지니어링 방식** 사용
- 패킷 분석을 통해 숨겨진 API 엔드포인트 발견 예정
- 다른 PC 이식성을 위해 **절대 경로를 설정 파일로 관리**

---

## 🔐 보안 주의사항

⚠️ `config.json` 파일에는 택배사 로그인 정보가 포함되므로:
- Git에 커밋하지 말 것 (`.gitignore`에 추가)
- 파일 권한 설정 필요
- 백업 시 암호화 권장

---

*이 문서는 프로젝트 개발이 진행됨에 따라 계속 업데이트됩니다.*
