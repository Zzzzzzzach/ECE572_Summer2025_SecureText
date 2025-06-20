#!/usr/bin/env python3
"""
Author: Ardeshir S.
Course: ECE 572; Summer 2025
SecureText Console Messenger (Insecure Genesis Version)
A basic console-based messenger application with intentional security vulnerabilities.

Features:
- Account creation with plaintext password storage
- User login
- Send/receive messages via TCP sockets
- Basic password reset functionality
"""

import socket
import threading
import json
import os
import sys
import time
from datetime import datetime
import hashlib
import bcrypt
import base64

HASH_METHOD = "bcrypt"

SHARED_KEY = b'this_is_a_secret_shared_key'

class SecureTextServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.users_file = 'users.json'
        self.users = self.load_users()
        self.active_connections = {}  # username -> connection
        self.server_socket = None

    @staticmethod
    def generate_salt():
        return base64.b64encode(os.urandom(16)).decode('utf-8')
    @staticmethod
    def generate_mac(message: str) -> str:
        return hashlib.md5(SHARED_KEY + message.encode('utf-8')).hexdigest()
    
    def verify_mac(self, message: str, mac: str) -> bool:
        return self.generate_mac(message) == mac

    def hash_password(self, password, salt, method=HASH_METHOD) -> str:
        if method == "sha256":
            return hashlib.sha256(password.encode('utf-8')).hexdigest()
        elif method == "bcrypt":
            password = password+salt
            return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')
        else:
            return password

    def verify_password(self, password, stored_hash, salt, method=HASH_METHOD) -> bool:
        print(f"{password} , {stored_hash}, {method}")
        if method == "sha256":
            return hashlib.sha256(password.encode('utf-8')).hexdigest() == stored_hash
        elif method == "bcrypt":
            password = password+salt
            return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
        else:
            return password == stored_hash

    def load_users(self):
        """Load users from JSON file or create empty dict if file doesn't exist"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                print(f"Warning: Could not load {self.users_file}, starting with empty user database")
        return {}
    
    def save_users(self):
        """Save users to JSON file with plaintext passwords (INSECURE!)"""
        try:
            with open(self.users_file, 'w') as f:
                json.dump(self.users, f, indent=2)
        except IOError as e:
            print(f"Error saving users: {e}")
    
    def create_account(self, username, password):
        """Create new user account - stores password in PLAINTEXT!"""
        if username in self.users:
            return False, "Username already exists"
        salt = self.generate_salt()

        # start = time.time()
        hashed_pw = self.hash_password(password, salt, HASH_METHOD)
        # interval = time.time()-start

        # print(f'{HASH_METHOD} costs {interval} seconds to complete.')
#       sha256 costs 3.0994415283203125e-05 seconds to complete.
#       sha256 costs 2.4080276489257812e-05 seconds to complete.
#       sha256 costs 1.6927719116210938e-05 seconds to complete.
#       sha256 costs 1.5974044799804688e-05 seconds to complete.
#       sha256 costs 2.47955322265625e-05 seconds to complete.

#       bcrypt costs 0.21899008750915527 seconds to complete.
#       bcrypt costs 0.21755099296569824 seconds to complete.
#       bcrypt costs 0.21746587753295898 seconds to complete.
#       bcrypt costs 0.21658706665039062 seconds to complete.
#       bcrypt costs 0.21867704391479492 seconds to complete.

        # SECURITY VULNERABILITY: Storing password in plaintext!
        self.users[username] = {
            'password': hashed_pw,  # PLAINTEXT PASSWORD!
            'hash_method': HASH_METHOD,
            'salt': salt,
            'created_at': datetime.now().isoformat(),
            'reset_question': 'What is your favorite color?',
            'reset_answer': 'blue'  # Default for simplicity
        }
        self.save_users()
        return True, "Account created successfully"
    
    def authenticate(self, username, password):
        """Authenticate user with plaintext password comparison"""
        if username not in self.users:
            return False, "Username not found"
        
        if self.verify_password(password, self.users[username]['password'], self.users[username].get('salt'), self.users[username].get("hash_method", "plaintext")):
            if self.users[username].get('hash_method') == None :
                self.migrate_plaintext_user(username, password)
            return True, "Authentication successful"
        else:
            return False, "Invalid password"

    def migrate_plaintext_user(self, username, password):
        salt = self.generate_salt()
        hashed_pw = self.hash_password(password, salt, HASH_METHOD)

        self.users[username]['password'] = hashed_pw
        self.users[username]['salt'] = salt
        self.users[username]['hash_method'] = HASH_METHOD
        self.save_users()
    
    def reset_password(self, username, new_password):
        """Basic password reset - just requires existing username"""
        if username not in self.users:
            return False, "Username not found"
        
        salt = self.users[username].get('salt')
        if not salt:
            salt = self.generate_salt()
            self.user[username]['salt'] = salt
        hashed_pw = self.hash_password(new_password, salt,HASH_METHOD)

        self.users[username]['password'] = hashed_pw
        self.users[username]['hash_method'] = HASH_METHOD
        self.save_users()
        return True, "Password reset successful"
    
    def handle_client(self, conn, addr):
        """Handle individual client connection"""
        print(f"New connection from {addr}")
        current_user = None
        
        try:
            while True:
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    break
                
                try:
                    message = json.loads(data)
                    command = message.get('command')
                    
                    if command == 'CREATE_ACCOUNT':
                        username = message.get('username')
                        password = message.get('password')
                        success, msg = self.create_account(username, password)
                        response = {'status': 'success' if success else 'error', 'message': msg}
                        
                    elif command == 'LOGIN':
                        username = message.get('username')
                        password = message.get('password')
                        success, msg = self.authenticate(username, password)
                        if success:
                            current_user = username
                            self.active_connections[username] = conn
                        response = {'status': 'success' if success else 'error', 'message': msg}
                        
                    elif command == 'SEND_MESSAGE':
                        if not current_user:
                            response = {'status': 'error', 'message': 'Not logged in'}
                        else:
                            recipient = message.get('recipient')
                            msg_content = message.get('content')
                            
                            # Send message to recipient if they're online
                            if recipient in self.active_connections:
                                msg_data = {
                                    'type': 'MESSAGE',
                                    'from': current_user,
                                    'content': msg_content,
                                    'mac': message.get('mac'),
                                    'timestamp': datetime.now().isoformat()
                                }
                                try:
                                    self.active_connections[recipient].send(
                                        json.dumps(msg_data).encode('utf-8')
                                    )
                                    response = {'status': 'success', 'message': 'Message sent'}
                                except:
                                    # Remove inactive connection
                                    del self.active_connections[recipient]
                                    response = {'status': 'error', 'message': 'Recipient is offline'}
                            else:
                                response = {'status': 'error', 'message': 'Recipient is offline'}
                    
                    elif command == 'RESET_PASSWORD':
                        username = message.get('username')
                        new_password = message.get('new_password')
                        success, msg = self.reset_password(username, new_password)
                        response = {'status': 'success' if success else 'error', 'message': msg}
                        
                    elif command == 'LIST_USERS':
                        if not current_user:
                            response = {'status': 'error', 'message': 'Not logged in'}
                        else:
                            online_users = list(self.active_connections.keys())
                            all_users = list(self.users.keys())
                            response = {
                                'status': 'success', 
                                'online_users': online_users,
                                'all_users': all_users
                            }
                    
                    else:
                        response = {'status': 'error', 'message': 'Unknown command'}
                    
                    conn.send(json.dumps(response).encode('utf-8'))
                    
                except json.JSONDecodeError:
                    error_response = {'status': 'error', 'message': 'Invalid JSON'}
                    conn.send(json.dumps(error_response).encode('utf-8'))
                    
        except ConnectionResetError:
            pass
        finally:
            # Clean up connection
            if current_user and current_user in self.active_connections:
                del self.active_connections[current_user]
            conn.close()
            print(f"Connection from {addr} closed")
    
    def start_server(self):
        """Start the TCP server"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f"SecureText Server started on {self.host}:{self.port}")
            print("Waiting for connections...")
            
            while True:
                conn, addr = self.server_socket.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                client_thread.daemon = True
                client_thread.start()
                
        except KeyboardInterrupt:
            print("\nServer shutting down...")
        finally:
            if self.server_socket:
                self.server_socket.close()

