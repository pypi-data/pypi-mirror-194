class bcolors:
    GRAY = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PINK = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'    
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
   


def print_pink(msg):
    print(f"{bcolors.PINK}{msg}{bcolors.ENDC}")

def print_blue(msg):
    print(f"{bcolors.BLUE}{msg}{bcolors.ENDC}")

def print_cyan(msg):
    print(f"{bcolors.CYAN}{msg}{bcolors.ENDC}")

def print_green(msg):
    print(f"{bcolors.GREEN}{msg}{bcolors.ENDC}")

def print_yellow(msg):
    print(f"{bcolors.YELLOW}{msg}{bcolors.ENDC}")

def print_red(msg):
    print(f"{bcolors.RED}{msg}{bcolors.ENDC}")    

def print_pinkb(msg):
    print(f"{bcolors.PINK}{bcolors.BOLD}{msg}{bcolors.ENDC}")

def print_blueb(msg):
    print(f"{bcolors.BLUE}{bcolors.BOLD}{msg}{bcolors.ENDC}")

def print_cyanb(msg):
    print(f"{bcolors.CYAN}{bcolors.BOLD}{msg}{bcolors.ENDC}")

def print_greenb(msg):
    print(f"{bcolors.GREEN}{bcolors.BOLD}{msg}{bcolors.ENDC}")

def print_yellowb(msg):
    print(f"{bcolors.YELLOW}{bcolors.BOLD}{msg}{bcolors.ENDC}")

def print_redb(msg):
    print(f"{bcolors.RED}{bcolors.BOLD}{msg}{bcolors.ENDC}")  

def helloWorld():
    print("Hello World!")
    
