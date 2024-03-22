"""Web Utilities"""


import platform
import re
import requests
import traceback

from collections import OrderedDict, namedtuple
from urllib.parse import urlparse, parse_qs
from time import sleep
from typing import Any, NamedTuple, Optional

from textio import print_error, print_warning


def get_file_name_from_url(url: str) -> str:
    """Parses an URL and returns the last part which usually is a
    file name or directory/section.
    
    :param url: The URL to parse.
    :type url: str
    
    :return: The last part of the path ie. everything after the
        last slash excluding the query string.
    :rtype: str
    """
    parsed_url = urlparse(url)

    last_part = parsed_url.path.split('/')[-1]

    return last_part


def get_qs_value(url: str, key: str, default: Any=None) -> Any:
    """Returns the value of a specific key of an URL query string.
    
    :param url: The URL to parse for a query string.
    :type url: str

    :param key: The key in the query string (&key1=value1&key2=value2 ...)
        whose value to return.
    :type key: str

    :param default: The default value to return if the
        key was not found.
    :type default: Any

    :return: The value of `key` in the query string or `default` otherwise.
    :rtype: Any
    """
    parsed_url = urlparse(url)
    qs = parsed_url.query
    parsed_qs = parse_qs(qs)

    result = parsed_qs.get(key, default)

    if result is default:
        return result
    
    if len(result) == 0:
        return None
    
    return result[0]


def get_flat_qs_dict(url: str) -> dict[str, str]:
    """Returns a flattened version of the dictionary
    as returned by `parse_qs`.
    
    :param url: The URL to parse for a query string.
    :type url: str

    :return: The dictionary as returned by `parse_qs` but with
        the values flattened (first element of list or `''`).
    :rtype: Any
    """
    query = parse_qs(urlparse(url).query)

    new_dict = OrderedDict()

    for key in query.keys():
        value = query[key]

        if len(value) == 0:
            new_dict[key] = ''
        
        else:
            new_dict[key] = value[0]

    return new_dict


def split_url(url: str) -> NamedTuple:
    """Splits an URL into absolue base and file name URLs
    without query strings et al.

    Eg.:
        https://my.server/some/path/interesting.txt?k1=v1&a2=b4
    
    becomes

        (
            base_url='https://my.server/some/path',
            file_url='https://my.server/some/path/interesting.txt'
        )
    """
    parsed_url = urlparse(url)

    # URL without query string et al
    file_url = f'{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}'

    # Base URL
    base_url = file_url.rsplit('/', 1)[0]

    SplitURL = namedtuple('SplitURL', ['base_url', 'file_url'])

    return SplitURL(base_url, file_url)


# mostly used to attempt to open fansly downloaders documentation
def open_url(url_to_open: str) -> None:
    """Opens an URL in a browser window.
    
    :param url_to_open: The URL to open in the browser.
    :type url_to_open: str
    """
    sleep(10)

    try:
        import webbrowser
        webbrowser.open(url_to_open, new=0, autoraise=True)

    except Exception:
        pass


def open_get_started_url() -> None:
    open_url('https://github.com/prof79/fansly-downloader-ng/wiki/Getting-Started')


def guess_check_key(
            main_js_pattern: str,
            check_key_pattern: str,
            user_agent: str,
        ) -> Optional[str]:
    """Tries to guess the check key from the Fansly homepage.
    
    :param main_js_pattern: A regular expression to locate the main.*.js file.
    :type main_js_pattern: str

    :param check_key_pattern: A regular expression to parse the check key.
    :type check_key_pattern: str

    :param user_agent: Browser user agent to use for requests.
    :type user_agent: str
    
    :return: The check key string if found or None otherwise.
    :rtype: Optional[str]
    """
    fansly_url = 'https://fansly.com'

    headers = {
        'User-Agent': user_agent,
    }

    try:
        html_response = requests.get(
            fansly_url,
            headers=headers,
        )

        if html_response.status_code == 200:

            if html_response.text:
                main_js_match = re.search(
                    pattern=main_js_pattern,
                    string=html_response.text,
                    flags=re.IGNORECASE | re.MULTILINE,
                )

                if main_js_match:

                    main_js = main_js_match.group(1)

                    main_js_url = f'{fansly_url}/{main_js}'

                    js_response = requests.get(
                        main_js_url,
                        headers=headers,
                    )

                    if js_response.status_code == 200:

                        if js_response.text:

                            check_key_match = re.search(
                                pattern=check_key_pattern,
                                string=js_response.text,
                                flags=re.IGNORECASE | re.MULTILINE,
                            )

                            if check_key_match:

                                check_key = check_key_match.group(1)

                                return check_key

    except:
        pass

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
    
    :param current_program_version: The current program version to be
        used in the user agent of web requests.
    :type current_program_version: str

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
