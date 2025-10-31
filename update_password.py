"""
로젠택배 비밀번호 업데이트 프로그램
- 비밀번호를 입력받아서 암호화하여 저장
- 비밀번호 변경 시마다 이 프로그램을 실행
"""

import getpass
from password_manager import PasswordManager


def main():
    """메인 함수"""
    print("=" * 60)
    print("로젠택배 비밀번호 업데이트")
    print("=" * 60)
    print()

    pm = PasswordManager()

    # 기존 비밀번호 확인
    if pm.is_password_saved():
        print("⚠️  기존에 저장된 비밀번호가 있습니다.")
        print("새로운 비밀번호를 입력하면 덮어씌워집니다.")
        print()

    # 비밀번호 입력
    print("로젠택배 비밀번호를 입력하세요.")
    print("(입력하는 동안 화면에 표시되지 않습니다)")
    print()

    try:
        password = getpass.getpass("비밀번호: ")

        if not password:
            print()
            print("✗ 비밀번호가 입력되지 않았습니다.")
            print()
            input("아무 키나 눌러 종료하세요...")
            return 1

        # 비밀번호 확인
        password_confirm = getpass.getpass("비밀번호 확인: ")

        if password != password_confirm:
            print()
            print("✗ 비밀번호가 일치하지 않습니다.")
            print()
            input("아무 키나 눌러 종료하세요...")
            return 1

        # 비밀번호 저장
        print()
        print("비밀번호를 암호화하여 저장 중...")

        if pm.save_password(password):
            print()
            print("=" * 60)
            print("✓ 비밀번호가 성공적으로 저장되었습니다!")
            print("=" * 60)
            print()
            print("이제 'run_downloader.bat'를 실행하면")
            print("저장된 비밀번호로 자동 실행됩니다.")
            print()
            print("💡 비밀번호 변경 시 다시 이 프로그램을 실행하세요.")
            print()
        else:
            print()
            print("✗ 비밀번호 저장에 실패했습니다.")
            print()

    except KeyboardInterrupt:
        print()
        print()
        print("✗ 사용자가 취소했습니다.")
        print()
        return 1

    except Exception as e:
        print()
        print(f"✗ 오류 발생: {e}")
        print()
        return 1

    input("아무 키나 눌러 종료하세요...")
    return 0


if __name__ == "__main__":
    exit(main())
