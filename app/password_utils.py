"""
Fixed password hashing utilities for FastAPI
Works with bcrypt 4.x versions
"""
import bcrypt


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt directly (not passlib)
    
    Args:
        password: Plain text password to hash
        
    Returns:
        Hashed password as string
        
    Note:
        bcrypt has a 72-byte limit. For longer passwords,
        we truncate to 72 bytes (which is ~72 characters for ASCII)
    """
    # Truncate password if needed (bcrypt has 72 byte limit)
    password_bytes = password.encode('utf-8')[:72]
    
    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Return as string
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to compare against
        
    Returns:
        True if password matches, False otherwise
    """
    # Truncate password if needed (same as when hashing)
    password_bytes = plain_password.encode('utf-8')[:72]
    hashed_bytes = hashed_password.encode('utf-8')
    
    try:
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception as e:
        # Handle any bcrypt errors gracefully
        print(f"Password verification error: {e}")
        return False


# Test the functions if run directly
if __name__ == "__main__":
    # Test hashing
    test_password = "mySecurePassword123"
    hashed = hash_password(test_password)
    print(f"Original: {test_password}")
    print(f"Hashed: {hashed}")
    
    # Test verification
    is_valid = verify_password(test_password, hashed)
    print(f"Verification: {is_valid}")
    
    # Test with wrong password
    is_invalid = verify_password("wrongPassword", hashed)
    print(f"Wrong password: {is_invalid}")
