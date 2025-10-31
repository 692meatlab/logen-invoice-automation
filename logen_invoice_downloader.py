"""
로젠택배 송장 자동 다운로드 프로그램
- SOAP API 호출
- 암호화된 데이터 복호화
- 엑셀 파일로 저장
"""

import os
import json
import logging
import base64
import re
from datetime import datetime
from pathlib import Path
import requests
import pandas as pd
import clr
import sys

# .NET DLL 경로 추가
ILOGEN_DLL_PATH = r'C:\iLOGEN\BIN'
sys.path.append(ILOGEN_DLL_PATH)

from System.Reflection import Assembly
from System import Array, Byte, Activator


class LogenInvoiceDownloader:
    """로젠택배 송장 다운로더"""

    def __init__(self, config_path: str = None):
        """초기화"""
        if config_path is None:
            script_dir = Path(__file__).parent.absolute()
            config_path = script_dir / "config.json"

        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.session = requests.Session()
        self._setup_logging()
        self._setup_decryptor()

    def _load_config(self):
        """설정 파일 로드"""
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

    def _setup_logging(self):
        """로깅 설정"""
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

    def _setup_decryptor(self):
        """복호화 DLL 로드"""
        try:
            os.chdir(ILOGEN_DLL_PATH)
            asm = Assembly.LoadFrom(os.path.join(ILOGEN_DLL_PATH, 'Logen.Framework.BaseUtil.dll'))
            encrypt_seed_type = asm.GetType('Logen.Framework.BaseUtil.EncryptSeed')
            self.decryptor = Activator.CreateInstance(encrypt_seed_type)
            self.logger.info("복호화 DLL 로드 성공")
        except Exception as e:
            self.logger.error(f"복호화 DLL 로드 실패: {e}")
            raise

    def _soap_request(self, url: str, soap_action: str, soap_body: str):
        """SOAP 요청"""
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

    def login(self):
        """로그인"""
        try:
            credentials = self.config['logen_credentials']
            api_config = self.config['api_endpoints']

            login_url = f"{api_config['base_url']}{api_config['login_soap']}"
            soap_action = "http://ilogen.ilogen.com/iLOGEN.COMM.WebService/W_COMM_NTx_LoginEncrypt"

            self.logger.info(f"로그인 시도: {login_url}")

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
                return True
            else:
                self.logger.error("✗ 로그인 실패")
                return False

        except Exception as e:
            self.logger.error(f"✗ 로그인 중 오류 발생: {e}")
            return False

    def get_invoice_data(self, encrypted_param: str):
        """송장 데이터 조회"""
        try:
            api_config = self.config['api_endpoints']
            data_url = f"{api_config['base_url']}{api_config['data_soap']}"
            soap_action = "http://ilogen.ilogen.com/iLOGEN.FC.WebService/W_FC0073T_NTx_SelectEnc"

            self.logger.info("송장 데이터 조회 중...")

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

    def decrypt_data(self, encrypted_base64: str):
        """데이터 복호화"""
        try:
            self.logger.info("데이터 복호화 중...")

            # Base64 디코딩
            encrypted_bytes = base64.b64decode(encrypted_base64)
            self.logger.info(f"Base64 디코딩 완료: {len(encrypted_bytes)} bytes")

            # .NET byte array로 변환
            net_bytes = Array[Byte](encrypted_bytes)

            # 복호화
            dataset = self.decryptor.SetDecrypt(net_bytes)

            self.logger.info(f"✓ 복호화 완료: {dataset.Tables.Count}개 테이블")

            return dataset

        except Exception as e:
            self.logger.error(f"✗ 복호화 실패: {e}")
            return None

    def save_to_excel(self, dataset, filename: str = None):
        """DataSet을 엑셀로 저장"""
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"logen_invoices_{timestamp}.xlsx"

            download_folder = Path(self.config['paths']['download_folder'])
            file_path = download_folder / filename

            # 데이터가 있는 테이블 찾기 (보통 Table 2 - DT6)
            main_table = None
            for i in range(dataset.Tables.Count):
                table = dataset.Tables[i]
                if table.Rows.Count > 0:
                    main_table = table
                    self.logger.info(f"데이터 테이블 발견: {table.TableName} ({table.Rows.Count} rows)")
                    break

            if not main_table:
                self.logger.error("데이터가 없습니다")
                return None

            # DataFrame으로 변환
            data = []
            columns = [col.ColumnName for col in main_table.Columns]

            for row in main_table.Rows:
                row_data = []
                for col in main_table.Columns:
                    value = row[col.ColumnName]
                    if value is None or str(value) == '':
                        row_data.append(None)
                    else:
                        row_data.append(str(value))
                data.append(row_data)

            df = pd.DataFrame(data, columns=columns)

            # 엑셀로 저장
            df.to_excel(file_path, index=False, engine='openpyxl')

            self.logger.info(f"✓ 엑셀 파일 저장 완료: {file_path}")
            return str(file_path)

        except Exception as e:
            self.logger.error(f"✗ 엑셀 저장 실패: {e}")
            return None

    def run(self, encrypted_param: str):
        """전체 프로세스 실행"""
        self.logger.info("=" * 60)
        self.logger.info("로젠택배 송장 자동 다운로드 시작")
        self.logger.info("=" * 60)

        # 1. 로그인
        if not self.login():
            self.logger.error("로그인 실패로 프로세스 중단")
            return False

        # 2. 송장 데이터 조회
        response_xml = self.get_invoice_data(encrypted_param)
        if not response_xml:
            return False

        # 3. 응답에서 암호화된 데이터 추출
        match = re.search(
            r'<W_FC0073T_NTx_SelectEncResult>(.*?)</W_FC0073T_NTx_SelectEncResult>',
            response_xml,
            re.DOTALL
        )

        if not match:
            self.logger.error("응답에서 데이터를 찾을 수 없습니다")
            return False

        encrypted_base64 = match.group(1).strip()

        # 4. 복호화
        dataset = self.decrypt_data(encrypted_base64)
        if not dataset:
            return False

        # 5. 엑셀로 저장
        excel_file = self.save_to_excel(dataset)
        if not excel_file:
            return False

        self.logger.info("=" * 60)
        self.logger.info("✓ 모든 작업 완료!")
        self.logger.info(f"다운로드 파일: {excel_file}")
        self.logger.info("=" * 60)

        return True


