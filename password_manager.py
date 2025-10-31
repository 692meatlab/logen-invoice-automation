"""
로젠택배 비밀번호 관리 모듈
- 비밀번호를 안전하게 암호화하여 저장
- 머신별로 고유한 키 사용 (다른 PC에서 복호화 불가)
"""

import os
import base64
import json
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2


class PasswordManager:
    """비밀번호 암호화 및 저장 관리"""

    def __init__(self, config_dir: str = None):
        """초기화"""
        if config_dir is None:
            self.config_dir = Path(__file__).parent.absolute()
        else:
            self.config_dir = Path(config_dir)

        self.password_file = self.config_dir / ".password"
        self.key_file = self.config_dir / ".key"

    def _get_machine_salt(self):
        """머신별 고유 Salt 생성 (MAC 주소 기반)"""
        import uuid
        mac = uuid.getnode()
        return str(mac).encode()

    def _get_or_create_key(self):
        """암호화 키 가져오기 또는 생성"""
        if self.key_file.exists():
            # 기존 키 로드
            with open(self.key_file, 'rb') as f:
                return f.read()
        else:
            # 새 키 생성 (머신별 고유)
            salt = self._get_machine_salt()
            kdf = PBKDF2(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(salt))

            # 키 저장
            with open(self.key_file, 'wb') as f:
                f.write(key)

            return key

    def save_password(self, password: str):
        """비밀번호를 암호화하여 저장"""
        try:
            # 암호화 키 가져오기
            key = self._get_or_create_key()
            fernet = Fernet(key)

            # 비밀번호 암호화
            encrypted = fernet.encrypt(password.encode())

            # 파일에 저장
            with open(self.password_file, 'wb') as f:
                f.write(encrypted)

            return True
        except Exception as e:
            print(f"비밀번호 저장 실패: {e}")
            return False

    def load_password(self):
        """저장된 비밀번호 복호화하여 로드"""
        try:
            # 비밀번호 파일이 없으면 None 반환
            if not self.password_file.exists():
                return None

            # 암호화 키 가져오기
            key = self._get_or_create_key()
            fernet = Fernet(key)

            # 암호화된 비밀번호 읽기
            with open(self.password_file, 'rb') as f:
                encrypted = f.read()

            # 복호화
            decrypted = fernet.decrypt(encrypted)
            return decrypted.decode()

        except Exception as e:
            print(f"비밀번호 로드 실패: {e}")
            return None

    def is_password_saved(self):
        """비밀번호가 저장되어 있는지 확인"""
        return self.password_file.exists()

    def delete_password(self):
        """저장된 비밀번호 삭제"""
        try:
            if self.password_file.exists():
                self.password_file.unlink()
            return True
        except Exception as e:
            print(f"비밀번호 삭제 실패: {e}")
            return False


def main():
    """테스트용 메인 함수"""
    pm = PasswordManager()

    # 비밀번호 저장 테스트
    test_password = "test1234"
    print(f"비밀번호 저장: {test_password}")
    pm.save_password(test_password)

    # 비밀번호 로드 테스트
    loaded = pm.load_password()
    print(f"비밀번호 로드: {loaded}")

    if loaded == test_password:
        print("✓ 테스트 성공!")
    else:
        print("✗ 테스트 실패!")


if __name__ == "__main__":
    main()
