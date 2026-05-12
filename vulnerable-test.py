import subprocess
import pickle

def get_user(username):
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchone()

def run_command(user_input):
    cmd = "ping -c 4 " + user_input
    return subprocess.check_output(cmd, shell=True)

def load_data(raw_bytes):
    return pickle.loads(raw_bytes)

API_KEY = "sk-proj-ABCDEFGHIJKLMNOP123456789"