def main():
    """메인 함수"""
    try:
        print("=" * 60)
        print("로젠택배 송장 자동 다운로드 프로그램")
        print("=" * 60)
        print()

        # 다운로더 인스턴스 생성
        downloader = LogenInvoiceDownloader()

        # TODO: 실제 조회 파라미터를 생성하는 로직 필요
        # 현재는 test.txt에서 가져온 샘플 파라미터 사용
        encrypted_param = "Z/nY+cZ3l4Da0g3Y7trY5OolaKE/unqq/ClhGzkCGqfbli7a47CoTIDU3uTjpJkojBR+Cw1ZjxrWWjHkVzF45+2X6ZAuNdnq+MgDCaHfjVNp1POQdKnB7JbO0YRoUBPFnMEmnWqXGebWGGiLKFskkblegkHsO78eG8ZpVlg6s/pApj/T7B7+8hycXPX8IiviP8yHVY65D/ZOfzMv/m+oXWzROpe6Tg08K2yNX2jJvaxB6cuMexm/ZBgfEzPJzxw6ioR4ybWHA9OkFXr5QTfyQuOgEZFl94NdrnaiFygQ+HQJBFoXwydthJNc0ezIMfcKdD7SxkxDPYbwKodQE3Ysv/UPSjV9oqYN4/Uo9HffeFSEi6rJddkXzFWELfo+tAfVypbkV8iJZdDt/07/203krH+tEEtaivtn/OlnzoV9XXAg4TBGVXbzpSfjFCjOIYL8"

        # 실행
        success = downloader.run(encrypted_param)

        if success:
            print("\n✓ 프로그램이 정상적으로 완료되었습니다.")
            return 0
        else:
            print("\n✗ 프로그램 실행 중 오류가 발생했습니다.")
            print(f"로그 파일을 확인하세요: {downloader.config['paths']['log_folder']}")
            return 1

    except Exception as e:
        print(f"\n✗ 예상치 못한 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
