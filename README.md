# zork

Zork is a flexible python script that allows you to quickly search on Google
using some powerful search parameters, commonly called 'dorks'.

Zork also includes a preconfigured list of dorks which can be conveniently selected with fzf (fuzzyfinder).

It can be tiresome to write the same parameters over and over again
so the single letters make your dorkin' experience easier.

Last but not least, Zork completely bypasses the very annoying and oh so frequent captchas.


## Installation

**1.** Clone the repository:
```shell
git clone https://github.com/recklessroot/zork
```
**2.** Install the fzf package from your package manager
```shell
cat linux-requirements.txt | xargs sudo [Your-Install-Cmd]
```

**3.** Install the python dependencies:
method 1: Pip
```shell
pip install -r py-requirements.txt
```
method 2: Package manager
```shell
cat py-requirements.txt | sed 's/^/python-/' | xargs sudo [Your-Install-Cmd]
```
**4.** Create an alias (Optional)
temporary:
```shell
alias zork="python3 /path/to/zork.py"
```
permanent:
```shell
echo "alias zork='python3 /path/to/zork.py'" >> /path/to/your_shell_config_file
```

## Precisions

- You can add your own dork list in 'fuzzy/'
  Zork will automatically make a single list with every files in this directory and remove duplicates.

- You can reproduce queries like: '+intitle:somequery', '-intitle:somequery'
  For this, add the sign as your first character.
  If instead you want to search for a literal '+' as first character, use '\+'. (See Examples)

- By default Zork uses a random user-agent, but you can specify one with the -a flag.

- When using the -z flag (fuzzyfinder), the result will prepend any other flags.
  Inversely, the -q flag (query) is always last.  ('FUZZY_CHOICE ... some dorks ... QUERY')

- Som arguments can be used multiple times, look for the '\*' in the help section


## Example usage

Searching for 5 results using Googlebot as user-agent containing [FUZZY_STRING] and includes both 'title1' and 'title2' in the title
```shell
python3 zork.py -z -n 5 -a 'Googlebot' -T '"title1" "title2"'
```

Searching for 10 results using a random user-agent (this is the default) for 'txt' files, only on 'example.com'
```shell
python3 zork.py -n 10 -s 'example.com' -f 'txt'
```

Searching for a url containing 'wp' AND '-admin', but NOT '-includes', with a title include '-login'
```shell
python3 zork.py -u 'wp' -u '+-admin' -u '-"-includes"' -t '"\-login"'
```
