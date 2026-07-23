from pwdlib import PasswordHash

code_hasher = PasswordHash.recommended()

def check_code(code: str, code_hash: str) -> bool:
    try:
        return code_hasher.verify(code, code_hash)
    except Exception:
        return False

def generate_code_hash(code: str) -> str:
    return code_hasher.hash(code)
