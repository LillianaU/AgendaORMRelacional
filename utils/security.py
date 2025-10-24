import hashlib

def hash_password(password: str) -> str:
    """
    Convierte una contraseña en su hash SHA-256.
    
    Args:
        password (str): Contraseña en texto plano
        
    Returns:
        str: Hash SHA-256 de la contraseña
    """
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, password_hash: str) -> bool:
    """
    Verifica si una contraseña coincide con un hash.
    
    Args:
        password (str): Contraseña en texto plano a verificar
        password_hash (str): Hash almacenado para comparar
        
    Returns:
        bool: True si la contraseña coincide, False en caso contrario
    """
    return hash_password(password) == password_hash