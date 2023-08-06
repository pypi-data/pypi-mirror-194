# Module update checker, based off the github file
import os


GlobalRead = True
try:
    import requests
except ModuleNotFoundError:
    print(
        "Requests is not installed. Can not check for a new PythonFunction update!"
    )
    GlobalRead = False


def CanReadGlobal():
    """Get if requests is installed

    Returns:
        bool: Requests is installed
    """
    return GlobalRead


def ReadLocal():
    """Get the module version

    Returns:
        str: Module version
    """
    return "1.4.8"


url = "https://raw.githubusercontent.com/FunAndHelpfulDragon/python-Functions/main/Version.txt"


def ReadGlobal():
    """Get the version on the server"""
    if GlobalRead:
        try:
            r = requests.get(url, timeout=10)
            return r.text
        except (
            requests.exceptions.TooManyRedirects,
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
            requests.exceptions.Timeout,
        ):
            print("Failed to read the latest version!")

    return None


def Compare(hint: bool = True):
    current = ReadLocal()
    server = ReadGlobal()

    if hint:
        print(
            "HINT: Make the PyFuncSet.json file and set Mute to true to speed up the loading time."
        )

    if server is None:
        # break eariler if no response, we have already mentioned about it.
        return

    if server > current:
        print("*" * os.get_terminal_size().columns)
        print(
            f"""Notice: A newer version of PythonFunctions is alvalible.
Current Version: {current}. New version: {server}"""
        )
        print("*" * os.get_terminal_size().columns)


if __name__ == "__main__":
    if GlobalRead:
        ReadGlobal()
