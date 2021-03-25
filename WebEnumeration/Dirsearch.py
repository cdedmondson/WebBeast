from Utilities import subprocess_helper as sp
from Utilities import utility_methods as utm
from Utilities import file_helper


class Dirsearch:

    # Initialization
    def __init__(self, ip, port, threads, file, word_list, extensions):
        self.ip = ip
        self.port = port
        self.threads = threads
        self.file = file
        self.word_list = word_list
        self.extensions = extensions

    '''
        Method: initial_scan
        Purpose: Non recursive scan.
    '''

    def initial_scan(self, wl):
        if not utm.port_443(self.port):
            scan = f"/opt/dirsearch/./dirsearch.py -u http://{self.ip}:{self.port} -e {self.extensions} -t {self.threads} -w {wl} >> {self.file}"
        else:
            scan = f"/opt/dirsearch/./dirsearch.py -u https://{self.ip}:{self.port} -e {self.extensions} -t {self.threads} >> {self.file}"

        return scan

    '''
        Method: deep_scan
        Purpose: Recursive scan.
    '''

    def deep_scan(self):
        if not utm.port_443(self.port):
            scan = f"/opt/dirsearch/./dirsearch.py -u http://{self.ip}:{self.port} -e {self.extensions} -r -t {self.threads} -w {self.word_list} >> {self.file}"
        else:
            scan = f"/opt/dirsearch/./dirsearch.py -u https://{self.ip}:{self.port} -e {self.extensions} -r -t {self.threads} >> {self.file}"

        return scan

    '''
        Method: progress
        Purpose: Let user know tool progress.
    '''

    def progress(self, wl):
        return utm.colors('bblue', f'[+] Wordlist {wl} scanning in progress')

    '''
        Method: finished
        Purpose: Let user know when tool has finished.
    '''

    def finished(self, wl):
        return utm.colors('bmagenta', f'[✔] {wl} Finished!\n')

    '''
        Method: scan
        Purpose: Initiate scan.
    '''

    def scan(self, custom_wordlist):
        print(self.progress(custom_wordlist))  # Display current wordlist progress
        sp.run(self.initial_scan(custom_wordlist))
        print(self.finished(custom_wordlist))  # Notify user scan has finished

        return file_helper.clean_file(self.file)  # Remove excess data
