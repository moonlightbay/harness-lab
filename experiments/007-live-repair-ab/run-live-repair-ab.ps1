$ErrorActionPreference = "Stop"

$experimentRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$artifactsRoot = Join-Path $experimentRoot "artifacts"
$runsRoot = Join-Path $experimentRoot "runs"
$promptPath = Join-Path $experimentRoot "prompts\\live-repair.txt"
$prepareScript = Join-Path $experimentRoot "prepare-live-runs.ps1"
$scoreScript = Join-Path $experimentRoot "score-live-run.py"
$compareScript = Join-Path $experimentRoot "compare-live-runs.py"

if (Test-Path $artifactsRoot) {
    Remove-Item -Recurse -Force $artifactsRoot
}
New-Item -ItemType Directory -Force -Path $artifactsRoot | Out-Null

& $prepareScript

$runNames = @("generic-check", "remediation-check")
$prompt = Get-Content -Raw $promptPath

foreach ($runName in $runNames) {
    $workspaceRoot = Join-Path $runsRoot "$runName\\workspace"
    $eventsPath = Join-Path $artifactsRoot "$runName-events.jsonl"
    $finalMessagePath = Join-Path $artifactsRoot "$runName-final.txt"
    $scorePath = Join-Path $artifactsRoot "$runName-score.json"
    $diffPath = Join-Path $artifactsRoot "$runName-diff.txt"

    codex exec `
        -m gpt-5.4 `
        -c model_reasoning_effort='"high"' `
        --dangerously-bypass-approvals-and-sandbox `
        --json `
        -o $finalMessagePath `
        -C $workspaceRoot `
        "$prompt" | Set-Content -Encoding utf8 $eventsPath

    if ($LASTEXITCODE -ne 0) {
        throw "codex exec failed for $runName with exit code $LASTEXITCODE"
    }

    python $scoreScript $workspaceRoot $eventsPath | Set-Content -Encoding utf8 $scorePath
    git -C $workspaceRoot diff --name-only HEAD | Set-Content -Encoding utf8 $diffPath
}

python $compareScript | Set-Content -Encoding utf8 (Join-Path $artifactsRoot "live-comparison.json")
