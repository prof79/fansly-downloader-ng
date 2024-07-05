# Fansly Downloader NG

## 🗒️ Release Notes

### v0.9.10 2024-06-28

Posts batch downloading ([#63](https://github.com/prof79/fansly-downloader-ng/issues/63)) kudos @1gintonic

### v0.9.9 2024-06-28

Accept URLs/be less picky when specifying single posts ([#64](https://github.com/prof79/fansly-downloader-ng/issues/64)) kudos @1gintonic

### v0.9.8 2024-06-28

Download menu in interactive mode ([#58](https://github.com/prof79/fansly-downloader-ng/issues/58)) kudos @1gintonic

### v0.9.7 2024-03-22

Fix for update checks (hopefully) and disabled SSL verification for WebSockets due to a specific issue.
Things are complicated for you now, check key must be deciphered by evaluating a `JavaScript` expression.

### v0.9.6 2024-03-22

Yay! I coded automatic retrieval of the check key from Fansly's page. Fallback to user input if it fails.
Should the need arise the patterns for locating the JS file and check key are saved/loaded in the `[Logic]` section in `config.ini`.

### v0.9.5 2024-03-22

Fixed headless/non-interactive input blooper during "check key" validation.

### v0.9.4 2024-03-22

Fix `check_key` setting in `config.ini` not honored.

### v0.9.3 2024-03-19

Be warned, Fansly may ban you using this! If you get errors be careful not to challenge your luck/try too often.

Well, stupid me, being overworked and tired, forgot to put an essential function call in after successful testing was complete!
Seems to work again, for now - I hope ...

### v0.9.2 2024-03-19

Be warned, Fansly may ban you using this!

I've made the `_checkKey` configurable but don't expect this to work any more - it feels they have done more like invalidating (changing) authorization tokens and I'm probably be done with this and unsubscribe from my paid creators and I suggest you do the same.

Fansly totally lacks imagination of legit use cases like using VR where a proper media player experience requires a local library.

### v0.9.1 2024-03-19

Well, helluva ride - Fansly stepped up their security game and only allow properly constructed web calls from now on or the results will come out empty.

I've totally rewritten almost all web calls into a separate Fansly API class that handles all the wild details with a a lot of foundation functions the more specific ones build upon, like a pyramid.

Long story short it should work again now 😊 I've tested my standard set of creators plus an empty-config alternate-browser set of creators with public content I do not follow. However, after those graving changes some bugs might linger - create an [issue](../../issues/) should you encounter something out of the ordinary.

### v0.8.21 2024-03-15

Be more precise with errors when potential Fansly API error happen.

### v0.8.20 2024-03-15

Changed wording to `update recommended` instead of `update required`.

### v0.8.19 2024-03-15

Kudos to [sunbart](https://github.com/sunbart) who contributed a switch to hide skipped item messages in PR #26 - meaning less clutter for those running headless and relying on the logs.
There are one or two caveats and I'll try to improve on them later.

And sorry, v0.8.18 docs had a wrong datestamp.

### v0.8.18 2024-03-15

Ubuntu 22.04 support for built-in Python by [XelaRellum](https://github.com/XelaRellum). Kudos!

### v0.8.17 2024-02-18

Better error handling to diagnose another [M3U8 error](../../issues/23).

### v0.8.16 2024-02-17

Hopefully finally fix [#7](../../issues/7).

### v0.8.12-15 2024-02-17

Self updater testing. Automatic updating disabled, this is too complicated as of now. ([#21](../../issues/21))

### v0.8.11 2024-02-17

A fix for the [self updater](../../issues/21).

### v0.8.10 2024-02-17

Fixed another stupid [memory bug](../../issues/14) and discovered and fixed some hashing inconsistencies during on-the-fly dedupe along the way.

### v0.8.9 2024-02-17

Removed the weird [file hierarchy checks](../../issues/7).

### v0.8.8 2024-02-17

Fix corner cases discussed in [#17](../../issues/17), go to 1080p as a last resort and fetch M3U8s recursively.

### v0.8.7 2024-02-15

This should hopefully fix [#18](../../issues/18).

### v0.8.6 2024-02-15

This primarily fixes [video download issue #17](../../issues/17) but I also made sure [#21 workaround](../../issues/21) only applies to Linux as I had a bad experience on my Windows machine with an old ImageMagick including old ffmpeg installed, not working with concat at all.

### v0.8.5 2024-02-14

Workaround for [Linux issue #20](../../issues/20) thanks to [FletcherD](https://github.com/FletcherD).

### v0.8.4 2024-02-02

Program version number for v0.8.3 still showed v0.8.2. Version number corrected, no code changes.

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

### v0.7.10 2024-01-05

Binary release fixing the [missing media downloads issue #3](../../issues/3). Thanks to all participants!
Also fixes a statistics message counting bug.
Summary release for v0.7.7-v0.7.9, no code changes in this one.

### v0.7.9 2024-01-04

Fixed statistics message counting bug.

### v0.7.8 2024-01-04

Safe dictionary access for media info access in Fansly objects.

### v0.7.7 2024-01-04

Preliminary release of missing items fix.

### v0.7.6 2024-01-02

Thanks to [@icewinterberry12](https://github.com/icewinterberry12) a Fansly API size limitation was uncovered and fixed by them. Kudos!
Further research required whether this also fixes issues other people are having or not.

Compared to v0.7.5 I added some error handling for batching and did minor restructuring myself.

### v0.7.5 2024-01-02

Thanks to [@icewinterberry12](https://github.com/icewinterberry12) a Fansly API size limitation was uncovered and fixed by them. Kudos!
Further research required whether this also fixes issues other people are having or not.

### v0.7.4 2023-11-18

This should fix the [download problem of M3U8 files](../../issues/2) when there is no audio stream for example. The code is now more robust and can detect/skip/warn when there are lists with neither audio nor video.

Please note that there are still issues with the macOS and Ubuntu builds though Ubuntu *should* work now (generic Linux being a totally different story). Actually I wanted to make a separate announcement about multi-OS releases but I'll do that in the future after more testing. 🙂

### v0.7.3 2023-11-11

This is a huge step - **Fansly Downloader NG** now has a binary download release for Windows and can be built automatically! 😁🎉

As a minor change, now also prints the program version number below the logo.

### v0.7.0 2023-11-11

* Vast improvements regarding statistics output
  * list total counts of items
  * include message item counts
  * show the number of missing items, potentially indicating a problem (timeline + messages - downloads - skipped)
  * show a grand total of all creators' downloads at the end of the program
  * show session duration info per creator and total
  * implemeinting this I found the "low-yield" calculations to be faulty - this is now handled differently based on missing items during the statistics output

### v0.6.0 2023-11-10

* Make anti-rate-limiting measures for timeline downloads configurable:
  * Configure number of timeline retries (`--timeline-retries` or `timeline_retries` in `config.ini`)
  * Configure delay in seconds between retries (`--timeline-delay-seconds` or `timeline_delay_seconds` in `config.ini`)
  * Thus you can experiment and try to lower your download session duration. The defaults of `1` retry with a delay of `60` seconds should work all the time but also delay unnecessarily at the proper end of a creator's timeline. You can calculate the minimum duration of a download session (without download time and rate-limiting retries) yourself: `NUMBER_OF_CREATORS * TIMELINE_RETRIES * TIMELINE_DELAY_SECONDS`

### v0.5.* 2023-09

The major rewrite from a single Python script to a more functional, modular, maintanable codebase!

* Full command-line support for all options
* `config.ini` not required to start the program anymore - a `config.ini` with all program defaults will be generated automatically
* Support for minimal `config.ini` files - missing options will be added from program defaults automatically
* True multi-user support - put one or more creators as a list into `config.ini` (`username = creator1, creator2, creator3`) or supply via command-line
* Run it in non-interactive mode (`-ni`) without any user intervention - eg. when downloading while being away from the computer
* You may also run it in fully silent mode without the close prompt at the very end (`-ni -npox`) - eg. running **Fansly Downloader NG** from another script or from a scheduled task/cron job
* Logs all relevant messages (`Info`, `Warning`, `Error`, ...) of the last few sessions to `fansly_downloader_ng.log`. A history of 5 log files with a maximum size of 1 MiB will be preserved and can be deleted at your own discretion.
* Easier-to-extend, modern, modular and robust codebase
* It doesn't care about starring the repository

Also see [my notes on the rewrite process](RewriteNotes.md).
