import os, ssl, json, base64
import pika, requests, getpass
from pathlib import Path
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from hashlib import sha256

BASE_DIR = Path(__file__).resolve().parent
REGISTRY = "https://localhost:8000"
RABBITMQ_HOST = "127.0.0.1"
RABBITMQ_PORT = 5671
CA_PATH = BASE_DIR / "ca.pem"

def generate_keys(username):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    with open(BASE_DIR/f"{username}_private.pem","wb") as f:
        f.write(private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption()
        ))
    with open(BASE_DIR/f"{username}_public.pem","wb") as f:
        f.write(public_key.public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    return private_key, public_key

def load_private_key(username):
    with open(BASE_DIR/f"{username}_private.pem","rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def load_public_key(username):
    with open(BASE_DIR/f"{username}_public.pem","rb") as f:
        return serialization.load_pem_public_key(f.read())

def sign_message(message, private_key):
    h = sha256(message.encode()).digest()
    return base64.b64encode(
        private_key.sign(
            h,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
    ).decode()

def verify_signature(message, signature, public_key):
    h = sha256(message.encode()).digest()
    public_key.verify(
        base64.b64decode(signature),
        h,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )

def encrypt_message(message, public_key):
    return base64.b64encode(
        public_key.encrypt(
            message.encode(),
            padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )
    ).decode()

def decrypt_message(ciphertext, private_key):
    return private_key.decrypt(
        base64.b64decode(ciphertext),
        padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    ).decode()

def register():
    username = input("Choose a username: ")
    password = getpass.getpass("Choose a password: ")

    priv, pub = generate_keys(username)
    response = requests.post(
        f"{REGISTRY}/register",
        json={"username": username, "public_key": pub.public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo).decode()},
        verify=str(CA_PATH)
    )
    print(response.status_code, response.text)
    return username, priv

def login():
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    priv = load_private_key(username)
    return username, priv

def connect_rabbit(username):
    context = ssl._create_unverified_context()
    credentials = pika.PlainCredentials("test_client", "test_client_password")
    params = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        ssl_options=pika.SSLOptions(context),
        credentials=credentials
    )
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=username)
    return connection, channel

def send_message(sender, sender_priv, channel):
    users_resp = requests.get(f"{REGISTRY}/users", verify=str(CA_PATH)).json()
    all_users = users_resp.get("users", [])
    all_users = [u for u in all_users if u != sender]

    if not all_users:
        print("No other registered users found.")
        return

    print("Registered users:")
    for user in all_users:
        print(user)

    recipient = input("Enter recipient username: ")

    if recipient not in all_users:
        print(f"{recipient} is not a registered user.")
        return

    text = input("Message: ")

    # Fetch recipient public key
    recipient_json = requests.get(f"{REGISTRY}/key/{recipient}", verify=str(CA_PATH)).json()
    recipient_pub = serialization.load_pem_public_key(recipient_json['public_key'].encode())

    # Sign-then-Encrypt
    sig = sign_message(text, sender_priv)
    cipher = encrypt_message(text, recipient_pub)

    payload = {"sender": sender, "ciphertext": cipher, "signature": sig, "receiver": recipient}
    channel.basic_publish(exchange="", routing_key=recipient, body=json.dumps(payload))
    print("Message sent!")

def receive_messages(username, priv, channel):
    print("Checking messages...")
    method_frame, header_frame, body = channel.basic_get(queue=username, auto_ack=True)
    if not body:
        print("No messages")
        return
    payload = json.loads(body)
    sender = payload["sender"]
    cipher = payload["ciphertext"]
    sig = payload["signature"]

    message = decrypt_message(cipher, priv)

    sender_pub_json = requests.get(f"{REGISTRY}/key/{sender}", verify=str(CA_PATH)).json()
    sender_pub = serialization.load_pem_public_key(sender_pub_json['public_key'].encode())
    verify_signature(message, sig, sender_pub)

    print(f"Message from {sender}: {message}")

def main():
    choice = input("Register or Login? (r/l): ").lower()
    if choice == "r":
        username, priv = register()
    else:
        username, priv = login()

    connection, channel = connect_rabbit(username)

    while True:
        action = input("Send message (s) / Check messages (c) / Quit (q): ").lower()
        if action == "s":
            send_message(username, priv, channel)
        elif action == "c":
            receive_messages(username, priv, channel)
        elif action == "q":
            break

    connection.close()

if __name__ == "__main__":
    main()
