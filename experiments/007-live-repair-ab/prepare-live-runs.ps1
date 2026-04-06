$ErrorActionPreference = "Stop"

$experimentRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$runsRoot = Join-Path $experimentRoot "runs"
$fixtureRoot = Join-Path $experimentRoot "fixtures\\base-broken-workspace"
$taskSource = Join-Path $experimentRoot "task.md"

$runDefinitions = @(
    @{
        Name = "generic-check"
        Overlay = Join-Path $experimentRoot "overlays\\generic-check\\check-architecture.py"
    },
    @{
        Name = "remediation-check"
        Overlay = Join-Path $experimentRoot "overlays\\remediation-check\\check-architecture.py"
    }
)

if (Test-Path $runsRoot) {
    Remove-Item -Recurse -Force $runsRoot
}

foreach ($run in $runDefinitions) {
    $runRoot = Join-Path $runsRoot $run.Name
    $workspaceRoot = Join-Path $runRoot "workspace"

    New-Item -ItemType Directory -Path $runRoot | Out-Null
    Copy-Item -Recurse -Force $fixtureRoot $workspaceRoot
    Copy-Item -Force $run.Overlay (Join-Path $workspaceRoot "check-architecture.py")
    Copy-Item -Force $taskSource (Join-Path $workspaceRoot "TASK.md")

    git init -q $workspaceRoot | Out-Null
    git -C $workspaceRoot config user.name "harness-lab"
    git -C $workspaceRoot config user.email "lab@example.invalid"
    git -C $workspaceRoot add .
    git -C $workspaceRoot commit -qm "baseline broken workspace"
}
