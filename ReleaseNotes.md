# Fansly Downloader NG

## 🗒️ Release Notes

### v0.7.4 2023-11-18

This should fix the [download problem of M3U8 files](#2) when there is no audio stream for example. The code is now more robust and can detect/skip/warn when there are lists with neither audio nor video.

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
