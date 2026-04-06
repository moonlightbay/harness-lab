param(
  [Parameter(Mandatory = $true)]
  [string]$RunRoot
)

$resolvedRun = (Resolve-Path $RunRoot).Path
$workspaceRoot = Join-Path $resolvedRun "workspace"
$verifyScript = Join-Path $PSScriptRoot "verify-workspace.ps1"
$workspaceScore = (& $verifyScript -WorkspaceRoot $workspaceRoot) | ConvertFrom-Json

$planPath = Join-Path $resolvedRun "PLANS.md"
$progressPath = Join-Path $resolvedRun "notes/progress.md"
$summaryPath = Join-Path $resolvedRun "notes/run-summary.md"
$decisionLogPath = Join-Path $resolvedRun "notes/decision-log.md"
$verificationPath = Join-Path $resolvedRun "notes/verification.md"
$scratchpadPath = Join-Path $resolvedRun "notes/scratchpad.md"

$summaryContent = if (Test-Path $summaryPath) { Get-Content -Raw $summaryPath } else { "" }
$progressContent = if (Test-Path $progressPath) { Get-Content -Raw $progressPath } else { "" }
$planContent = if (Test-Path $planPath) { Get-Content -Raw $planPath } else { "" }
$verificationContent = if (Test-Path $verificationPath) { Get-Content -Raw $verificationPath } else { "" }
$decisionContent = if (Test-Path $decisionLogPath) { Get-Content -Raw $decisionLogPath } else { "" }
$scratchpadContent = if (Test-Path $scratchpadPath) { Get-Content -Raw $scratchpadPath } else { "" }

$resultChecks = @(
  [pscustomobject]@{ name = "new-script-exists"; passed = ($workspaceScore.checks | Where-Object { $_.name -eq "new-script-exists" }).passed },
  [pscustomobject]@{ name = "old-script-removed"; passed = ($workspaceScore.checks | Where-Object { $_.name -eq "old-script-removed" }).passed },
  [pscustomobject]@{ name = "generated-at-field"; passed = ($workspaceScore.checks | Where-Object { $_.name -eq "generated-at-field" }).passed },
  [pscustomobject]@{ name = "item-count-field"; passed = ($workspaceScore.checks | Where-Object { $_.name -eq "item-count-field" }).passed },
  [pscustomobject]@{ name = "tests-updated"; passed = ($workspaceScore.checks | Where-Object { $_.name -eq "tests-updated" }).passed },
  [pscustomobject]@{ name = "readme-updated"; passed = ($workspaceScore.checks | Where-Object { $_.name -eq "readme-updated" }).passed },
  [pscustomobject]@{ name = "changelog-updated"; passed = ($workspaceScore.checks | Where-Object { $_.name -eq "changelog-updated" }).passed }
)

$restartChecks = @(
  [pscustomobject]@{ name = "plan-exists"; passed = (Test-Path $planPath) },
  [pscustomobject]@{ name = "status-recorded"; passed = ($planContent.Contains("Status") -or $progressContent.Contains("Status")) },
  [pscustomobject]@{ name = "changed-work-recorded"; passed = ($planContent.Contains("Changed files") -or $summaryContent.Contains("Changed files") -or $progressContent.Contains("Changed files")) },
  [pscustomobject]@{ name = "next-step-or-risk-recorded"; passed = ($planContent.Contains("Next") -or $planContent.Contains("Remaining") -or $summaryContent.Contains("Next") -or $progressContent.Contains("Remaining")) },
  [pscustomobject]@{ name = "verification-status-recorded"; passed = ((Test-Path $verificationPath) -or $scratchpadContent.Contains("tests passed")) }
)

$auditChecks = @(
  [pscustomobject]@{ name = "decision-log-exists"; passed = (Test-Path $decisionLogPath) },
  [pscustomobject]@{ name = "verification-log-exists"; passed = (Test-Path $verificationPath) },
  [pscustomobject]@{ name = "commands-recorded"; passed = ($verificationContent.Contains("Commands") -or $scratchpadContent.Contains("pwsh")) },
  [pscustomobject]@{ name = "assumptions-recorded"; passed = ($planContent.Contains("Assumptions") -or $decisionContent.Contains("Assumptions")) }
)

$resultScore = @($resultChecks | Where-Object { $_.passed }).Count
$restartScore = @($restartChecks | Where-Object { $_.passed }).Count
$auditScore = @($auditChecks | Where-Object { $_.passed }).Count
$totalScore = $resultScore + $restartScore + $auditScore

[pscustomobject]@{
  generated_at = (Get-Date).ToString("o")
  run_root = $resolvedRun
  result_quality = [pscustomobject]@{
    score = $resultScore
    max = $resultChecks.Count
    checks = $resultChecks
  }
  restartability = [pscustomobject]@{
    score = $restartScore
    max = $restartChecks.Count
    checks = $restartChecks
  }
  auditability = [pscustomobject]@{
    score = $auditScore
    max = $auditChecks.Count
    checks = $auditChecks
  }
  total = [pscustomobject]@{
    score = $totalScore
    max = ($resultChecks.Count + $restartChecks.Count + $auditChecks.Count)
  }
  workspace_verification = $workspaceScore
} | ConvertTo-Json -Depth 8
