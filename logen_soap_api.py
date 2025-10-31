"""
로젠택배 송장 자동 다운로드 프로그램 (SOAP API 버전)
Fiddler로 분석한 SOAP API를 사용하여 송장 데이터를 자동으로 다운로드합니다.
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
import requests
from typing import Optional, Dict, Any


class LogenSOAPClient:
    """로젠택배 SOAP API 클라이언트"""

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

    def _soap_request(self, url: str, soap_action: str, soap_body: str) -> Optional[str]:
        """
        SOAP 요청을 보냅니다.

        Args:
            url: SOAP 서비스 URL
            soap_action: SOAPAction 헤더 값
            soap_body: SOAP Body XML

        Returns:
            str: 응답 XML 또는 None
        """
        soap_envelope = f'''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <soap:Body>
        {soap_body}
    </soap:Body>
</soap:Envelope>'''

        headers = {
            'Content-Type': 'text/xml; charset=utf-8',
            'SOAPAction': f'"{soap_action}"',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; MS Web Services Client Protocol 2.0.50727.9179)'
        }

        try:
            response = self.session.post(
                url,
                data=soap_envelope.encode('utf-8'),
                headers=headers,
                timeout=self.config['settings']['timeout']
            )

            if response.status_code == 200:
                return response.text
            else:
                self.logger.error(f"SOAP 요청 실패: {response.status_code}")
                self.logger.error(f"응답 내용: {response.text}")
                return None

        except requests.exceptions.RequestException as e:
            self.logger.error(f"네트워크 오류: {e}")
            return None

    def login(self) -> bool:
        """
        로젠택배 SOAP API에 로그인합니다.

        Returns:
            bool: 로그인 성공 여부
        """
        try:
            credentials = self.config['logen_credentials']
            api_config = self.config['api_endpoints']

            login_url = f"{api_config['base_url']}{api_config['login_soap']}"
            soap_action = "http://ilogen.ilogen.com/iLOGEN.COMM.WebService/W_COMM_NTx_LoginEncrypt"

            self.logger.info(f"로그인 시도: {login_url}")

            # SOAP Body 생성
            soap_body = f'''<W_COMM_NTx_LoginEncrypt xmlns="http://ilogen.ilogen.com/iLOGEN.COMM.WebService/">
            <arrParam>
                <string>{credentials['user_id']}</string>
                <string>{credentials['encrypted_password']}</string>
                <string>{credentials['ip_address']}</string>
                <string>{credentials['mac_address']}</string>
            </arrParam>
        </W_COMM_NTx_LoginEncrypt>'''

            response_xml = self._soap_request(login_url, soap_action, soap_body)

            if response_xml:
                self.logger.info("✓ 로그인 성공")
                self.logger.debug(f"응답: {response_xml[:200]}...")
                return True
            else:
                self.logger.error("✗ 로그인 실패")
                return False

        except Exception as e:
            self.logger.error(f"✗ 로그인 중 오류 발생: {e}")
            return False

    def get_invoice_data(self, encrypted_param: str = None) -> Optional[str]:
        """
        송장 데이터를 조회합니다.

        Args:
            encrypted_param: 암호화된 조회 파라미터

        Returns:
            str: 응답 XML 또는 None
        """
        try:
            api_config = self.config['api_endpoints']
            data_url = f"{api_config['base_url']}{api_config['data_soap']}"
            soap_action = "http://ilogen.ilogen.com/iLOGEN.FC.WebService/W_FC0073T_NTx_SelectEnc"

            self.logger.info("송장 데이터 조회 중...")

            # TODO: encrypted_param을 생성하는 방법을 찾아야 함
            # 현재는 Fiddler에서 캡처한 값을 사용해야 함
            if not encrypted_param:
                self.logger.warning("암호화된 파라미터가 필요합니다")
                return None

            soap_body = f'''<W_FC0073T_NTx_SelectEnc xmlns="http://ilogen.ilogen.com/iLOGEN.FC.WebService/">
            <bytDataParam>{encrypted_param}</bytDataParam>
        </W_FC0073T_NTx_SelectEnc>'''

            response_xml = self._soap_request(data_url, soap_action, soap_body)

            if response_xml:
                self.logger.info("✓ 송장 데이터 조회 성공")
                return response_xml
            else:
                self.logger.error("✗ 송장 데이터 조회 실패")
                return None

        except Exception as e:
            self.logger.error(f"✗ 데이터 조회 중 오류 발생: {e}")
            return None

    def run(self) -> bool:
        """
        전체 프로세스를 실행합니다.

        Returns:
            bool: 성공 여부
        """
        self.logger.info("=" * 60)
        self.logger.info("로젠택배 송장 자동 다운로드 시작 (SOAP API)")
        self.logger.info("=" * 60)

        # 1. 로그인
        if not self.login():
            self.logger.error("로그인 실패로 프로세스 중단")
            return False

        # 2. 송장 데이터 조회
        # TODO: 실제 조회 파라미터를 생성하는 로직 필요
        self.logger.info("=" * 60)
        self.logger.info("✓ 로그인 완료!")
        self.logger.info("⚠️  송장 데이터 조회 기능은 추가 분석이 필요합니다.")
        self.logger.info("=" * 60)

        return True


def main():
    """메인 함수"""
    try:
        print("=" * 60)
        print("로젠택배 송장 자동 다운로드 프로그램 (SOAP API)")
        print("=" * 60)
        print()

        # LogenSOAPClient 인스턴스 생성
        client = LogenSOAPClient()

        # 실행
        success = client.run()

        if success:
            print("\n✓ 로그인이 정상적으로 완료되었습니다.")
            print("추가 기능 개발이 필요합니다.")
            return 0
        else:
            print("\n✗ 프로그램 실행 중 오류가 발생했습니다.")
            print("로그 파일을 확인하세요:", client.config['paths']['log_folder'])
            return 1

    except Exception as e:
        print(f"\n✗ 예상치 못한 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
