"""
Code Review Agent - Test Suite
This file contains 12 deliberately vulnerable and safe code patterns
across multiple security categories for testing the LLM-based code reviewer.
"""

import subprocess
import pickle
import yaml
import os
import json


# ==================== VULNERABLE ====================

def get_user_by_name(username):
    """CWE-89: SQL Injection - direct string concatenation"""
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchone()


def search_products(keyword):
    """CWE-89: SQL Injection - f-string in execute"""
    cursor.execute(f"SELECT * FROM products WHERE title LIKE '%{keyword}%'")
    return cursor.fetchall()


def ping_host(hostname):
    """CWE-78: Command Injection - shell=True with user input"""
    cmd = "ping -c 4 " + hostname
    return subprocess.check_output(cmd, shell=True)


def read_log_file(filename):
    """CWE-78: Command Injection - os.system with concatenation"""
    return os.system("cat /var/log/" + filename)


def load_user_session(raw_bytes):
    """CWE-502: Insecure Deserialization - pickle on untrusted data"""
    user_obj = pickle.loads(raw_bytes)
    return user_obj


def load_config(yaml_data):
    """CWE-502: Insecure Deserialization - yaml.load without SafeLoader"""
    config = yaml.load(yaml_data)
    return config


def download_file(filename):
    """CWE-22: Path Traversal - user-controlled path"""
    filepath = "/var/uploads/" + filename
    with open(filepath, "r") as f:
        return f.read()


def buffer_copy_unsafe(user_input):
    """CWE-120: Buffer Overflow simulation (Python doesn't have buffers,
    but this represents an unsafe pattern for demonstration)"""
    result = "x" * 1000000 + user_input
    return result


# Hardcoded credentials section (CWE-798)
API_KEY = "sk-proj-ABCDEFGHIJKLMNOP123456789ABCDEF"
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMIBPxRfiCYEXAMPLEKEY12345"
DATABASE_PASSWORD = "admin_super_secret_2024"


def connect_to_aws():
    """CWE-798: Hardcoded Credentials"""
    return boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )


# ==================== SAFE ====================

def get_user_safe(user_id):
    """SAFE: Parameterized query - no concatenation"""
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    return cursor.fetchone()


def ping_safe(hostname):
    """SAFE: subprocess with array, no shell"""
    if not hostname.replace(".", "").replace("-", "").isalnum():
        raise ValueError("Invalid hostname")
    return subprocess.check_output(["ping", "-c", "4", hostname])


def load_data_safe(json_string):
    """SAFE: JSON instead of pickle"""
    try:
        return json.loads(json_string)
    except json.JSONDecodeError:
        return None


def read_file_validated(filename):
    """SAFE: Path validation against directory traversal"""
    safe_base = "/var/uploads/"
    full_path = os.path.realpath(os.path.join(safe_base, filename))
    if not full_path.startswith(safe_base):
        raise ValueError("Invalid path")
    with open(full_path, "r") as f:
        return f.read()


def connect_with_env():
    """SAFE: Credentials from environment variables"""
    password = os.environ.get("DB_PASSWORD")
    if not password:
        raise EnvironmentError("DB_PASSWORD not set")
    return mysql.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=password
    )


def safe_divide(a, b):
    """SAFE: Input validation prevents errors"""
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Inputs must be numbers")
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


def load_config_safe(yaml_data):
    """SAFE: yaml.safe_load instead of yaml.load"""
    return yaml.safe_load(yaml_data)
