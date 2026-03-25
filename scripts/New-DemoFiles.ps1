param(
    [string]$OutputDirectory = "demo-files"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$targetDirectory = Join-Path $repoRoot $OutputDirectory

New-Item -ItemType Directory -Path $targetDirectory -Force | Out-Null

$files = @(
    @{
        Name = "release-notes.txt"
        Content = @"
VaultFlow Release Notes

- Added expiring share links
- Added streamed upload/download paths
- Added workspace metrics and audit history
"@
    },
    @{
        Name = "customer-export.csv"
        Content = @"
account_id,region,plan,status
1001,us-west,enterprise,active
1002,us-east,growth,active
1003,eu-central,starter,pending
"@
    },
    @{
        Name = "architecture-notes.md"
        Content = @"
# VaultFlow Demo Notes

- Backend: Flask app factory with versioned blueprints
- Frontend: Vue 3 + Vite control plane
- Storage: user-scoped files with SQLite metadata
- Sharing: expiring public tokens with revocation
"@
    }
)

foreach ($file in $files) {
    $path = Join-Path $targetDirectory $file.Name
    Set-Content -Path $path -Value $file.Content -Encoding UTF8
}

Write-Host "Demo files created in $targetDirectory"
