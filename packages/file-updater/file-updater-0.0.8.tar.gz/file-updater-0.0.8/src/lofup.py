from fup.updater import FileUpdater
import sys
from colorama import init
init()
from colorama import Fore, Back, Style

if(len(sys.argv) < 3):
    print(f'{Fore.RED}Please use the following format:')
    print(f'{Fore.MAGENTA}lofup.py {Fore.GREEN}[Source path] [Destination path]{Style.RESET_ALL}')
    print(fr'e.g. lofup.py C:\Users\max\programming H:\code\snippets')
else:
    try:
        if(len(sys.argv) == 4):
            file_updater = FileUpdater(output_console=True, fup_file_path=sys.argv[3])
        else:
            file_updater = FileUpdater(output_console=True)

        file_updater.update_files(
            path_source=sys.argv[1], 
            path_dest=sys.argv[2])
    except Exception as exc:
        print(f'{Fore.RED}{exc}{Style.RESET_ALL}')

    