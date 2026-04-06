param(
  [Parameter(Mandatory = $true)]
  [string]$WorkspaceRoot
)

$resolvedWorkspace = (Resolve-Path $WorkspaceRoot).Path
$checks = @()

function Add-Check {
  param(
    [string]$Name,
    [bool]$Passed,
    [string]$Detail
  )

  $script:checks += [pscustomobject]@{
    name = $Name
    passed = $Passed
    detail = $Detail
  }
}

$newScriptPath = Join-Path $resolvedWorkspace "scripts/generate-report.ps1"
$oldScriptPath = Join-Path $resolvedWorkspace "scripts/export-report.ps1"
$readmePath = Join-Path $resolvedWorkspace "README.md"
$testPath = Join-Path $resolvedWorkspace "tests/report-format.ps1"
$changelogPath = Join-Path $resolvedWorkspace "docs/CHANGELOG.md"

Add-Check -Name "new-script-exists" -Passed (Test-Path $newScriptPath) -Detail "Expected scripts/generate-report.ps1."
Add-Check -Name "old-script-removed" -Passed (-not (Test-Path $oldScriptPath)) -Detail "Expected scripts/export-report.ps1 to be removed."

$newScriptContent = if (Test-Path $newScriptPath) { Get-Content -Raw $newScriptPath } else { "" }
$readmeContent = if (Test-Path $readmePath) { Get-Content -Raw $readmePath } else { "" }
$testContent = if (Test-Path $testPath) { Get-Content -Raw $testPath } else { "" }
$changelogContent = if (Test-Path $changelogPath) { Get-Content -Raw $changelogPath } else { "" }

Add-Check -Name "generated-at-field" -Passed ($newScriptContent.Contains("generated_at")) -Detail "Expected generated_at field in the new script."
Add-Check -Name "item-count-field" -Passed ($newScriptContent.Contains("item_count")) -Detail "Expected item_count field in the new script."
Add-Check -Name "tests-updated" -Passed ($testContent.Contains("generate-report.ps1") -and $testContent.Contains("generated_at") -and $testContent.Contains("item_count")) -Detail "Expected tests to reference the new script and fields."
Add-Check -Name "readme-updated" -Passed ($readmeContent.Contains("generate-report.ps1")) -Detail "Expected README usage example to reference generate-report.ps1."
Add-Check -Name "changelog-updated" -Passed ($changelogContent.Contains("generate-report.ps1")) -Detail "Expected changelog entry for the refactor."

$testsPassed = $false
$testError = ""

try {
  & $testPath | Out-Null
  $testsPassed = $true
} catch {
  $testError = $_.Exception.Message
}

$testDetail = ""
if ($testsPassed) {
  $testDetail = "Tests passed."
} else {
  $testDetail = $testError
}

Add-Check -Name "tests-pass" -Passed $testsPassed -Detail $testDetail

[pscustomobject]@{
  generated_at = (Get-Date).ToString("o")
  workspace_root = $resolvedWorkspace
  checks = $checks
  summary = [pscustomobject]@{
    passed = @($checks | Where-Object { $_.passed }).Count
    total = $checks.Count
  }
} | ConvertTo-Json -Depth 5
