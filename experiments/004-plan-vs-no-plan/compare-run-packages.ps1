param()

$scoreScript = Join-Path $PSScriptRoot "score-run-package.ps1"
$noPlanRoot = Join-Path $PSScriptRoot "runs/no-plan"
$withPlanRoot = Join-Path $PSScriptRoot "runs/with-plan"

$noPlan = (& $scoreScript -RunRoot $noPlanRoot) | ConvertFrom-Json
$withPlan = (& $scoreScript -RunRoot $withPlanRoot) | ConvertFrom-Json

$resultDelta = [int]$withPlan.result_quality.score - [int]$noPlan.result_quality.score
$restartDelta = [int]$withPlan.restartability.score - [int]$noPlan.restartability.score
$auditDelta = [int]$withPlan.auditability.score - [int]$noPlan.auditability.score
$totalDelta = [int]$withPlan.total.score - [int]$noPlan.total.score

$verdict = "inconclusive"
if (($restartDelta -gt 0) -and ($auditDelta -gt 0) -and ($resultDelta -ge 0)) {
  $verdict = "plan-driven-run-is-easier-to-resume-and-audit"
}

$recommendation = ""
if ($verdict -eq "plan-driven-run-is-easier-to-resume-and-audit") {
  $recommendation = "Use a checked-in execution plan for multi-step refactors that may need review, restart, or handoff."
} else {
  $recommendation = "Repeat the comparison with a stronger task or stricter scoring rubric."
}

[pscustomobject]@{
  generated_at = (Get-Date).ToString("o")
  no_plan = $noPlan
  with_plan = $withPlan
  deltas = [pscustomobject]@{
    result_quality = $resultDelta
    restartability = $restartDelta
    auditability = $auditDelta
    total = $totalDelta
  }
  verdict = $verdict
  recommendation = $recommendation
} | ConvertTo-Json -Depth 8
