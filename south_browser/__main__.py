import inquirer

from requests.exceptions import ConnectionError
from .rpc import *

def main():
    try:
        work()
    except ConnectionError:
        print("Failed to connect to RPC")

def work():
    servers = NSGetGameServers()

    choices = [f"{s[2]} ({s[6]}/{s[7]})" for s in servers]
    questions = [
        inquirer.List('server_index',
            message="What server do you want to join?",
            choices=choices,
        ),
    ]

    answers = inquirer.prompt(questions)
    i = answers["server_index"]
    si = choices.index(i)

    NSTryAuthWithServer(si)

    sleep(1)

    if not NSWasAuthSuccessful():
        print("Failed to auth")
        return

    NSConnectToAuthedServer()


if __name__ == "__main__":
    main()
