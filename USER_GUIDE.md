# 로젠택배 송장 자동화 프로그램 사용 가이드

**버전**: 1.0
**최종 업데이트**: 2025-10-31

---

## 목차

1. [프로그램 소개](#1-프로그램-소개)
2. [사전 준비사항](#2-사전-준비사항)
3. [초기 설치 및 설정](#3-초기-설치-및-설정)
4. [Fiddler를 이용한 API 분석](#4-fiddler를-이용한-api-분석)
5. [프로그램 실행 방법](#5-프로그램-실행-방법)
6. [자동 실행 설정](#6-자동-실행-설정)
7. [문제 해결 가이드](#7-문제-해결-가이드)
8. [FAQ (자주 묻는 질문)](#8-faq-자주-묻는-질문)

---

## 1. 프로그램 소개

### 1.1 프로그램 목적

이 프로그램은 **로젠택배에서 매일 발송된 송장 데이터를 자동으로 다운로드**하여 엑셀 파일로 저장합니다.

**주요 사용 사례**:
- 온라인 쇼핑몰 운영자가 고객에게 송장번호를 회신해야 할 때
- 매일 수동으로 로젠택배 프로그램에서 엑셀을 다운로드하는 번거로움 해소
- 송장 데이터를 자동으로 수집하여 다른 시스템과 연동

### 1.2 프로그램 특징

✅ **완전 자동화**: 한 번 설정하면 버튼 하나로 실행
✅ **암호화 자동 해제**: 로젠택배의 암호화된 데이터를 자동으로 복호화
✅ **엑셀 파일 생성**: 다운로드된 데이터를 바로 사용 가능한 엑셀 형식으로 저장
✅ **상세 로그**: 모든 작업 내역을 로그 파일에 기록
✅ **다중 PC 지원**: 설정 파일만 수정하면 어느 PC에서든 사용 가능

### 1.3 프로그램 작동 원리

```
[로젠택배 서버]
      ↓
   SOAP API 호출 (로그인)
      ↓
   송장 데이터 요청 (암호화됨)
      ↓
   Base64 디코딩
      ↓
   로젠 DLL로 복호화
      ↓
   엑셀 파일로 저장
```

---

## 2. 사전 준비사항

### 2.1 필수 소프트웨어

#### ✅ Python 3.8 이상

**확인 방법**:
```bash
python --version
```

**결과 예시**:
```
Python 3.11.5
```

**설치되지 않은 경우**:
1. https://www.python.org/downloads/ 접속
2. "Download Python" 버튼 클릭
3. 설치 시 **"Add Python to PATH"** 체크 필수!

---

#### ✅ 로젠택배 클라이언트 프로그램

**⚠️ 매우 중요**: 이 프로그램은 **반드시 `C:\iLOGEN`에 설치**되어 있어야 합니다.

**확인 방법**:
1. 내 컴퓨터 → C 드라이브 열기
2. `C:\iLOGEN` 폴더가 있는지 확인
3. `C:\iLOGEN\BIN\Logen.Framework.BaseUtil.dll` 파일이 있는지 확인

**없는 경우**:
- 로젠택배 고객센터(1588-9988)에 문의하여 클라이언트 프로그램 설치

---

#### ✅ Fiddler (패킷 분석 도구)

**용도**: 로젠택배 프로그램이 사용하는 숨겨진 API를 찾기 위해 사용

**다운로드**:
- Fiddler Classic: https://www.telerik.com/download/fiddler
- 또는 Fiddler Everywhere: https://www.telerik.com/download/fiddler/fiddler-everywhere-windows

**설치 후 설정**:
1. Fiddler 실행
2. **Tools → Options → HTTPS** 탭
3. ✅ "Capture HTTPS CONNECTs" 체크
4. ✅ "Decrypt HTTPS traffic" 체크
5. 인증서 설치 경고가 나오면 "Yes" 클릭

---

### 2.2 로젠택배 계정 정보 준비

다음 정보를 미리 준비해두세요:
- **업체 아이디** (로젠택배에서 제공한 숫자)
- **비밀번호**

---

## 3. 초기 설치 및 설정

### 3.1 프로그램 설치

#### Step 1: 폴더 확인

프로그램이 다음 위치에 있는지 확인:
```
D:\share\logen-invoice-automation
```

다른 위치로 복사해도 무방합니다.

---

#### Step 2: Python 라이브러리 설치

**방법 1: 배치 파일 사용 (추천)**

1. `install_requirements.bat` 파일을 **더블 클릭**
2. 설치가 완료될 때까지 기다리기 (약 1-2분)
3. "Press any key to continue..." 메시지가 나오면 아무 키나 누르기

**방법 2: 명령어 직접 입력**

1. `Win + R` 키 → `cmd` 입력 → Enter
2. 다음 명령어 입력:
```bash
cd D:\share\logen-invoice-automation
pip install -r requirements.txt
```

---

#### Step 3: 설치 확인

`check_setup.bat` 파일을 더블 클릭하여 설치 상태 확인

**정상 출력 예시**:
```
Python: 설치됨 (3.11.5)
requests: 설치됨 (2.31.0)
pandas: 설치됨 (2.1.0)
pythonnet: 설치됨 (3.0.3)
openpyxl: 설치됨 (3.1.2)

✓ 모든 필수 요소가 설치되었습니다!
```

---

### 3.2 설정 파일 작성

#### Step 1: 설정 파일 복사

1. `config.example.json` 파일을 같은 폴더에 **복사**
2. 이름을 `config.json`으로 변경

**명령어로 하는 경우**:
```bash
copy config.example.json config.json
```

---

#### Step 2: config.json 편집

`config.json` 파일을 메모장이나 VS Code로 열기

**편집해야 할 부분**:

```json
{
  "logen_credentials": {
    "user_id": "12345",  ← 실제 업체 아이디로 변경
    "encrypted_password": "암호화된_비밀번호",  ← Fiddler로 찾아서 입력
    "ip_address": "192.168.0.1",  ← Fiddler로 찾아서 입력
    "mac_address": "00:11:22:33:44:55"  ← Fiddler로 찾아서 입력
  },
  "api_endpoints": {
    "base_url": "http://ilogen.ilogen.com",  ← 보통 변경 불필요
    "login_soap": "/iLOGEN.COMM.WebService/W_COMM.asmx",
    "data_soap": "/iLOGEN.FC.WebService/W_FC.asmx"
  },
  "paths": {
    "download_folder": "D:\\share\\logen-invoice-automation\\downloads",
    "log_folder": "D:\\share\\logen-invoice-automation\\logs"
  },
  "settings": {
    "timeout": 30
  }
}
```

**⚠️ 중요**: `encrypted_password`, `ip_address`, `mac_address`는 다음 단계(Fiddler 분석)에서 찾아야 합니다.

---

## 4. Fiddler를 이용한 API 분석

### 4.1 왜 Fiddler를 사용해야 하나요?

로젠택배는 공식 API를 제공하지 않습니다. 따라서 클라이언트 프로그램이 **어떤 주소로, 어떤 데이터를 보내는지** 직접 확인해야 합니다.

---

### 4.2 Fiddler 실행 및 설정

#### Step 1: Fiddler 실행

1. Fiddler Classic 또는 Fiddler Everywhere 실행
2. 왼쪽 패널에서 HTTP 요청들이 실시간으로 보이는지 확인

---

#### Step 2: 필터 설정 (선택사항)

너무 많은 요청이 보이면 필터를 설정하세요:

1. **Filters** 탭 클릭
2. **"Show only if URL contains"** 체크
3. 입력란에 `ilogen` 입력

---

### 4.3 로젠택배 프로그램 실행 및 패킷 캡처

#### Step 1: 로그인 요청 캡처

1. **Fiddler가 실행된 상태에서** 로젠택배 프로그램 실행
2. 아이디/비밀번호 입력 후 **로그인 버튼 클릭**
3. Fiddler에서 `ilogen.ilogen.com` 주소로 가는 요청 찾기

**찾아야 할 요청**:
```
POST http://ilogen.ilogen.com/iLOGEN.COMM.WebService/W_COMM.asmx
```

---

#### Step 2: 로그인 요청 상세 정보 확인

해당 요청을 클릭하고 오른쪽 패널에서:

1. **Inspectors** 탭 클릭
2. **Raw** 또는 **XML** 탭 클릭
3. 다음 정보를 찾아서 메모:

```xml
<W_COMM_NTx_LoginEncrypt>
    <arrParam>
        <string>12345</string>  ← user_id
        <string>암호화된비밀번호</string>  ← encrypted_password
        <string>192.168.0.100</string>  ← ip_address
        <string>00-11-22-33-44-55</string>  ← mac_address
    </arrParam>
</W_COMM_NTx_LoginEncrypt>
```

**이 4가지 값을 `config.json`에 입력하세요!**

---

#### Step 3: 송장 조회 요청 캡처

1. 로젠택배 프로그램에서 **송장 조회** 화면으로 이동
2. 조회 조건 입력 (예: 오늘 날짜, 상태: 출력완료)
3. **조회 버튼 클릭**
4. Fiddler에서 다음 요청 찾기:

```
POST http://ilogen.ilogen.com/iLOGEN.FC.WebService/W_FC.asmx
```

---

#### Step 4: 조회 파라미터 추출

해당 요청을 클릭하고:

1. **Inspectors → Raw** 탭
2. `<bytDataParam>` 태그 안의 긴 문자열 복사

**예시**:
```xml
<W_FC0073T_NTx_SelectEnc>
    <bytDataParam>Z/nY+cZ3l4Da0g3Y7trY5OolaKE/unqq/ClhGzkCGqfbli7a47CoTIDU...</bytDataParam>
</W_FC0073T_NTx_SelectEnc>
```

**이 긴 문자열(암호화된 조회 파라미터)을 복사하세요!**

---

### 4.4 추출한 정보 저장

#### config.json 최종 업데이트

```json
{
  "logen_credentials": {
    "user_id": "12345",  ← Fiddler에서 찾은 값
    "encrypted_password": "실제암호화된비밀번호",  ← Fiddler에서 찾은 값
    "ip_address": "192.168.0.100",  ← Fiddler에서 찾은 값
    "mac_address": "00-11-22-33-44-55"  ← Fiddler에서 찾은 값
  }
}
```

#### 조회 파라미터 저장

`logen_invoice_downloader.py` 파일을 열고 314번 줄 부근의 `encrypted_param` 값을 Fiddler에서 복사한 값으로 변경:

```python
encrypted_param = "여기에_Fiddler에서_복사한_긴_문자열_붙여넣기"
```

---

## 5. 프로그램 실행 방법

### 5.1 실행 전 체크리스트

다음 항목들을 모두 확인하세요:

- [ ] Python 3.8+ 설치됨
- [ ] 필수 라이브러리 설치됨 (`pip install -r requirements.txt`)
- [ ] 로젠택배 프로그램이 `C:\iLOGEN`에 설치됨
- [ ] `config.json` 파일 작성 완료
- [ ] Fiddler로 로그인 정보 확인 완료
- [ ] 조회 파라미터 추출 완료

---

### 5.2 방법 1: 배치 파일로 실행 (추천)

#### 실행 방법

`run_downloader.bat` 파일을 **더블 클릭**

#### 정상 실행 화면

```
============================================================
로젠택배 송장 자동 다운로드 프로그램
============================================================

2025-10-31 15:30:00 [INFO] 복호화 DLL 로드 성공
2025-10-31 15:30:00 [INFO] 로그인 시도: http://ilogen.ilogen.com/...
2025-10-31 15:30:01 [INFO] ✓ 로그인 성공
2025-10-31 15:30:02 [INFO] 송장 데이터 조회 중...
2025-10-31 15:30:03 [INFO] ✓ 송장 데이터 조회 성공
2025-10-31 15:30:03 [INFO] 데이터 복호화 중...
2025-10-31 15:30:03 [INFO] Base64 디코딩 완료: 65136 bytes
2025-10-31 15:30:04 [INFO] ✓ 복호화 완료: 5개 테이블
2025-10-31 15:30:04 [INFO] 데이터 테이블 발견: DT6 (60 rows)
2025-10-31 15:30:05 [INFO] ✓ 엑셀 파일 저장 완료: D:\share\...\logen_invoices_20251031_153005.xlsx
============================================================
✓ 모든 작업 완료!
다운로드 파일: D:\share\logen-invoice-automation\downloads\logen_invoices_20251031_153005.xlsx
============================================================

✓ 프로그램이 정상적으로 완료되었습니다.
Press any key to continue . . .
```

---

### 5.3 방법 2: 명령어로 실행

#### 실행 방법

```bash
cd D:\share\logen-invoice-automation
python logen_invoice_downloader.py
```

---

### 5.4 결과 파일 확인

#### 다운로드 폴더 열기

```
D:\share\logen-invoice-automation\downloads\
```

#### 파일명 형식

```
logen_invoices_YYYYMMDD_HHMMSS.xlsx
```

예시: `logen_invoices_20251031_153005.xlsx`

#### 엑셀 파일 내용

파일을 열면 다음과 같은 컬럼들이 있습니다:

| 운송장번호 | 수하인명 | 주소 | 전화번호 | 물품명 | ... |
|------------|----------|------|----------|--------|-----|
| 123456789  | 홍길동   | 서울... | 010-1234-5678 | 스마트폰 | ... |

---

### 5.5 로그 파일 확인

#### 로그 파일 위치

```
D:\share\logen-invoice-automation\logs\logen_YYYYMMDD.log
```

예시: `logen_20251031.log`

#### 로그 파일 용도

- 오류 발생 시 원인 파악
- 실행 이력 확인
- 디버깅

---

## 6. 자동 실행 설정

### 6.1 Windows 작업 스케줄러 사용

매일 자동으로 실행되도록 설정하는 방법입니다.

#### Step 1: 작업 스케줄러 열기

1. `Win + R` 키
2. `taskschd.msc` 입력 → Enter

#### Step 2: 기본 작업 만들기

1. 오른쪽 패널에서 **"기본 작업 만들기"** 클릭

#### Step 3: 작업 이름 입력

- **이름**: `로젠택배 송장 자동 다운로드`
- **설명**: `매일 오후 5시에 송장 데이터를 자동으로 다운로드합니다`
- **다음** 클릭

#### Step 4: 트리거 설정

1. **"매일"** 선택
2. **다음** 클릭
3. **시작 시간**: 오후 5:00 (또는 원하는 시간)
4. **다음** 클릭

#### Step 5: 작업 설정

1. **"프로그램 시작"** 선택
2. **다음** 클릭
3. 다음 정보 입력:
   - **프로그램/스크립트**: `D:\share\logen-invoice-automation\run_downloader.bat`
   - **시작 위치**: `D:\share\logen-invoice-automation`
4. **다음** 클릭

#### Step 6: 완료

1. 설정 내용 확인
2. **마침** 클릭

#### Step 7: 테스트

1. 작업 스케줄러 라이브러리에서 방금 만든 작업 찾기
2. 마우스 오른쪽 클릭 → **"실행"**
3. 정상 작동하는지 확인

---

### 6.2 자동 실행 확인

다음 날 설정한 시간 이후에:

1. `downloads` 폴더에 새 엑셀 파일이 생성되었는지 확인
2. 로그 파일에서 실행 기록 확인

---

## 7. 문제 해결 가이드

### 7.1 오류: "설정 파일을 찾을 수 없습니다"

**증상**:
```
FileNotFoundError: 설정 파일을 찾을 수 없습니다: D:\share\logen-invoice-automation\config.json
```

**원인**:
- `config.json` 파일이 없음

**해결 방법**:
```bash
cd D:\share\logen-invoice-automation
copy config.example.json config.json
```

그 후 `config.json`을 편집하여 실제 정보 입력

---

### 7.2 오류: "로그인 실패"

**증상**:
```
2025-10-31 15:30:01 [ERROR] ✗ 로그인 실패
```

**원인**:
1. 아이디/비밀번호가 틀림
2. `config.json`의 `encrypted_password`가 잘못됨
3. IP 주소나 MAC 주소가 틀림

**해결 방법**:

1. **Fiddler로 다시 확인**:
   - Fiddler 실행 → 로젠택배 프로그램으로 로그인
   - 로그인 요청에서 4가지 값 다시 확인
   - `config.json` 업데이트

2. **로젠택배 프로그램으로 직접 로그인 테스트**:
   - 같은 아이디/비밀번호로 로그인되는지 확인
   - 비밀번호 변경 기간이 지나지 않았는지 확인

---

### 7.3 오류: "복호화 DLL 로드 실패"

**증상**:
```
2025-10-31 15:30:00 [ERROR] 복호화 DLL 로드 실패: Could not load file or assembly
```

**원인**:
- 로젠택배 프로그램이 `C:\iLOGEN`에 설치되지 않음
- `Logen.Framework.BaseUtil.dll` 파일이 없음

**해결 방법**:

1. **로젠택배 프로그램 설치 확인**:
   ```
   C:\iLOGEN\BIN\Logen.Framework.BaseUtil.dll
   ```
   이 파일이 존재하는지 확인

2. **로젠택배 프로그램 재설치**:
   - 로젠택배 고객센터(1588-9988) 문의
   - 클라이언트 프로그램 다시 설치

---

### 7.4 오류: "송장 데이터 조회 실패"

**증상**:
```
2025-10-31 15:30:03 [ERROR] ✗ 송장 데이터 조회 실패
```

**원인**:
- 조회 파라미터(`encrypted_param`)가 잘못됨
- 조회 가능한 데이터가 없음

**해결 방법**:

1. **Fiddler로 조회 파라미터 다시 추출**:
   - Fiddler 실행
   - 로젠택배 프로그램에서 조회 버튼 클릭
   - `W_FC0073T_NTx_SelectEnc` 요청 찾기
   - `<bytDataParam>` 값 복사
   - `logen_invoice_downloader.py` 314번 줄 업데이트

2. **로젠택배 프로그램에서 직접 확인**:
   - 같은 조건으로 조회했을 때 데이터가 나오는지 확인

---

### 7.5 오류: "엑셀 파일 저장 실패"

**증상**:
```
2025-10-31 15:30:05 [ERROR] ✗ 엑셀 저장 실패: Permission denied
```

**원인**:
- 파일이 이미 열려 있음
- 폴더 쓰기 권한이 없음
- 디스크 공간 부족

**해결 방법**:

1. **기존 엑셀 파일 닫기**:
   - `downloads` 폴더의 엑셀 파일들을 모두 닫기

2. **폴더 권한 확인**:
   - `downloads` 폴더에서 마우스 오른쪽 클릭 → 속성
   - 읽기 전용 체크 해제

3. **디스크 공간 확인**:
   - D 드라이브 여유 공간 확인

---

### 7.6 오류: "pythonnet 설치 실패"

**증상**:
```
ERROR: Could not build wheels for pythonnet
```

**원인**:
- .NET Framework가 설치되지 않음
- Visual C++ 재배포 패키지가 없음

**해결 방법**:

1. **.NET Framework 설치**:
   - https://dotnet.microsoft.com/download/dotnet-framework
   - .NET Framework 4.8 이상 설치

2. **Visual C++ 재배포 패키지 설치**:
   - https://aka.ms/vs/17/release/vc_redist.x64.exe
   - 다운로드 후 설치

3. **다시 시도**:
   ```bash
   pip install --upgrade pip
   pip install pythonnet
   ```

---

## 8. FAQ (자주 묻는 질문)

### Q1. 다른 PC에서도 사용할 수 있나요?

**A**: 네, 가능합니다!

**필요한 작업**:
1. 전체 폴더를 다른 PC로 복사
2. 해당 PC에서도 로젠택배 프로그램을 `C:\iLOGEN`에 설치
3. Python 3.8+ 설치
4. `pip install -r requirements.txt` 실행
5. `config.json`의 `paths` 섹션만 해당 PC 경로로 수정

---

### Q2. 조회 날짜를 자동으로 설정할 수 있나요?

**A**: 현재 버전에서는 불가능합니다.

**현재 방식**:
- Fiddler로 조회 요청을 캡처하여 파라미터를 수동으로 입력

**향후 개선 예정**:
- 날짜를 입력하면 자동으로 조회 파라미터를 생성하는 기능 추가
- `EncryptSeed.SetEncrypt()` 메서드를 활용한 파라미터 암호화

---

### Q3. 로젠택배 비밀번호를 주기적으로 변경해야 하는데, 그때마다 설정을 바꿔야 하나요?

**A**: 네, 비밀번호 변경 시 `config.json`을 업데이트해야 합니다.

**방법**:
1. 로젠택배 프로그램에서 비밀번호 변경
2. Fiddler로 로그인 요청 캡처
3. 새로운 `encrypted_password` 값 복사
4. `config.json` 업데이트

**향후 개선 예정**:
- 실행 시 비밀번호를 직접 입력받는 방식으로 변경

---

### Q4. 여러 업체 아이디로 실행할 수 있나요?

**A**: 가능하지만 수동으로 설정을 바꿔야 합니다.

**방법**:
1. 각 업체별로 `config_업체A.json`, `config_업체B.json` 파일 생성
2. 실행 시 사용할 설정 파일 지정:
   ```bash
   python logen_invoice_downloader.py --config config_업체A.json
   ```

**향후 개선 예정**:
- 여러 업체를 한 번에 처리하는 기능

---

### Q5. 엑셀 파일 형식을 변경할 수 있나요?

**A**: 네, 코드를 수정하면 가능합니다.

**예시 - CSV로 저장하려면**:

`logen_invoice_downloader.py` 245번 줄을:
```python
df.to_excel(file_path, index=False, engine='openpyxl')
```

다음과 같이 변경:
```python
df.to_csv(file_path, index=False, encoding='utf-8-sig')
```

---

### Q6. 특정 컬럼만 추출할 수 있나요?

**A**: 네, 가능합니다.

**예시 - 운송장번호, 수하인명, 전화번호만 추출**:

`logen_invoice_downloader.py` 242번 줄 다음에 추가:
```python
df = df[['운송장번호', '수하인명', '전화번호']]
```

---

### Q7. 데이터가 너무 많으면 어떻게 하나요?

**A**: 프로그램은 모든 데이터를 처리합니다.

**성능 팁**:
- 조회 조건을 좁혀서 데이터 양 줄이기
- SSD를 사용하여 파일 쓰기 속도 향상

---

### Q8. 로그 파일이 계속 쌓이는데 삭제해도 되나요?

**A**: 네, 오래된 로그 파일은 삭제해도 됩니다.

**자동 삭제 스크립트** (선택사항):

`cleanup_old_logs.bat` 파일 생성:
```batch
@echo off
forfiles /p "D:\share\logen-invoice-automation\logs" /s /m *.log /d -30 /c "cmd /c del @path"
echo 30일 이상 된 로그 파일이 삭제되었습니다.
pause
```

---

### Q9. 프로그램 실행 중에 에러가 나면 어떻게 하나요?

**A**: 다음 순서로 확인하세요:

1. **로그 파일 확인**:
   ```
   D:\share\logen-invoice-automation\logs\logen_YYYYMMDD.log
   ```

2. **이 가이드의 문제 해결 섹션 참조**

3. **Fiddler로 API 요청 재확인**

4. **위 방법으로도 해결 안 되면**:
   - 개발 기록 확인: `DEVELOPMENT_LOG.md`
   - README.md 참조

---

### Q10. API 주소가 변경되면 어떻게 하나요?

**A**: `config.json`을 수정하세요.

**수정 위치**:
```json
{
  "api_endpoints": {
    "base_url": "http://ilogen.ilogen.com",  ← 여기 변경
    "login_soap": "/iLOGEN.COMM.WebService/W_COMM.asmx",
    "data_soap": "/iLOGEN.FC.WebService/W_FC.asmx"
  }
}
```

Fiddler로 새로운 주소를 확인한 후 업데이트하세요.

---

## 부록 A: 전체 실행 흐름도

```
[시작]
   ↓
[Python 설치 확인]
   ↓
[pip install -r requirements.txt]
   ↓
[로젠택배 프로그램 설치 확인 (C:\iLOGEN)]
   ↓
[Fiddler 설치 및 설정]
   ↓
[로젠택배 프로그램 실행]
   ↓
[Fiddler로 로그인 요청 캡처]
   ↓
[user_id, encrypted_password, ip_address, mac_address 추출]
   ↓
[config.json 작성]
   ↓
[Fiddler로 조회 요청 캡처]
   ↓
[bytDataParam (조회 파라미터) 추출]
   ↓
[logen_invoice_downloader.py에 파라미터 입력]
   ↓
[run_downloader.bat 실행]
   ↓
[downloads 폴더에서 엑셀 파일 확인]
   ↓
[자동 실행 설정 (작업 스케줄러)]
   ↓
[완료]
```

---

## 부록 B: 파일 목록 및 역할

| 파일명 | 역할 | 수정 필요 여부 |
|--------|------|----------------|
| `logen_invoice_downloader.py` | 메인 실행 스크립트 | ⚠️ encrypted_param만 수정 |
| `config.json` | 설정 파일 (아이디, 비밀번호 등) | ✅ 반드시 수정 |
| `config.example.json` | 설정 파일 예시 | ❌ 수정 불필요 |
| `requirements.txt` | Python 패키지 목록 | ❌ 수정 불필요 |
| `run_downloader.bat` | 실행 배치 파일 | ❌ 수정 불필요 |
| `install_requirements.bat` | 라이브러리 설치 배치 파일 | ❌ 수정 불필요 |
| `check_setup.bat` | 환경 확인 배치 파일 | ❌ 수정 불필요 |
| `README.md` | 프로젝트 개요 | ❌ 수정 불필요 |
| `DEVELOPMENT_LOG.md` | 개발 과정 기록 | ❌ 수정 불필요 |
| `USER_GUIDE.md` | 이 문서 | ❌ 수정 불필요 |

---

## 부록 C: 연락처 및 지원

### 로젠택배 고객센터
- **전화**: 1588-9988
- **운영시간**: 평일 09:00 ~ 18:00

### Python 관련 도움말
- 공식 문서: https://docs.python.org/ko/3/
- 한국어 커뮤니티: https://python.kr/

### Fiddler 사용법
- 공식 문서: https://docs.telerik.com/fiddler

---

**마지막 업데이트**: 2025-10-31
**버전**: 1.0
