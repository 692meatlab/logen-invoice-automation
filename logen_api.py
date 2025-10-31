"""
로젠택배 송장 자동 다운로드 프로그램
Fiddler로 분석한 API를 사용하여 송장 데이터를 자동으로 다운로드합니다.
"""

import os
import json
import logging
import getpass
from datetime import datetime
from pathlib import Path
import requests
from typing import Optional, Dict, Any


class LogenInvoiceDownloader:
    """로젠택배 송장 데이터를 자동으로 다운로드하는 클래스"""

    def __init__(self, config_path: str = None):
        """
        Args:
            config_path: config.json 파일 경로 (기본값: 스크립트와 같은 폴더)
        """
        # 설정 파일 경로 설정
        if config_path is None:
            script_dir = Path(__file__).parent.absolute()
            config_path = script_dir / "config.json"

        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.session = requests.Session()

        # 로깅 설정
        self._setup_logging()

    def _load_config(self) -> Dict[str, Any]:
        """config.json 파일을 로드합니다."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # 필수 폴더 생성
            Path(config['paths']['download_folder']).mkdir(parents=True, exist_ok=True)
            Path(config['paths']['log_folder']).mkdir(parents=True, exist_ok=True)

            return config
        except FileNotFoundError:
            raise FileNotFoundError(
                f"설정 파일을 찾을 수 없습니다: {self.config_path}\n"
                f"config.example.json을 복사하여 config.json을 만들고 설정을 입력하세요."
            )
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON 파싱 오류: {e}")

    def _setup_logging(self):
        """로깅을 설정합니다."""
        log_folder = Path(self.config['paths']['log_folder'])
        log_file = log_folder / f"logen_{datetime.now():%Y%m%d}.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def login(self, password: str) -> bool:
        """
        로젠택배 API에 로그인합니다.

        Args:
            password: 로젠택배 비밀번호 (실행 시 입력받음)

        Returns:
            bool: 로그인 성공 여부
        """
        try:
            credentials = self.config['logen_credentials']
            api_config = self.config['api_endpoints']

            login_url = f"{api_config['base_url']}{api_config['login']}"

            self.logger.info(f"로그인 시도: {login_url}")

            # TODO: Fiddler 분석 후 실제 요청 형식으로 수정 필요
            # 아래는 예시입니다. 실제 API에 맞게 수정하세요.
            response = self.session.post(
                login_url,
                json={
                    "id": credentials['user_id'],
                    "pw": password  # 입력받은 비밀번호 사용
                },
                timeout=self.config['settings']['timeout']
            )

            if response.status_code == 200:
                self.logger.info("✓ 로그인 성공")
                return True
            else:
                self.logger.error(f"✗ 로그인 실패: {response.status_code}")
                self.logger.error(f"응답 내용: {response.text}")
                return False

        except requests.exceptions.RequestException as e:
            self.logger.error(f"✗ 네트워크 오류: {e}")
            return False

    def get_today_invoices(self) -> Optional[Dict[str, Any]]:
        """
        오늘 발송된 송장 목록을 가져옵니다.

        Returns:
            dict: 송장 데이터 (JSON 형식) 또는 None
        """
        try:
            api_config = self.config['api_endpoints']
            invoices_url = f"{api_config['base_url']}{api_config['invoices']}"

            today = datetime.now().strftime(self.config['settings']['date_format'])

            self.logger.info(f"송장 데이터 조회 중... (날짜: {today})")

            # TODO: Fiddler 분석 후 실제 요청 형식으로 수정 필요
            response = self.session.get(
                invoices_url,
                params={
                    "date": today,
                    "status": "printed"  # 송장출력 완료된 것만
                },
                timeout=self.config['settings']['timeout']
            )

            if response.status_code == 200:
                data = response.json()
                self.logger.info(f"✓ 송장 데이터 조회 성공 ({len(data)} 건)")
                return data
            else:
                self.logger.error(f"✗ 송장 데이터 조회 실패: {response.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            self.logger.error(f"✗ 네트워크 오류: {e}")
            return None

    def download_excel(self) -> Optional[str]:
        """
        송장 데이터를 엑셀 파일로 다운로드합니다.

        Returns:
            str: 다운로드된 파일 경로 또는 None
        """
        try:
            api_config = self.config['api_endpoints']
            excel_url = f"{api_config['base_url']}{api_config['excel_download']}"

            today = datetime.now().strftime(self.config['settings']['date_format'])

            self.logger.info("엑셀 파일 다운로드 중...")

            # TODO: Fiddler 분석 후 실제 요청 형식으로 수정 필요
            response = self.session.get(
                excel_url,
                params={"date": today},
                timeout=self.config['settings']['timeout']
            )

            if response.status_code == 200:
                # 파일 저장
                download_folder = Path(self.config['paths']['download_folder'])
                filename = f"logen_invoices_{datetime.now():%Y%m%d_%H%M%S}.{self.config['settings']['download_format']}"
                file_path = download_folder / filename

                with open(file_path, 'wb') as f:
                    f.write(response.content)

                self.logger.info(f"✓ 엑셀 다운로드 완료: {file_path}")
                return str(file_path)
            else:
                self.logger.error(f"✗ 엑셀 다운로드 실패: {response.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            self.logger.error(f"✗ 네트워크 오류: {e}")
            return None
        except IOError as e:
            self.logger.error(f"✗ 파일 저장 오류: {e}")
            return None

    def run(self, password: str) -> bool:
        """
        전체 프로세스를 실행합니다.

        Args:
            password: 로젠택배 비밀번호

        Returns:
            bool: 성공 여부
        """
        self.logger.info("=" * 60)
        self.logger.info("로젠택배 송장 자동 다운로드 시작")
        self.logger.info("=" * 60)

        # 1. 로그인
        if not self.login(password):
            self.logger.error("로그인 실패로 프로세스 중단")
            return False

        # 2. 송장 데이터 조회 (선택사항)
        invoices = self.get_today_invoices()
        if invoices:
            self.logger.info(f"조회된 송장 건수: {len(invoices)}")

        # 3. 엑셀 다운로드
        file_path = self.download_excel()
        if file_path:
            self.logger.info("=" * 60)
            self.logger.info(f"✓ 모든 작업 완료!")
            self.logger.info(f"다운로드 파일: {file_path}")
            self.logger.info("=" * 60)
            return True
        else:
            self.logger.error("엑셀 다운로드 실패")
            return False


def main():
    """메인 함수"""
    try:
        # LogenInvoiceDownloader 인스턴스 생성
        downloader = LogenInvoiceDownloader()

        # 비밀번호 입력받기
        print("=" * 60)
        print("로젠택배 송장 자동 다운로드 프로그램")
        print("=" * 60)
        print(f"업체 아이디: {downloader.config['logen_credentials']['user_id']}")

        # getpass를 사용하면 입력 시 화면에 표시되지 않음
        password = getpass.getpass("비밀번호 입력: ")

        if not password:
            print("\n✗ 비밀번호가 입력되지 않았습니다.")
            return 1

        # 실행
        success = downloader.run(password)

        if success:
            print("\n✓ 프로그램이 정상적으로 완료되었습니다.")
            return 0
        else:
            print("\n✗ 프로그램 실행 중 오류가 발생했습니다.")
            print("로그 파일을 확인하세요:", downloader.config['paths']['log_folder'])
            return 1

    except Exception as e:
        print(f"\n✗ 예상치 못한 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
