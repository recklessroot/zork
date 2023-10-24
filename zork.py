#!venv/bin/python3.11

import argparse
import json
import pyfzf
from fake_useragent import UserAgent
from googlesearch import search
from os import listdir, path

# $PWD
SCRIPT_DIR = f'{path.dirname(__file__)}'

FUZZY_DIR = f'{SCRIPT_DIR}/fuzzy/'
HELP_FILE = f'{SCRIPT_DIR}/HELP.txt'

def someHelpPlease():
    with open(HELP_FILE, 'r') as help_file:
        print(help_file.read())
    exit(0)


# dork selection with fzf
def fuzzyFind():
    dork_lists = []

    # every file in FUZZY_DIR
    for file in listdir(FUZZY_DIR):
        lst = open(FUZZY_DIR + file, 'r')
        dork_lists = [*dork_lists, *lst.read().splitlines()]
        lst.close()

    choice = pyfzf.FzfPrompt().prompt(set(dork_lists), '--multi --cycle')
    return ' '.join(choice)

# google search
def zorkin(query, userAgent, num, wait):
    results = []
    for i in search(query, num=int(num), stop=int(num), pause=int(wait), user_agent=userAgent):
        results.append(i)
    return results

# command options
def getOptions():
    parser = argparse.ArgumentParser(add_help=False)

    # Script Options:
    parser.add_argument("-a", "--agent", action="store", dest="agent", required=False)
    parser.add_argument("-d", "--dry-run", action="store_true", dest="dryrun", default=False)
    parser.add_argument("-h", "--help", action="store_true", dest="help", default=False)
    parser.add_argument("-j", "--json", action="store_true", dest="json", default=False)
    parser.add_argument("-n", "--num", action="store", dest="num")
    parser.add_argument("-o", "--outfile", action="store", dest="outfile", required=False)
    parser.add_argument("-z", "--fuzzy", action="store_true", dest="fuzzy", default=False)
    # Search parameters:
    parser.add_argument("-e", "--ext", action="store", dest="ext", required=False)
    parser.add_argument("-f", "--filetype", action="store", dest="filetype", required=False)
    parser.add_argument("-l", "--link", action="append", dest="link", required=False)
    parser.add_argument("-q", "--query", action="append", dest="query", required=False)
    parser.add_argument("-r", "--related", action="append", dest="related", required=False)
    parser.add_argument("-s", "--site", action="store", dest="site", required=False)
    parser.add_argument("-t", "--intitle", action="append", dest="intitle", required=False)
    parser.add_argument("-T", "--allintitle", action="store", dest="allintitle", required=False)
    parser.add_argument("-u", "--inurl", action="append", dest="inurl", required=False)
    parser.add_argument("-U", "--allinurl", action="store", dest="allinurl", required=False)
    parser.add_argument("-w", "--wait", action="store", dest="wait", default=5)
    parser.add_argument("-x", "--intext", action="append", dest="intext", required=False)

    if parser.parse_args().help:
        someHelpPlease()

    options = {
        'search_string' : '',
        'agent' : parser.parse_args().agent,
        'num' : parser.parse_args().num,
        'wait' : parser.parse_args().wait,
        'outfile' : parser.parse_args().outfile,
        'json' : parser.parse_args().json,
        'dryrun' : parser.parse_args().dryrun
    }

    query_special = {
        'query' : parser.parse_args().query,
        'fuzzy' : parser.parse_args().fuzzy
    }

    # list of query parameters to concatonate after being formatted
    query_blocks = []

    query_dorks = {
        'site' : parser.parse_args().site,
        'allintitle' : parser.parse_args().allintitle,
        'allinurl' : parser.parse_args().allinurl,
        'ext' : parser.parse_args().ext,
        'filetype' : parser.parse_args().filetype,
        'intext' : parser.parse_args().intext,
        'intitle' : parser.parse_args().intitle,
        'inurl' : parser.parse_args().inurl,
        'link' : parser.parse_args().link,
        'related' : parser.parse_args().related
    }

    if query_special['fuzzy']:
        query_blocks.append(fuzzyFind())

    for arg in query_dorks.items():

        # Check if flag was used
        if arg[1]:
            param = f"{arg[0]}:"
            value_lst = arg[1]

            # transform string value into list to accomodate reusable flags
            if type(value_lst) is str:
                value_lst = [value_lst]

            for value in value_lst:

                # ex: -x '-example' --> -intext:example
                if value.startswith('-') or value.startswith('+'):
                    param = ''.join([value[0], param])
                    value = value[1:]

                # ex: -x '\-example' --> intext:-example
                if value.startswith('\\'):
                    value = value[1:]
                
                query_blocks.append(''.join([param, value]))

    if query_special['query']:
        query_blocks.append(str(query_special['query']))

    options['search_string'] = ' '.join(query_blocks)

    return options

# json formatting
def fmtJson(options, results):
    json_results = {
        'options' : options,
        'results' : results
    }
    return json.dumps(json_results, indent=2)


def main():
    opts = getOptions()

    if not opts['agent']:
        opts['agent'] = UserAgent().random

    if not opts['num']:
        opts['num'] = 10

    if opts['search_string'] == '':
        someHelpPlease()

    if opts['dryrun']:
        print(f"Zork: Dry run mode.\n\n{opts['search_string']}")
        exit(0)

    results = zorkin(opts['search_string'], opts['agent'], opts['num'], opts['wait'])

    if opts['json']:
        results = fmtJson(opts, results)

    if opts['outfile']:
        if not opts['json'] and opts['outfile'].endswith('.json'):
            content = fmtJson(opts, results)
        else:
            content = results

        with open(opts['outfile'], 'w') as outfile:
            outfile.write(content)

    print(results)


if __name__ == "__main__":
    main()

