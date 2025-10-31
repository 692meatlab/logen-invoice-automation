# 🚚 로젠택배 송장 자동 다운로드 프로그램

로젠택배 클라이언트 프로그램에서 매일 발송된 송장 데이터를 자동으로 다운로드하는 Python 프로그램입니다.

**버전**: 1.0
**최종 업데이트**: 2025-10-31

---

## 📋 목차

1. [프로젝트 소개](#-프로젝트-소개)
2. [주요 기능](#-주요-기능)
3. [빠른 시작](#-빠른-시작)
4. [상세 가이드](#-상세-가이드)
5. [프로젝트 구조](#-프로젝트-구조)
6. [기술 스택](#-기술-스택)
7. [제한사항](#-제한사항)
8. [문제 해결](#-문제-해결)
9. [추가 문서](#-추가-문서)

---

## 🎯 프로젝트 소개

온라인 주문 고객에게 송장번호를 회신하기 위해 로젠택배에서 송장 데이터를 자동으로 추출합니다.

**개발 배경**:
- 로젠택배는 공식 API를 제공하지 않음
- 매일 수동으로 프로그램에서 엑셀을 다운로드하는 번거로움 해소
- 네트워크 패킷 분석을 통해 숨겨진 API를 찾아 자동화

---

## ✨ 주요 기능

- ✅ 로젠택배 SOAP API 자동 로그인
- ✅ 암호화된 송장 데이터 조회 및 자동 복호화
- ✅ 로젠 DLL (`Logen.Framework.BaseUtil.dll`) 활용한 복호화
- ✅ 엑셀 파일 자동 저장
- ✅ 상세 로그 기록
- ✅ 다중 PC 지원 (설정 파일만 수정하면 어디서든 사용 가능)
- 🔜 조회 파라미터 자동 생성 (날짜 기반)
- 🔜 이메일 자동 발송
- 🔜 스케줄러 (매일 자동 실행)

---

## ⚡ 빠른 시작

### 1단계: Python 설치 확인
```bash
python --version
```
Python 3.8 이상 필요

### 2단계: 라이브러리 설치
`install_requirements.bat` 더블 클릭 또는:
```bash
pip install -r requirements.txt
```

### 3단계: 설정 파일 작성
```bash
copy config.example.json config.json
```
`config.json`을 편집하여 실제 정보 입력

### 4단계: Fiddler로 API 분석
- Fiddler로 로젠택배 프로그램의 네트워크 요청 캡처
- 로그인 정보 및 조회 파라미터 추출
- 상세 방법은 [USER_GUIDE.md](USER_GUIDE.md) 참조

### 5단계: 실행
`run_downloader.bat` 더블 클릭

---

## 📚 상세 가이드

**처음 사용하시나요?**

👉 **[USER_GUIDE.md](USER_GUIDE.md)를 먼저 읽어주세요!**

USER_GUIDE.md에는 다음 내용이 포함되어 있습니다:
- 사전 준비사항 상세 설명
- Fiddler 설치 및 사용법 (스크린샷 포함)
- 설정 파일 작성 가이드
- 단계별 실행 방법
- 자동 실행 설정 (Windows 작업 스케줄러)
- 문제 해결 가이드
- FAQ (자주 묻는 질문)

**개발 과정이 궁금하신가요?**

👉 **[DEVELOPMENT_LOG.md](DEVELOPMENT_LOG.md)를 읽어주세요!**

DEVELOPMENT_LOG.md에는 다음 내용이 포함되어 있습니다:
- 프로젝트 개발 배경
- 단계별 개발 과정 (Step 1 ~ Step 12)
- 기술적 문제 해결 과정
- SOAP API 분석 및 암호화 해제 방법
- .NET DLL 활용한 복호화 구현

---

## 🔧 문제 해결

### Q1: "설정 파일을 찾을 수 없습니다" 오류

**해결**:
```bash
copy config.example.json config.json
```
그 후 `config.json`을 편집하여 실제 정보 입력

---

### Q2: "로그인 실패" 오류

**원인**:
1. 아이디/비밀번호가 잘못됨
2. API 주소가 틀림
3. 요청 형식이 실제 API와 다름

**해결**:
1. `config.json`의 credentials 확인
2. Fiddler로 다시 패킷 분석
3. `logen_api.py`의 `login()` 메서드 수정:
   - POST 방식인지 확인
   - JSON/Form Data 형식 확인
   - 헤더 추가 필요 여부 확인

---

### Q3: "엑셀 다운로드 실패" 오류

**해결**:
1. 로그 파일 확인: `logs/logen_YYYYMMDD.log`
2. Fiddler로 엑셀 다운로드 요청 다시 분석
3. 날짜 형식 확인
4. 파일 권한 확인

---

### Q4: 다른 PC에서 실행이 안 됨

**체크리스트**:
- [ ] Python 3.8+ 설치됨
- [ ] `pip install -r requirements.txt` 실행함
- [ ] `config.json`의 `paths` 섹션을 해당 PC 경로로 수정함
- [ ] 해당 폴더에 쓰기 권한이 있음

---

## 📁 프로젝트 구조

```
D:\share\logen-invoice-automation\
├── logen_invoice_downloader.py   # 메인 실행 스크립트 ⭐
├── config.json                    # 설정 파일 (직접 작성 필요)
├── config.example.json            # 설정 파일 예시
├── requirements.txt               # Python 패키지 목록
├── README.md                      # 프로젝트 개요 (이 문서)
├── USER_GUIDE.md                  # 상세 사용 가이드 ⭐
├── DEVELOPMENT_LOG.md             # 개발 과정 기록
├── run_downloader.bat             # 실행 배치 파일 ⭐
├── install_requirements.bat       # 라이브러리 설치 배치 파일
├── check_setup.bat                # 환경 확인 배치 파일
├── logs/                          # 실행 로그 (자동 생성)
└── downloads/                     # 엑셀 파일 저장 (자동 생성)
```

**주요 파일 설명**:
- **logen_invoice_downloader.py**: SOAP API 호출 → 복호화 → 엑셀 저장
- **config.json**: 로그인 정보 및 API 엔드포인트 설정
- **run_downloader.bat**: 간편 실행용 배치 파일

---

## 🔧 기술 스택

### 언어 및 프레임워크
- **Python 3.8+**: 메인 프로그래밍 언어

### 핵심 라이브러리
- **requests**: SOAP API 호출
- **pythonnet**: .NET DLL 로드 및 호출 (복호화 핵심)
- **pandas**: 데이터 처리 및 변환
- **openpyxl**: 엑셀 파일 생성

### 외부 의존성
- **로젠택배 클라이언트**: `C:\iLOGEN` (복호화 DLL 필요)
- **Logen.Framework.BaseUtil.dll**: 암호화 데이터 복호화

### 분석 도구
- **Fiddler**: 네트워크 패킷 분석 및 API 엔드포인트 발견

### 작동 원리
```
[SOAP API 호출]
      ↓
[암호화된 응답 수신]
      ↓
[Base64 디코딩]
      ↓
[.NET DLL 복호화]
      ↓
[DataSet → DataFrame]
      ↓
[엑셀 파일 저장]
```

---

## ⚠️ 제한사항

### 조회 파라미터 수동 설정 필요

현재 버전에서는 **조회 파라미터(날짜, 조건 등)를 자동 생성하지 못합니다**.

따라서:
1. Fiddler로 로젠 프로그램의 조회 요청을 캡처
2. `bytDataParam` 값을 복사
3. 코드의 `encrypted_param` 변수에 붙여넣기

**향후 개선 예정**:
- 날짜 입력 시 자동으로 조회 파라미터 생성
- `EncryptSeed.SetEncrypt()` 메서드를 활용한 파라미터 암호화

### 로젠 프로그램 필수 설치

이 프로그램은 로젠택배 클라이언트의 DLL 파일을 직접 사용합니다.
따라서 **로젠택배 프로그램이 `C:\iLOGEN`에 설치되어 있어야** 작동합니다.

---

## 🔐 보안 주의사항

⚠️ **중요**: `config.json`에는 로그인 정보가 포함되어 있습니다.

- Git에 커밋하지 마세요 (`.gitignore`에 추가됨)
- 파일 권한 설정 권장
- 다른 사람과 공유할 때 주의

---

## 📚 추가 문서

### 필수 문서
- **[USER_GUIDE.md](USER_GUIDE.md)** ⭐ - 상세 사용 가이드 (처음 사용자 필독!)
  - Fiddler 사용법 및 API 분석 방법
  - 설정 파일 작성 가이드
  - 단계별 실행 방법
  - 문제 해결 및 FAQ

### 참고 문서
- **[DEVELOPMENT_LOG.md](DEVELOPMENT_LOG.md)** - 개발 과정 기록
  - 프로젝트 개발 배경 및 동기
  - 단계별 개발 과정 (Step 1 ~ Step 12)
  - 기술적 문제 해결 과정
  - 암호화/복호화 구현 상세

---

## 🆘 지원 및 문제 해결

### 문제 발생 시 확인 순서

1. **로그 파일 확인**:
   ```
   logs/logen_YYYYMMDD.log
   ```

2. **USER_GUIDE.md 문제 해결 섹션 참조**:
   - 로그인 실패
   - 복호화 오류
   - 엑셀 저장 실패
   - 기타 일반적인 문제들

3. **Fiddler로 API 재분석**:
   - API 주소가 변경되었을 가능성
   - 로그인 정보 재확인

4. **DEVELOPMENT_LOG.md 참조**:
   - 개발 과정에서 발생했던 유사한 문제 확인

### 로젠택배 고객센터
- **전화**: 1588-9988
- **운영시간**: 평일 09:00 ~ 18:00

---

## 🔐 보안 주의사항

⚠️ **중요**: `config.json`에는 로그인 정보가 포함되어 있습니다.

**보안 권장사항**:
- ❌ Git에 커밋하지 마세요 (`.gitignore`에 추가됨)
- ✅ 파일 권한을 적절히 설정하세요
- ✅ 다른 사람과 공유할 때 주의하세요
- ✅ 정기적으로 비밀번호를 변경하세요

---

## 📝 라이선스

이 프로젝트는 내부 사용 목적으로 개발되었습니다.

---

## 📌 빠른 링크

- 📖 [상세 사용 가이드](USER_GUIDE.md)
- 📝 [개발 과정 기록](DEVELOPMENT_LOG.md)
- 📦 [requirements.txt](requirements.txt)
- ⚙️ [설정 예시](config.example.json)

---

**버전**: 1.0
**최종 업데이트**: 2025-10-31
**개발 기간**: 2025-10-31 ~ 2025-10-31
