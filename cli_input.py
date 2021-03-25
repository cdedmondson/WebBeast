import argparse
import sys
from Utilities import file_helper
from Utilities import utility_methods as utm

parser = argparse.ArgumentParser(description="Web application enumeration tool without a lame banner",
                                 usage=''' python3 web_enum.py <target> <port> [options]

  Example: 

      python3 web_enum.py -t http://10.15.1.1 -p 80''',
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-t',
                    '--target',
                    type=str,
                    required=False,
                    help='Scan a single target')
parser.add_argument('-p',
                    '--port',
                    type=int,
                    required=False,
                    default=80,
                    help="Web port to scan i.e. 80,443,8080,...")
parser.add_argument('-th',
                    '--threads',
                    type=int,
                    required=False,
                    default=10,
                    help='Number of threads you want each tool run (50 MAX) default 10')
parser.add_argument('-o',
                    '--output',
                    type=str,
                    required=False,
                    help='Absolute path you want scan results stored')
parser.add_argument('-e',
                    '--extensions',
                    type=str,
                    required=False,
                    help='''File extensions you want tools to enumerate separated by comma Example: 
                              asp,aspx,sh,html,txt,etc,...''')
parser.add_argument('-lw',
                    '--list_wordlists',
                    action="store_true",
                    help='List all word list key value pairs')
parser.add_argument('-le',
                    '--list_extensions',
                    action="store_true",
                    help='List all file extensions')
parser.add_argument("-w",
                    "--wordlist",
                    type=str,
                    required=False,
                    help='''
Options:

  Apache: apache:common, apache:fuzz, apache:vulns
  Apache Tomcat: apache_tomcat:common
  Wordpress: wordpress:themes, wordpress:plugins, wordpress:fuzz
  Joomla: joomla:themes
  Coldfusion: coldfusion:fuzz, coldfusion:vulns
  Drupal: drupal:fuzz
  Dirb: dirb:big, dirb:common
  Dirbuster: dirbuster:ls, dirbuster:lm, dirbuster:sm, dirbuster:m, dirbuster:s

Examples:

  -w dirb:medium = Scan target with wordlist from dirb
  -w wordpress:themes plugins = Scan target for wordpress plugins

  ''')

args = parser.parse_args()

if args.list_wordlists:
    file_helper.display_word_list()
    sys.exit()
elif args.list_extensions:
    file_helper.display_file_extensions()
    sys.exit()
else:
    if args.target is None:
        sys.exit(utm.colors('bred', "[!] You must specify a target's IP address"))
    elif not utm.is_valid_ip(args.target):
        sys.exit()
    if args.port is None:
        sys.exit(utm.colors('bred', "[!] You must specify a web port to scan"))
    elif not utm.is_valid_port(args.port):
        sys.exit(utm.colors('bred', '[!] Port must between 1 and 65535'))
    if args.threads is None:
        args.threads = 10
    elif not utm.check_range(args.threads):
        sys.exit(utm.colors('bred', '[!] Thread count must be between 1 and 50'))
    if args.output is None:
        pass  # Add default directory
    if args.extensions is None:
        args.extensions = "php,txt,pl,sh,asp,aspx,html,json,py,cfm,rb,cgi"
    if args.wordlist is None:
        args.wordlist = ['dirsearch:default']
    else:
        # Split user input from dirb:commmon,dirb:large to [['dirb:common','dirb:large']]
        scan_list = [args.wordlist.rsplit(",")]
        # Turn double list to single i.e. from [['dirb:common','dirb:large']] to ['dirb:commmon','dirb:large']
        scan_list = utm.getlist_values(scan_list)
        args.wordlist = scan_list
