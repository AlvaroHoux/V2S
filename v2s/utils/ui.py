import sys
import time
import threading
import itertools

class Spinner:
    def __init__(self, message="Processing..."):
        self.spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        self.stop_running = False
        self.message = message
        self.thread = None

    def spin(self):
        while not self.stop_running:
            sys.stdout.write(f'\r\033[96m{next(self.spinner)}\033[0m {self.message}')
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\r' + ' ' * (len(self.message) + 4) + '\r')

    def __enter__(self):
        self.stop_running = False
        self.thread = threading.Thread(target=self.spin)
        self.thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_running = True
        if self.thread:
            self.thread.join()

def print_success(msg): 
    print(f"[\033[92m✓\033[0m] {msg}")

def print_error(msg):   
    print(f"[\033[91mX\033[0m] {msg}")

def print_info(msg):    
    print(f"[\033[94mi\033[0m] {msg}")

def print_step(msg):    
    print(f"\n\033[1;95m> {msg}\033[0m")

def print_banner():
    print("""\033[96m
    ██╗   ██╗██████╗ ███████╗
    ██║   ██║╚════██╗██╔════╝
    ██║   ██║ █████╔╝███████╗
    ╚██╗ ██╔╝██╔═══╝ ╚════██║
     ╚████╔╝ ███████╗███████║
      ╚═══╝  ╚══════╝╚══════╝
       Voice-to-Speech CLI
\033[0m""")