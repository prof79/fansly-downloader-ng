"""Configuration Class for Shared State"""


from configparser import ConfigParser
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from config.modes import DownloadMode
from config.metadatahandling import MetadataHandling

from api import FanslyApi


@dataclass
class FanslyConfig(object):
    #region Fields

    #region File-Independent Fields

    # Mandatory property
    # This should be set to __version__ in the main script.
    program_version: str

    # Define base threshold (used for when modules don't provide vars)
    DUPLICATE_THRESHOLD: int = 50

    # Batch size for batched API access (Fansly API size limit)
    BATCH_SIZE: int = 150

    # Configuration file
    config_path: Optional[Path] = None

    # Misc
    token_from_browser_name: Optional[str] = None
    debug: bool = False
    # If specified on the command-line
    post_id: Optional[str] = None
    # Set on start after self-update
    updated_to: Optional[str] = None

    # Objects
    _parser = ConfigParser(interpolation=None)
    _api: Optional[FanslyApi] = None

    #endregion File-Independent

    #region config.ini Fields

    # TargetedCreator > username
    user_names: Optional[set[str]] = None

    # MyAccount
    token: Optional[str] = None
    user_agent: Optional[str] = None
    check_key: Optional[str] = None
    #session_id: str = 'null'

    # Options
    # "Normal" | "Timeline" | "Messages" | "Single" | "Collection"
    download_mode: DownloadMode = DownloadMode.NORMAL
    download_directory: (None | Path) = None
    download_media_previews: bool = True
    # "Advanced" | "Simple"
    metadata_handling: MetadataHandling = MetadataHandling.ADVANCED
    open_folder_when_finished: bool = True
    separate_messages: bool = True
    separate_previews: bool = False
    separate_timeline: bool = True
    show_downloads: bool = True
    show_skipped_downloads: bool = True
    use_duplicate_threshold: bool = False
    use_folder_suffix: bool = True
    # Show input prompts or sleep - for automation/scheduling purposes
    interactive: bool = True
    # Should there be a "Press <ENTER>" prompt at the very end of the program?
    # This helps for semi-automated runs (interactive=False) when coming back
    # to the computer and wanting to see what happened in the console window.
    prompt_on_exit: bool = True

    # Number of retries to get a timeline
    timeline_retries: int = 1
    # Anti-rate-limiting delay in seconds
    timeline_delay_seconds: int = 60

    # Cache
    cached_device_id: Optional[str] = None
    cached_device_id_timestamp: Optional[int] = None

    # Logic
    check_key_pattern: Optional[str] = None
    main_js_pattern: Optional[str] = None

    #endregion config.ini

    #endregion Fields

    #region Methods

    def get_api(self) -> FanslyApi:
        if self._api is None:
            token = self.get_unscrambled_token()
            user_agent = self.user_agent

            if token and user_agent and self.check_key:
                self._api = FanslyApi(
                    token=token,
                    user_agent=user_agent,
                    check_key=self.check_key,
                    #session_id=self.session_id,
                    device_id=self.cached_device_id,
                    device_id_timestamp=self.cached_device_id_timestamp,
                    on_device_updated=self._save_config,
                )

                # Explicit save - on init of FanslyApi() self._api was None
                self._save_config()
            
            else:
                raise RuntimeError(
                    'Token or user agent error creating Fansly API object.'
                )

        return self._api


    def user_names_str(self) -> Optional[str]:
        """Returns a nicely formatted and alphabetically sorted list of
        creator names - for console or config file output.
        
        :return: A single line of all creator names, alphabetically sorted
            and separated by commas eg. "alice, bob, chris, dora".
            Returns None if user_names is None.
        :rtype: Optional[str]
        """
        if self.user_names is None:
            return None

        return ', '.join(sorted(self.user_names))


    def download_mode_str(self) -> str:
        """Gets the string representation of `download_mode`."""
        return str(self.download_mode).capitalize()


    def metadata_handling_str(self) -> str:
        """Gets the string representation of `metadata_handling`."""
        return str(self.metadata_handling).capitalize()

    
    def _sync_settings(self) -> None:
        """Syncs the settings of the config object
        to the config parser/config file.

        This helper is required before saving.
        """
        self._parser.set('TargetedCreator', 'username', self.user_names_str())

        self._parser.set('MyAccount', 'authorization_token', self.token)
        self._parser.set('MyAccount', 'user_agent', self.user_agent)
        self._parser.set('MyAccount', 'check_key', self.check_key)
        #self._parser.set('MyAccount', 'session_id', self.session_id)

        if self.download_directory is None:
            self._parser.set('Options', 'download_directory', 'Local_directory')
        else:
            self._parser.set('Options', 'download_directory', str(self.download_directory))

        self._parser.set('Options', 'download_mode', self.download_mode_str())
        self._parser.set('Options', 'metadata_handling', self.metadata_handling_str())
        
        # Booleans
        self._parser.set('Options', 'show_downloads', str(self.show_downloads))
        self._parser.set('Options', 'show_skipped_downloads', str(self.show_skipped_downloads))
        self._parser.set('Options', 'download_media_previews', str(self.download_media_previews))
        self._parser.set('Options', 'open_folder_when_finished', str(self.open_folder_when_finished))
        self._parser.set('Options', 'separate_messages', str(self.separate_messages))
        self._parser.set('Options', 'separate_previews', str(self.separate_previews))
        self._parser.set('Options', 'separate_timeline', str(self.separate_timeline))
        self._parser.set('Options', 'use_duplicate_threshold', str(self.use_duplicate_threshold))
        self._parser.set('Options', 'use_folder_suffix', str(self.use_folder_suffix))
        self._parser.set('Options', 'interactive', str(self.interactive))
        self._parser.set('Options', 'prompt_on_exit', str(self.prompt_on_exit))

        # Unsigned ints
        self._parser.set('Options', 'timeline_retries', str(self.timeline_retries))
        self._parser.set('Options', 'timeline_delay_seconds', str(self.timeline_delay_seconds))

        # Cache
        if self._api is not None:
            self._parser.set('Cache', 'device_id', str(self._api.device_id))
            self._parser.set('Cache', 'device_id_timestamp', str(self._api.device_id_timestamp))
            self.cached_device_id = self._api.device_id
            self.cached_device_id_timestamp = self._api.device_id_timestamp

        # Logic
        self._parser.set('Logic', 'check_key_pattern', str(self.check_key_pattern))
        self._parser.set('Logic', 'main_js_pattern', str(self.main_js_pattern))


    def _load_raw_config(self) -> list[str]:
        if self.config_path is None:
            return []

        else:
            return self._parser.read(self.config_path)


    def _save_config(self) -> bool:
        if self.config_path is None:
            return False

        else:
            self._sync_settings()

            with self.config_path.open('w', encoding='utf-8') as f:
                self._parser.write(f)
                return True


    def token_is_valid(self) -> bool:
        if self.token is None:
            return False

        return not any(
            [
                len(self.token) < 50,
                'ReplaceMe' in self.token,
            ]
        )

    
    def useragent_is_valid(self) -> bool:
        if self.user_agent is None:
            return False

        return not any(
            [
                len(self.user_agent) < 40,
                'ReplaceMe' in self.user_agent,
            ]
        )
    

    def get_unscrambled_token(self) -> Optional[str]:
        """Gets the unscrambled Fansly authorization token.

        Unscrambles the token if necessary.
                
        :return: The unscrambled Fansly authorization token.
        :rtype: Optional[str]
        """

        if self.token is not None:
            F, c ='fNs', self.token
            
            if c[-3:] == F:
                c = c.rstrip(F)

                A, B, C = [''] * len(c), 7, 0
                
                for D in range(B):
                    for E in range(D, len(A), B) : A[E] = c[C]; C += 1
                
                return ''.join(A)

            else:
                return self.token

        return self.token

    #endregion
