
import os
import psutil
import re

def is_already_running(lock_file_path):
    """Checks if the application is already running using a lock file and PID check."""
    if os.path.exists(lock_file_path):
        try:
            with open(lock_file_path, 'r') as f:
                content = f.read().strip()
                if not content:
                    return False
                pid = int(content)
            if psutil.pid_exists(pid):
                return True
        except (IOError, ValueError, psutil.NoSuchProcess):
            try:
                os.remove(lock_file_path)
            except OSError:
                pass
    return False

def create_lock_file(lock_file_path):
    try:
        with open(lock_file_path, 'w') as f:
            f.write(str(os.getpid()))
    except OSError:
        pass

def remove_lock_file(lock_file_path):
    if os.path.exists(lock_file_path):
        try:
            os.remove(lock_file_path)
        except OSError:
            pass

def parse_input_text(input_text):
    """
    Parses input text into a matrix of values.
    Supports tab-separated (Excel) and loose separators (comma, space, etc).
    """
    input_text = input_text.strip()
    if not input_text:
        return []

    input_matrix = []
    
    # Check if it looks like copied Excel data (tabs)
    if '\t' in input_text:
        for line in input_text.split('\n'):
            values = line.split('\t')
            row = []
            for v in values:
                v_stripped = v.strip()
                if not v_stripped:
                    row.append(None)
                    continue
                try:
                    row.append(float(v_stripped))
                except (ValueError, TypeError):
                    row.append(None)
            input_matrix.append(row)
    else:
        # Loose parsing
        for line in input_text.split('\n'):
            if not line.strip(): continue
            # Split by common separators: whitespace, comma, semicolon, slash, chinese comma/semicolon
            values = re.split(r'[\s,;；/\t]+', line.strip())
            row = []
            for v in values:
                try:
                    row.append(float(v))
                except (ValueError, TypeError):
                    continue
            if row: 
                input_matrix.append(row)
    
    return input_matrix
