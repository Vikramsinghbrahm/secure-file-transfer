param(
    [switch]$BackendOnly,
    [switch]$FrontendOnly
)

$ErrorActionPreference = "Stop"

if ($BackendOnly -and $FrontendOnly) {
    throw "Use only one of -BackendOnly or -FrontendOnly."
}

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendDir = Join-Path $repoRoot "backend"
$frontendDir = Join-Path $repoRoot "frontend"
$backendPython = Join-Path $backendDir "venv\Scripts\python.exe"
$frontendNodeModules = Join-Path $frontendDir "node_modules"
$backendPort = 5001

function Assert-PathExists {
    param(
        [string]$Path,
        [string]$Message
    )

    if (-not (Test-Path $Path)) {
        throw $Message
    }
}

function Start-WorkspaceProcess {
    param(
        [string]$Name,
        [string]$WorkingDirectory,
        [string]$Command
    )

    $arguments = @(
        "-NoExit",
        "-Command",
        "Set-Location '$WorkingDirectory'; $Command"
    )

    $process = Start-Process `
        -FilePath "powershell.exe" `
        -WorkingDirectory $WorkingDirectory `
        -ArgumentList $arguments `
        -PassThru

    Write-Host "$Name started in a new PowerShell window (PID $($process.Id))."
}

if (-not $FrontendOnly) {
    Assert-PathExists `
        -Path $backendPython `
        -Message "Backend virtualenv not found at '$backendPython'. Create it first with 'python -m venv backend\venv' and install requirements."

    Start-WorkspaceProcess `
        -Name "Backend" `
        -WorkingDirectory $backendDir `
        -Command "`$env:PORT='$backendPort'; & '$backendPython' run.py"
}

if (-not $BackendOnly) {
    Assert-PathExists `
        -Path $frontendNodeModules `
        -Message "Frontend dependencies not found at '$frontendNodeModules'. Run 'npm install' inside the frontend directory first."

    Start-WorkspaceProcess `
        -Name "Frontend" `
        -WorkingDirectory $frontendDir `
        -Command "npm run dev"
}

Write-Host ""
if (-not $FrontendOnly) {
    Write-Host "Backend URL : http://localhost:$backendPort"
}
if (-not $BackendOnly) {
    Write-Host "Frontend URL: http://localhost:8081"
}
