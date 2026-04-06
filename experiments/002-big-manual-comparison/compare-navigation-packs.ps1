param(
  [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path,
  [string[]]$RequiredPaths = @(
    "README.md",
    "docs/knowledge/harness-engineering-overview.md",
    "docs/plans/experiment-plan.md",
    "docs/plans/experiment-log.md"
  )
)

$measureScript = Join-Path $PSScriptRoot "..\\shared\\measure-navigation-pack.ps1"
$baselinePaths = @("AGENTS.md", "README.md")
$manualPaths = @("experiments/002-big-manual-comparison/fixtures/MEGA-MANUAL.md")

$baselineMetrics = (& $measureScript -RootPath $RepoRoot -RelativePaths $baselinePaths -RequiredPaths $RequiredPaths) | ConvertFrom-Json
$manualMetrics = (& $measureScript -RootPath $RepoRoot -RelativePaths $manualPaths -RequiredPaths $RequiredPaths) | ConvertFrom-Json

$baselineWords = [double]$baselineMetrics.summary.words
$manualWords = [double]$manualMetrics.summary.words
$baselineLines = [double]$baselineMetrics.summary.lines
$manualLines = [double]$manualMetrics.summary.lines
$baselineFirstMention = [double]$baselineMetrics.summary.first_required_mention_pack_line
$manualFirstMention = [double]$manualMetrics.summary.first_required_mention_pack_line
$baselineAverageMention = [double]$baselineMetrics.summary.average_first_mention_pack_line
$manualAverageMention = [double]$manualMetrics.summary.average_first_mention_pack_line
$baselineDensity = [double]$baselineMetrics.summary.required_path_mentions_per_100_words
$manualDensity = [double]$manualMetrics.summary.required_path_mentions_per_100_words

$wordMultiplier = $null
if ($baselineWords -gt 0) {
  $wordMultiplier = [math]::Round(($manualWords / $baselineWords), 2)
}

$lineMultiplier = $null
if ($baselineLines -gt 0) {
  $lineMultiplier = [math]::Round(($manualLines / $baselineLines), 2)
}

$firstMentionDelta = $manualFirstMention - $baselineFirstMention
$averageMentionDelta = [math]::Round(($manualAverageMention - $baselineAverageMention), 2)
$densityDelta = [math]::Round(($manualDensity - $baselineDensity), 2)

$sameCoverage = ($baselineMetrics.summary.required_paths_covered -eq $manualMetrics.summary.required_paths_covered) -and ($manualMetrics.summary.required_paths_covered -eq $RequiredPaths.Count)
$manualIsHeavier = ($null -ne $wordMultiplier) -and ($wordMultiplier -ge 3)
$manualBuriesPaths = $firstMentionDelta -ge 40
$manualHasLowerDensity = $densityDelta -lt 0

$verdict = ""
if ($sameCoverage -and $manualIsHeavier -and $manualBuriesPaths -and $manualHasLowerDensity) {
  $verdict = "giant-manual-is-functionally-complete-but-structurally-worse"
} elseif ($sameCoverage) {
  $verdict = "giant-manual-is-usable-but-inconclusive"
} else {
  $verdict = "giant-manual-loses-required-path-coverage"
}

$recommendation = ""
if ($verdict -eq "giant-manual-is-functionally-complete-but-structurally-worse") {
  $recommendation = "Keep a short top-level map, keep deep detail in linked docs, and treat giant manuals as experiment fixtures rather than production repo guidance."
} else {
  $recommendation = "Repeat the comparison with a stricter manual fixture or a second agent run."
}

[pscustomobject]@{
  generated_at = (Get-Date).ToString("o")
  baseline = $baselineMetrics
  giant_manual = $manualMetrics
  deltas = [pscustomobject]@{
    word_multiplier = $wordMultiplier
    line_multiplier = $lineMultiplier
    first_required_mention_line_delta = $firstMentionDelta
    average_first_mention_line_delta = $averageMentionDelta
    density_delta = $densityDelta
  }
  verdict = $verdict
  recommendation = $recommendation
} | ConvertTo-Json -Depth 8
