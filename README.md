<div align="center" style="font-size: smaller;">
  <h1><code>Fansly Downloader NG</code>: The Ultimate Content Downloading Tool</h1>
</div>

<div align="center">
  <a href="https://github.com/prof79/fansly-downloader-ng/releases/latest">
    <img src="https://img.shields.io/github/downloads/prof79/fansly-downloader-ng/total?color=0078d7&label=%F0%9F%94%BD%20Downloads&style=flat-square" alt="Downloads" />
  </a>
  <a href="https://github.com/prof79/fansly-downloader-ng/releases/latest">
    <img src="https://img.shields.io/github/v/release/prof79/fansly-downloader-ng?color=%23b02d4a&display_name=tag&label=%F0%9F%9A%80%20Latest%20Compiled%20Release&style=flat-square" alt="Latest Release" />
  </a>
  <a href="https://github.com/prof79/fansly-downloader-ng/commits/main">
    <img src="https://img.shields.io/github/commits-since/prof79/fansly-downloader-ng/latest?color=orange&label=%F0%9F%92%81%20Uncompiled%20Commits&style=flat-square" alt="Commits since latest release" />
  </a>
  <a href="https://github.com/prof79/fansly-downloader-ng/issues?q=is%3Aissue+is%3Aopen+label%3Abug">
    <img src="https://img.shields.io/github/issues-raw/prof79/fansly-downloader-ng/bug?color=pink&label=%F0%9F%A6%84%20Active%20Bugs&style=flat-square" alt="Active Bugs" />
  </a>
</div>

<div align="center">
  <a href="https://github.com/prof79/fansly-downloader-ng#%EF%B8%8F-set-up">
    <img src="https://img.shields.io/badge/Compatible with-grey?style=flat-square" alt="Compatible with text" />
  </a>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/static/v1?style=flat-square&label=%F0%9F%90%8D%20Python&message=3.11%2B&color=3c8c50" alt="Compatibility" />
  </a>
  <a href="https://github.com/prof79/fansly-downloader-ng#%EF%B8%8F-set-up">
    <img src="https://img.shields.io/badge/%F0%9F%AA%9F-Windows-0078D6?style=flat-square" alt="Compatible with Windows" />
  </a>
  <a href="https://github.com/prof79/fansly-downloader-ng#%EF%B8%8F-set-up">
    <img src="https://img.shields.io/badge/%F0%9F%90%A7-Linux-FCC624?style=flat-square" alt="Compatible with Linux" />
  </a>
  <a href="https://github.com/prof79/fansly-downloader-ng#%EF%B8%8F-set-up">
    <img src="https://img.shields.io/badge/%E2%9A%AA-macOS-000000?style=flat-square" alt="Compatible with macOS" />
  </a>
</div>

![Fansly Downloader NG Screenshot](resources/fansly_ng_screenshot.png)

