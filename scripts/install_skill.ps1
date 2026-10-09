[CmdletBinding()]
param(
    [string]$Destination = $(if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills\music-pal' } else { Join-Path $env:USERPROFILE '.codex\skills\music-pal' }),
    [ValidateSet('Junction', 'Copy')][string]$Mode = 'Junction'
)
$ErrorActionPreference = 'Stop'
$source = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\skills\music-pal'))
$destinationPath = [IO.Path]::GetFullPath($Destination)
if (-not (Test-Path -LiteralPath (Join-Path $source 'SKILL.md') -PathType Leaf)) {
    throw "Missing source skill: $source"
}
if ($destinationPath.TrimEnd('\') -eq $source.TrimEnd('\') -or
    $destinationPath.StartsWith($source.TrimEnd('\') + '\', [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Destination must not be the source skill or a child of it.'
}
$markerName = '.music-pal-install.json'
$existing = Get-Item -LiteralPath $destinationPath -Force -ErrorAction SilentlyContinue
if ($null -ne $existing) {
    if ($existing.Attributes -band [IO.FileAttributes]::ReparsePoint) {
        $targets = @($existing.Target)
        if ($targets.Count -eq 1 -and
            [IO.Path]::GetFullPath($targets[0]).TrimEnd('\') -eq $source.TrimEnd('\')) {
            if ($Mode -ne 'Junction') { throw 'Existing junction: use Junction mode or choose another destination.' }
            Write-Output "Already installed: $destinationPath -> $source"
            return
        }
        throw "Refusing to replace unrelated link: $destinationPath"
    }
    if ($Mode -eq 'Junction') { throw "Refusing to replace existing directory: $destinationPath" }
    $marker = Join-Path $destinationPath $markerName
    if (-not (Test-Path -LiteralPath $marker -PathType Leaf)) {
        throw "Refusing to overwrite unrelated skill: $destinationPath"
    }
    $owner = Get-Content -LiteralPath $marker -Raw | ConvertFrom-Json
    if ($owner.owner -ne 'MusicPal installer' -or $owner.source -ne $source) {
        throw "Refusing to overwrite unrelated skill: $destinationPath"
    }
}
$parent = Split-Path -Parent $destinationPath
New-Item -ItemType Directory -Path $parent -Force | Out-Null
if ($Mode -eq 'Junction') {
    New-Item -ItemType Junction -Path $destinationPath -Target $source | Out-Null
    Write-Output "Installed junction: $destinationPath -> $source"
} else {
    New-Item -ItemType Directory -Path $destinationPath -Force | Out-Null
    Get-ChildItem -LiteralPath $source -Force | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination $destinationPath -Recurse -Force
    }
    @{ owner = 'MusicPal installer'; source = $source } | ConvertTo-Json |
        Set-Content -LiteralPath (Join-Path $destinationPath $markerName) -Encoding UTF8
    Write-Output "Installed copy: $destinationPath"
}