class SecureTextClient:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.socket = None
        self.logged_in = False
        self.username = None
        self.running = False
        self.last_command_response = None
        self.response_event = threading.Event()

    @staticmethod
    def generate_mac(message: str) -> str:
        return hashlib.md5(SHARED_KEY + message.encode('utf-8')).hexdigest()
    
    def verify_mac(self, message: str, mac: str) -> bool:
        return self.generate_mac(message) == mac

    def connect(self):
        """Connect to the server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            threading.Thread(target=self.listen_for_messages, daemon=True).start()

            return True
        except ConnectionRefusedError:
            print("Error: Could not connect to server. Make sure the server is running.")
            return False
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    def send_command(self, command_data):
        """Send command to server and get response"""
        try:
            self.socket.send(json.dumps(command_data).encode('utf-8'))
            if self.response_event.wait(timeout=5):  # wait max 5 seconds
                print(self.last_command_response)
                response = self.last_command_response
                self.last_command_response = None
                self.response_event.clear()
                return response
            # response = self.socket.recv(1024).decode('utf-8')
            # return json.loads(response)
        except Exception as e:
            print(f"Communication error: {e}")
            return {'status': 'error', 'message': 'Communication failed'}
    
    def listen_for_messages(self):
        """Listen for incoming messages in a separate thread"""
        while True:
            try:
                data = self.socket.recv(1024).decode('utf-8')
                if data:
                    message = json.loads(data)
                    print(f"listen received message {message}")
                    if self.username != None and message.get('type') == 'MESSAGE' and message.get('mac'):
                        if not self.verify_mac(message['content'], message.get('mac')):
                            print("mac not match")
                            print(f"{mac}, {self.generate_mac(message['content'])}")
                        else:
                            print(f"\n[{message['timestamp']}] {message['from']}: {message['content']}")
                            print(">> ", end="", flush=True)
                    else:
                        print('?????')
                        self.last_command_response = message
                        self.response_event.set()
            except Exception as e:
                print("Error generating MAC:", e)
                break
    
    def create_account(self):
        """Create a new account"""
        print("\n=== Create Account ===")
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        
        if not username or not password:
            print("Username and password cannot be empty!")
            return
        
        command = {
            'command': 'CREATE_ACCOUNT',
            'username': username,
            'password': password
        }
        
        response = self.send_command(command)
        print(f"{response['message']}")
    
    def login(self):
        """Login to the system"""
        print("\n=== Login ===")
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        
        command = {
            'command': 'LOGIN',
            'username': username,
            'password': password
        }
        
        response = self.send_command(command)
        print(f"{response['message']}")
        
        if response['status'] == 'success':
            self.logged_in = True
            self.username = username
            self.running = True
    
    def send_message(self):
        """Send a message to another user"""
        if not self.logged_in:
            print("You must be logged in to send messages!")
            return
        
        print("\n=== Send Message ===")
        recipient = input("Enter recipient username: ").strip()
        content = input("Enter message: ").strip()
        mac = self.generate_mac(content)
        if not recipient or not content:
            print("Recipient and message cannot be empty!")
            return
        
        command = {
            'command': 'SEND_MESSAGE',
            'recipient': recipient,
            'content': content,
            'mac': mac
        }
        
        response = self.send_command(command)
        print(f"{response['message']}")
    
    def list_users(self):
        """List all users and show who's online"""
        if not self.logged_in:
            print("You must be logged in to list users!")
            return
        
        command = {'command': 'LIST_USERS'}
        response = self.send_command(command)
        
        if response['status'] == 'success':
            print(f"\nOnline users: {', '.join(response['online_users'])}")
            print(f"All users: {', '.join(response['all_users'])}")
        else:
            print(f"Error: {response['message']}")
    
    def reset_password(self):
        """Reset password (basic implementation)"""
        print("\n=== Reset Password ===")
        username = input("Enter username: ").strip()
        new_password = input("Enter new password: ").strip()
        
        command = {
            'command': 'RESET_PASSWORD',
            'username': username,
            'new_password': new_password
        }
        
        response = self.send_command(command)
        print(f"{response['message']}")
    
    def run(self):
        """Main client loop"""
        if not self.connect():
            return
        
        print("=== SecureText Messenger (Insecure Version) ===")
        print("WARNING: This is an intentionally insecure implementation for educational purposes!")
        
        while True:
            if not self.logged_in:
                print("\n1. Create Account")
                print("2. Login")
                print("3. Reset Password")
                print("4. Exit")
                choice = input("Choose an option: ").strip()
                
                if choice == '1':
                    self.create_account()
                elif choice == '2':
                    self.login()
                elif choice == '3':
                    self.reset_password()
                elif choice == '4':
                    break
                else:
                    print("Invalid choice!")
            else:
                print(f"\nLogged in as: {self.username}")
                print("1. Send Message")
                print("2. List Users")
                print("3. Logout")
                choice = input("Choose an option (or just press Enter to wait for messages): ").strip()
                
                if choice == '1':
                    self.send_message()
                elif choice == '2':
                    self.list_users()
                elif choice == '3':
                    self.logged_in = False
                    self.running = False
                    self.username = None
                    print("Logged out successfully")
                elif choice == '':
                    # Just wait for messages
                    print("Waiting for messages... (press Enter to show menu)")
                    input()
                else:
                    print("Invalid choice!")
        
        if self.socket:
            self.socket.close()
        print("Goodbye!")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'server':
        # Run as server
        server = SecureTextServer()
        server.start_server()
    else:
        # Run as client
        client = SecureTextClient()
        client.run()

if __name__ == "__main__":
    main()