This is a rewrite/refactoring of [Avnsx](https://github.com/Avnsx)'s original [Fansly Downloader](https://github.com/Avnsx/fansly-downloader). **Fansly Downloader NG** supports new features:

* Full command-line support for all options
* `config.ini` not required to start the program anymore - a `config.ini` with all program defaults will be generated automatically
* Support for minimal `config.ini` files - missing options will be added from program defaults automatically
* True multi-user support - put one or more creators as a list into `config.ini` (`username = creator1, creator2, creator3`) or supply via command-line
* Run it in non-interactive mode (`-ni`) without any user intervention - eg. when downloading while being away from the computer
* You may also run it in fully silent mode without the close prompt at the very end (`-ni -npox`) - eg. running **Fansly Downloader NG** from another script or from a scheduled task/cron job
* Logs all relevant messages (`Info`, `Warning`, `Error`, ...) of the last few sessions to `fansly_downloader_ng.log`. A history of 5 log files with a maximum size of 1 MiB will be preserved and can be deleted at your own discretion.
* Easier-to-extend, modern, modular and robust codebase
* It doesn't care about starring the repository

*There are still pieces missing like an appropriate wiki update.*

**Fansly Downloader NG** is the go-to app for all your bulk media downloading needs. Download photos, videos, audio or any other media from Fansly. This powerful tool has got you covered! Say goodbye to the hassle of individually downloading each piece of media – now you can download them all or just some in one go.

## ✨ Features

<table>
  <tr>
    <td align="middle" nowrap>
      <strong>📥 Download Modes</strong>
      <hr>
      <ul align="left">
        <li>Bulk: Timeline, Messages, Collection</li>
        <li>Single Posts by post ID</li>
      </ul>
    </td>
    <td align="middle" nowrap>
      <strong>♻️ Updates</strong>
      <hr>
      <ul align="left">
        <li>Easily update prior download folders</li>
        <li>App keeps itself up-to-date with fansly</li>
      </ul>
    </td>
    <td align="middle" nowrap>
      <strong>🖥️ Cross-Platform Compatibility</strong>
      <hr>
      <ul align="left">
        <li>Compatible with Windows, Linux & MacOS</li>
        <li>Executable app only ships for Windows</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td align="middle" nowrap>
      <strong>⚙️ Customizability</strong>
      <hr>
      <ul align="left">
        <li>Separate media into sub-folders?</li>
        <li>Want to download previews?</li>
      </ul>
    </td>
    <td align="middle" nowrap>
      <strong>🔎 Deduplication</strong>
      <hr>
      <ul align="left">
        <li>Downloads only unique content</li>
        <li>resulting in less bandwidth usage</li>
      </ul>
    </td>
    <td align="middle" nowrap>
      <strong>💸 Free of Charge</strong>
      <hr>
      <ul align="left">
        <li>Open source, community driven project</li>
      </ul>
    </td>
  </tr>
</table>

<img src="https://i.imgur.com/fj0sjQy.png" alt="Computer Mouse Icon" width="23" height="23">[Configuration Settings in detail](https://github.com/prof79/fansly-downloader-ng/wiki/Explanation-of-provided-programs-&-their-functionality#explanation-of-configini)

[Detailed description on each of the components of this software](https://github.com/prof79/fansly-downloader-ng/wiki/Explanation-of-provided-programs-&-their-functionality)<img src="https://i.imgur.com/iIsCcGU.png" alt="Computer Mouse Icon" width="20" height="20">

## 📰 What's New (Release Notes)

⚠️ Due to a [hashing bug](../../issues/13) duplicate videos might be downloaded if a creator re-posts a lot. Downloaded videos will have to be renamed in a future version when video hashing is perfected.

### v0.8.3 2024-02-02

The MP4 parser, required for hashing, now properly supports files larger than 4 GiB in size.

### v0.8.2 2024-02-02

Emergency bugfix, due to [botched hashing](../../issues/12) videos might not have been downloaded with v0.8.0/v0.8.1 any longer. I'm terribly sorry! Files will get a `_hash2_` designation before a hopefully proper `_hash3_` comes along.

### v0.8.1 2024-02-02

Bugfix release:

- MPEG-4 FourCC codes may contain non-printable characters. The box parser can now handle that.
- Show proper error info and suggestions when invalid MPEG-4 files are encountered.

### v0.8.0 2024-01-27

Video Fix Edition

This version fixes some graving bugs in regard to video downloading:

* Ludicrous memory usage, whole MPEG-4 files were buffered to RAM using up to several gigabytes ([#8](../../issues/8))
* Manual re-muxing of MPEG streams which a) caused incompatibilites with certain media ([#9](../../issues/9)) and b) could also lead to malformed MPEG-4 files
* Hashing video files is tricky and broke due to the fix for ([#9](../../issues/9)) but was bound to unnoticeably break in the future anyway, like a timebomb

As a side effect, existing files will be re-hashed and now have a `_hash1_` part instead of `_hash_`. The front remains the same. Sorry for the inconvenience. I also have plans for a new (opt-in) shorter naming scheme using a checksum probably but that's a story for another day.

Along the way I also fixed a configuration file issue where timeline settings where not honored and a file-rename bug.

Long read:

Video files are actually split into chunks of several MPEG-TS streams in varying resolutions and a web video player can decide what to load in (adaptive streaming, DASH, whatever technology and naming). It is common to have such info in playlists using a text format called `M3U8`. So to get an MPEG-4 out of this you need to take the playlist with the highest resolution, fetch all MPEG-TS streams and merge them into an MPEG-4 file. This should be done by software written by video experts who know the standards, not by hand; Avnsx, for whatever reason, decided to re-mux the streams not only on-the-fly in RAM but also fixing DTS packet sequences by hand. People with some tech knowledge can see what all could go and went wrong with this and how I might feel about that.

First, all streams (`.ts`) must be downloaded to disk first instead of buffering all to RAM. Second, regarding concatenation/merging a web search usually ends up with the go-to tool for manipulation of audio and video files - `ffmpeg`. Thus I ended up using `pyffmpeg` which is platform-independent and downloads an appropriate `ffmpeg` binary to help with re-encoding tasks. The lib misses some fixes regarding Linux support - but I could easily launch `ffmpeg` with appropriate arguments by hand. I then use the "demuxer" concat protocol of `ffmpeg` using a concat file (that gets deleted afterwards) to properly merge all streams into an MPEG-4 file, using copy-encoding, with proper timing info and no artifacts (except the original already had problems). This results in a structurally clean `.mp4`.

Merging (concatenating) to a proper MPEG-4 file makes the file look totally different at first glance. Two vids downloaded with the old and new methods differ in file sizes and metadata info like bitrate and duration although they are essentially the same content-wise. What is more, I also discovered that all `libav*`-based software like `ffmpeg` and `PyAV` write the framework's version number into the user metadata portion of the `.mp4`. That's the timebomb I referred to, upgrade to a new library and files that would be the same suddenly differ.

Using some online articles about the essentials of the MPEG-4 format I devised a new hashing method for `.mp4` files: I exclude the so-called `moov` and `mdat` boxes (or atoms) which essentially include all varying header data/metadata like bitrate, duration and so on and also have user data (`udta`) with the `Lavf` version as a sub-part. I'm no MPEG-4 expert at all so hopefully I haven't missed something essential here - but from my tests this works beautifully. The bytes of the audio-video-content itself are the same so they hash the same 🙂.
However, since there is no way to distinguish old-style from new-style hashed files I had to introduce a marker, like a version number, `_hash1_` - and re-hash all existing old-version files on program launch including images. Although image hashing has not changed, differentiating here would have only led to a buggy, unintelligible mess.

Obviously, if a creator re-encoded existing material then the file will be totally different from a binary perspective - even though it may optically check out the same as a previous release; this would require something like a "perceptive hash" - but I still have doubts of that tech probably being too vague - and thus missing content. Therefore, after testing, I might remove pHashing from images in the future.

For more details and history see: **[Release Notes](ReleaseNotes.md)**

## 🏗️ Setup
On Windows you can just download and run the [executable version](https://github.com/prof79/fansly-downloader-ng/releases/latest) - skip the entire setup section and go directly to [Quick Start](https://github.com/prof79/fansly-downloader-ng#-quick-start).

#### Python Environment
If your operating system is not compatible with executable versions of **Fansly Downloader NG** (only Windows supported for ``.exe``) or you want to use the Python sources directly please [download and extract](https://github.com/prof79/fansly-downloader-ng/archive/refs/heads/master.zip) *or* clone the repository and ensure that [Python 3.11+](https://www.python.org/downloads/) is installed on your system.

**Note:** Using a [Python virtual environment](https://docs.python.org/3/library/venv.html) is recommended but out-of-scope of this guide.

Once Python is installed, you can then proceed by installing the required packages using [Python's package manager](https://realpython.com/what-is-pip/) ("`pip3`"/"`pip`") from your system's terminal:

    pip3 install -r requirements.txt

On Windows `pip3` is just called `pip`:

    pip install -r requirements.txt

Developers should also install `requirements-dev.txt`:

    pip3 install -r requirements-dev.txt

For Linux operating systems you may need to install the Python `Tkinter` module separately by using the command:

    sudo apt-get install python3-tk

On Windows and macOS the `Tkinter` module is typically included in the [Python installer itself](https://youtu.be/O2PzLeiBEuE?t=38).

After all requirements are met run `fansly_downloader_ng.py`.

Raw Python code versions of **Fansly Downloader NG** do not receive automatic updates. If an update is available you will be notified but need to manually download and set-up the [current repository](https://github.com/prof79/fansly-downloader-ng/archive/refs/heads/master.zip) again.

## 🚀 Quick Start
Follow these steps to quickly get started with either the [Python](https://github.com/prof79/fansly-downloader-ng#python-version-requirements) or the [Executable](https://github.com/prof79/fansly-downloader-ng/releases/latest):

1. Download the latest version of **Fansly Downloader NG** by choosing one of the options below:
   - [Windows exclusive executable version](https://github.com/prof79/fansly-downloader-ng/releases/latest) - `Fansly Downloader NG.exe`
   - [Python code version](https://github.com/prof79/fansly-downloader-ng#python-version-requirements) - `fansly_downloader_ng.py`

   and extract the files from the zip folder.

2. Ensure that you have recently logged into your Fansly account and accessed the Fansly website using one of the following web browsers: **Chrome, Firefox, Microsoft Edge, Brave, Opera, or Opera GX** on the operating systems **Windows 10/11, macOS or Linux**.

3. Open and run the ``Fansly Downloader NG.exe`` file by clicking on it or run `fansly_downloader_ng.py` from a terminal. This will initiate the interactive setup tutorial for the configuration file called [``config.ini``](https://github.com/prof79/fansly-downloader-ng/wiki/Explanation-of-provided-programs-&-their-functionality#explanation-of-configini).

4. After values for the targeted creators [Username](https://github.com/prof79/fansly-downloader-ng/blob/fc7c6734061f6b61ddf3ef3ae29618aedc21e052/config.ini#L2), your Fansly account [Authorization Token](https://github.com/prof79/fansly-downloader-ng/blob/fc7c6734061f6b61ddf3ef3ae29618aedc21e052/config.ini#L5) and your web browser's [User-Agent](https://github.com/prof79/fansly-downloader-ng/blob/fc7c6734061f6b61ddf3ef3ae29618aedc21e052/config.ini#L6) are filled you're good to go 🎉!
See the [manual set-up tutorial](https://github.com/prof79/fansly-downloader-ng/wiki/Get-Started) if anything could not be configured automatically.

Once you have completed the initial configuration of **Fansly Downloader NG**, for every future use case, you will only need to adapt the creator(s) in `Targeted Creator > Username` section in the `config.ini` using a text editor of your choice. Additional settings can also be found in the `config.ini` file, which are documented in [the Wiki](https://github.com/prof79/fansly-downloader-ng/wiki/Explanation-of-provided-programs-&-their-functionality#4-configini) page.

## 🤔 FAQ
Do you have any unanswered questions or want to know more about **Fansly Downloader NG**? Head over to the [Wiki](https://github.com/prof79/fansly-downloader-ng/wiki) or check if your topic was mentioned in [Discussions](https://github.com/prof79/fansly-downloader-ng/discussions) or [Issues](https://github.com/prof79/fansly-downloader-ng/issues)

* **Q**: "Is **Fansly Downloader NG** exclusive to Windows?"

* **A**: No, **Fansly Downloader NG** can be ran on Windows, MacOS or Linux. It's just that the executable version of the downloader, is currently only being distributed for the windows 10 & 11 operating systems. You can use **Fansly Downloader NG** from the [raw Python sources](https://github.com/prof79/fansly-downloader-ng#%EF%B8%8F-set-up) on any other operating system and it'll behave the exact same as the Windows executable version.

* **Q**: "Is it possible to download Fansly files on a mobile device?"

* **A**: Unfortunately, downloading Fansly files on a mobile device is currently not supported by **Fansly Downloader NG** or any other available means.

* **Q**: "Why do some executables show detections on them in VirusTotal?"

* **A**: The **Fansly Downloader NG** executables are not [digitally signed](https://www.digicert.com/signing/code-signing-certificates) as software certificates are very expensive. Thus the executables tend to produce a lot of false positives (invalid detections). Antivirus providers can be mailed to update their detections but not all do care.
If you're knowledgeable with the Python programming language you can decompile a [PyInstaller](https://github.com/pyinstaller/pyinstaller) executable such as **Fansly Downloader NG** using a tool like [uncompyle6](https://github.com/rocky/python-uncompyle6/) - and assure yourself that no harmful code is included. Or you could just create your own [PyInstaller](https://github.com/pyinstaller/pyinstaller) executable.

* **Q**: "Could you add X feature or do X change?"

* **A**: I'm regrettably very limited on time and thus primarily do stuff I find useful myself. You can contribute code by [opening a pull request](https://github.com/prof79/fansly-downloader-ng/pulls)

* **Q**: "Will you add any payment bypassing features to **Fansly Downloader NG**?"

* **A**: No, as the intention of this repository is not to harm Fansly or it's content creators.

+ **Q**: "Is there a possibility of being banned?"
**A**: While there are no guarantees, it's worth noting that among the 24.000+ previous users, there have been no reported incidents.

Please note that "Issue" tickets are reserved for reporting genuine or suspected bugs in the codebase of the downloader which require attention from the developer. They are not for general computer user problems.

## 🤝 Contributing to Fansly Downloader NG
Any kind of positive contribution is welcome! Please help the project improve by [opening a pull request](https://github.com/prof79/fansly-downloader-ng/pulls) with your suggested changes!

### Special Thanks
A heartfelt thank you goes out to [@liviaerxin](https://github.com/liviaerxin) for their invaluable contribution in providing the cross-platform package [plyvel](https://github.com/wbolster/plyvel). Due to [these builds](https://github.com/liviaerxin/plyvel/releases/latest) Fansly downloader NG's initial interactive cross-platform setup has become a reality.

## 🛡️ License
This project (including executables) is licensed under the GPL-3.0 License - see the [`LICENSE`](LICENSE) file for details.

## Disclaimer
"Fansly" or [fansly.com](https://fansly.com/) is operated by Select Media LLC as stated on their "Contact" page. This repository and the provided content in it isn't in any way affiliated with, sponsored by, or endorsed by Select Media LLC or "Fansly". The developer(referred to: "prof79" in the following) of this code is not responsible for the end users actions, no unlawful activities of any kind are being encouraged. Statements and processes described in this repository only represent best practice guidance aimed at fostering an effective software usage. The repository was written purely for educational purposes, in an entirely theoretical environment. Thus, any information is presented on the condition that the developer of this code shall not be held liable in no event to you or anyone else for any direct, special, incidental, indirect or consequential damages of any kind, or any damages whatsoever, including without limitation, loss of profit, loss of use, savings or revenue, or the claims of third parties, whether the developer has advised of the possibility of such loss, however caused and on any theory of liability, arising out of or in connection with the possession, use or performance of this software. The material embodied in this repository is supplied to you "as-is" and without warranty of any kind, express, implied or otherwise, including without limitation, any warranty of fitness. This code does not bypass any paywalls & no end user information is collected during usage. Finally it is important to note that this GitHub repository is the sole branch maintained and owned by the developer and any third-party websites or entities, that might refer to or be referred from it are in no way affiliated with Fansly Downloader, either directly or indirectly. This disclaimer is preliminary and is subject to revision.
