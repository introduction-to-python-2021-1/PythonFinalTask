import subprocess
from termcolor import colored


UTIL_NAME = "rss-dimer"


def call_command(command, optional_params):
    params = [command, optional_params, "--", ""]
    result = subprocess.run(params, stdout=subprocess.PIPE)
    return result.stdout.decode("utf-8")


def check_version():
    result = call_command(UTIL_NAME, "--version")
    if result:
        if "version" in result.strip().lower():
            print(colored("PASSED!\n", "green"))
        else:
            print(colored("FAILED!\n", "red"))
    else:
        print(colored("FAILED!\n", "red"))


def main():
    print(colored("***Functional check***\n", "green"))
    print("Check version...")
    check_version()


if __name__ == "__main__":
    main()
