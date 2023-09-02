"""Web Utilities"""


import platform
import re
import requests
import traceback

from time import sleep

from config.fanslyconfig import FanslyConfig
from textio import print_error, print_info_highlight, print_warning


# mostly used to attempt to open fansly downloaders documentation
def open_url(url_to_open: str) -> None:
    """Opens an URL in a browser window.
    
    :param str url_to_open: The URL to open in the browser.
    """
    sleep(10)

    try:
        import webbrowser
        webbrowser.open(url_to_open, new=0, autoraise=True)

    except Exception:
        pass


def open_get_started_url() -> None:
    open_url('https://github.com/prof79/fansly-downloader-ng/wiki/Getting-Started')


def get_fansly_account_for_token(auth_token: str) -> str | None:
    """Fetches user account information for a particular authorization token.

    :param auth_token: The Fansly authorization token.
    :type auth_token: str

    :return: The account user name or None.
    :rtype: str | None
    """
    headers = {
        'authority': 'apiv3.fansly.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en;q=0.8,en-US;q=0.7',
        'authorization': auth_token,
        'origin': 'https://fansly.com',
        'referer': 'https://fansly.com/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    me_req = requests.get(
        'https://apiv3.fansly.com/api/v1/account/me',
        params={'ngsw-bypass': 'true'},
        headers=headers
    )

    if me_req.status_code == 200:
        me_req = me_req.json()['response']['account']
        account_username = me_req['username']

        if account_username:
            return account_username

    return None


def guess_user_agent(user_agents: dict, based_on_browser: str, default_ua: str) -> str:
    """Returns the guessed browser's user agent or a default one."""

    if based_on_browser == 'Microsoft Edge':
        based_on_browser = 'Edg' # msedge only reports "Edg" as its identifier

        # could do the same for opera, opera gx, brave. but those are not supported by @jnrbsn's repo. so we just return chrome ua
        # in general his repo, does not provide the most accurate latest user-agents, if I am borred some time in the future,
        # I might just write my own similar repo and use that instead

    os_name = platform.system()

    try:
        if os_name == "Windows":
            for user_agent in user_agents:
                if based_on_browser in user_agent and "Windows" in user_agent:
                    match = re.search(r'Windows NT ([\d.]+)', user_agent)
                    if match:
                        os_version = match.group(1)
                        if os_version in user_agent:
                            return user_agent

        elif os_name == "Darwin":  # macOS
            for user_agent in user_agents:
                if based_on_browser in user_agent and "Macintosh" in user_agent:
                    match = re.search(r'Mac OS X ([\d_.]+)', user_agent)
                    if match:
                        os_version = match.group(1).replace('_', '.')
                        if os_version in user_agent:
                            return user_agent

        elif os_name == "Linux":
            for user_agent in user_agents:
                if based_on_browser in user_agent and "Linux" in user_agent:
                    match = re.search(r'Linux ([\d.]+)', user_agent)
                    if match:
                        os_version = match.group(1)
                        if os_version in user_agent:
                            return user_agent

    except Exception:
        print_error(f'Regexing user-agent from online source failed: {traceback.format_exc()}', 4)

    print_warning(f"Missing user-agent for {based_on_browser} & OS: {os_name}. Chrome & Windows UA will be used instead.")

    return default_ua


def get_release_info_from_github(current_program_version: str) -> dict | None:
    """Fetches and parses the Fansly Downloader NG release info JSON from GitHub.
    
    :param str current_program_version: The current program version to be
        used in the user agent of web requests.

    :return: The release info from GitHub as dictionary or
        None if there where any complications eg. network error.
    :rtype: dict | None
    """
    try:
        url = f"https://api.github.com/repos/prof79/fansly-downloader-ng/releases/latest"

        response = requests.get(
            url,
            allow_redirects=True,
            headers={
                'user-agent': f'Fansly Downloader NG {current_program_version}',
                'accept-language': 'en-US,en;q=0.9'
            }
        )

        response.raise_for_status()

    except Exception:
        return None
    
    if response.status_code != 200:
        return None
    
    return response.json()
