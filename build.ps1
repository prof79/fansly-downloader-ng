# Fansly Downloader NG Build Script

# Executable name
$name = ''

# Crude OS detection but should work multi-platform
if ((Test-Path -PathType Leaf -Path "${Env:SystemRoot}\System32\kernel32.dll"))
{
    # Windows (without extension)
    $name = 'Fansly Downloader NG'
}
else
{
    # macOS, Linux, ...
    $name = 'fansly-downloader-ng'
}

# Build
pyinstaller `
    -n $name `
    --onefile `
    --console `
    --noupx `
    --icon=resources\fansly_ng.ico `
    "$PSScriptRoot\fansly_downloader_ng.py"
