import hashlib
import base64
import time
import os 
import bcrypt

def salt_vs_unsalt_demo():
    password = "password123"
    dictionary = ["123456", "password", "password123", "admin", "654321", "11111111", "qwerty"]
    
    unsalted_hash_password = hashlib.sha256(password.encode()).hexdigest()
    
    start = time.time()
    for word in dictionary:
        guess = hashlib.sha256(word.encode()).hexdigest()
        if guess == unsalted_hash_password:
            print(f"found unsalted password in {(time.time()-start):.9f}s")


    # salted
    salt = base64.b64encode(os.urandom(16)).decode('utf-8')
    salted_input = password + salt
    salted_hash = hashlib.sha256(salted_input.encode()).hexdigest()
    start = time.time()
    for word in dictionary:
        guess = hashlib.sha256(word.encode()).hexdigest()  
        if guess == salted_hash:
            print(f"found salted password in {(time.time()-start):.9f}s")

def slow_vs_fast_hash_demo():
    password = "password123"
    # SHA256
    start_sha = time.time()
    sha256_result = hashlib.sha256(password.encode()).hexdigest()
    end_sha = time.time()
    sha256_time = end_sha - start_sha

    # bcrypt
    start_bcrypt = time.time()
    bcrypt_result = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
    end_bcrypt = time.time()
    bcrypt_time = end_bcrypt - start_bcrypt

    print("=== Performance Comparison ===")
    print(f"SHA-256 Hash Time: {sha256_time:.9f} seconds")
    print(f"bcrypt Hash Time: {bcrypt_time:.9f} seconds")
	
if __name__ == '__main__':
    salt_vs_unsalt_demo()

    slow_vs_fast_hash_demo()