# Fansly Downloader NG Build Script

[CmdletBinding()]

[OutputType()]

Param(
    [Parameter(Mandatory = $false, HelpMessage = 'The name of the executable to generate without extension')]
    [string]
    $BaseName
)

# Executable name
$name = ''

# If name provided by automated build workflow, use it.
if (-not [String]::IsNullOrEmpty($BaseName))
{
    $name = $BaseName
}
# Crude OS detection but should work multi-platform
elseif ((Test-Path -PathType Leaf -Path "${Env:SystemRoot}\System32\kernel32.dll"))
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
