import cli_input
from Utilities import file_helper as fh
from Utilities import utility_methods as utm
from WebEnumeration.Dirsearch import Dirsearch


def main():
    # Build output file name
    file_path = fh.prepare_scan_results_file(cli_input.args.target, cli_input.args.port)
    # Pass parameters to Dirsearch constructor
    ds = Dirsearch(cli_input.args.target, cli_input.args.port, cli_input.args.threads, file_path,
                   cli_input.args.wordlist,
                   cli_input.args.extensions)

    # Combine all user selected wordlists locations into one list
    combined_list = fh.combine_lists(ds.word_list)

    # Convert user input list selections into string
    wordlists = fh.list_to_string(combined_list)

    # Concatenate chosen lists to one custom list
    fh.create_custom_wordlist(wordlists, ds.ip)

    ds.scan(utm.get_current_directory() + '/' + f"{ds.ip}_custom_wordlist.txt")  # Invoke scan

    fh.filter_codes(file_path)  # Remove invalid http codes


if __name__ == '__main__':
    main()
