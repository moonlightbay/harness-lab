param(
  [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
)

$auditScript = Join-Path $PSScriptRoot "audit-garbage-collection.ps1"
$dirtyRoot = Join-Path $PSScriptRoot "fixtures/dirty"
$cleanRoot = Join-Path $PSScriptRoot "fixtures/clean"

$dirtyAudit = (& $auditScript -TargetRoot $dirtyRoot) | ConvertFrom-Json
$cleanAudit = (& $auditScript -TargetRoot $cleanRoot) | ConvertFrom-Json

$dirtyCategories = @($dirtyAudit.category_counts | Select-Object -ExpandProperty category)
$cleanCategories = @($cleanAudit.category_counts | Select-Object -ExpandProperty category)
$resolvedFindings = [math]::Max(([int]$dirtyAudit.total_findings - [int]$cleanAudit.total_findings), 0)
$cleanupEffectiveness = if ([int]$dirtyAudit.total_findings -gt 0) {
  [math]::Round(($resolvedFindings / [int]$dirtyAudit.total_findings) * 100, 2)
} else {
  0
}

$verdict = "inconclusive"
if (([int]$dirtyAudit.total_findings -ge 4) -and ([int]$cleanAudit.total_findings -eq 0)) {
  $verdict = "cleanup-pass-detected-and-cleared-expected-entropy"
}

$recommendation = ""
if ($verdict -eq "cleanup-pass-detected-and-cleared-expected-entropy") {
  $recommendation = "Promote the audit categories into a reusable hygiene pass for future repos."
} else {
  $recommendation = "Expand the fixture or strengthen the audit rules before relying on this pass."
}

[pscustomobject]@{
  generated_at = (Get-Date).ToString("o")
  dirty = $dirtyAudit
  clean = $cleanAudit
  delta = [pscustomobject]@{
    findings_removed = $resolvedFindings
    cleanup_effectiveness_percent = $cleanupEffectiveness
    dirty_categories = $dirtyCategories
    clean_categories = $cleanCategories
  }
  verdict = $verdict
  recommendation = $recommendation
} | ConvertTo-Json -Depth 8
