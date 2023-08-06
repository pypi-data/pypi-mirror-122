from colorama import init, Fore

init()

class Logger:
    def __init__(self, debug=False, verbose_debug=False) -> None:
        self.__debug = debug
        self.__verbose_debug = verbose_debug
        pass

    def log_program_error(self, msg : str):
        print(f"{Fore.LIGHTRED_EX}[!] Program Error: {msg}{Fore.RESET}")
        exit(0)
    
    def log_correct(self, msg : str):
        print(f"{Fore.LIGHTGREEN_EX}[+] {msg}{Fore.RESET}")

    def log_error(self, msg: str):
        print(f"{Fore.LIGHTRED_EX}[!] {msg}{Fore.RESET}")
    
    def log_skip(self, msg: str):
        print(f"{Fore.LIGHTMAGENTA_EX}[-] {msg}{Fore.RESET}")

    def log_message(self, msg: str):
        print(f"{Fore.LIGHTCYAN_EX}[*]{Fore.RESET} {msg}")

    def log_text(self, msg: str):
        print(f"{Fore.LIGHTBLUE_EX}{msg}{Fore.RESET}")


    def log_space(self):
        print("")

    def debug(self, msg: str):
        if self.__debug:
            print(f"{Fore.LIGHTYELLOW_EX}[!] {msg}{Fore.RESET}")

    def verbose_debug(self, msg: str):
        if self.__verbose_debug:
            print(f"{Fore.LIGHTYELLOW_EX}[!] {msg}{Fore.RESET}")