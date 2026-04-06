param(
  [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
)

$requiredPaths = @(
  "README.md",
  "docs/knowledge/harness-engineering-overview.md",
  "docs/plans/experiment-plan.md",
  "docs/plans/experiment-log.md"
)

$scoreScript = Join-Path $PSScriptRoot "score-legibility-pack.ps1"

$baseline = (& $scoreScript -PackName "baseline" -RootPath $RepoRoot -RelativePaths @("AGENTS.md", "README.md") -RequiredPaths $requiredPaths) | ConvertFrom-Json
$staleDoc = (& $scoreScript -PackName "stale-doc" -RootPath $RepoRoot -RelativePaths @("experiments/010-stale-doc-and-duplicate-guidance/fixtures/STALE-TOP-LEVEL-MAP.md") -RequiredPaths $requiredPaths) | ConvertFrom-Json
$duplicateGuidance = (& $scoreScript -PackName "duplicate-guidance" -RootPath $RepoRoot -RelativePaths @("experiments/010-stale-doc-and-duplicate-guidance/fixtures/DUPLICATE-GUIDANCE-MAP.md") -RequiredPaths $requiredPaths) | ConvertFrom-Json

$packs = @($baseline, $staleDoc, $duplicateGuidance)
$ranked = @($packs | Sort-Object { -1 * [int]$_.score.total_points }, { [int]$_.summary.words })

$fixturesKeepCoverage = (
  ([int]$staleDoc.summary.required_paths_covered -eq $requiredPaths.Count) -and
  ([int]$duplicateGuidance.summary.required_paths_covered -eq $requiredPaths.Count)
)

$baselineWins = ([int]$baseline.score.total_points -gt [int]$staleDoc.score.total_points) -and
  ([int]$baseline.score.total_points -gt [int]$duplicateGuidance.score.total_points)

$verdict = ""

if (
  $fixturesKeepCoverage -and
  $baselineWins -and
  ([int]$staleDoc.summary.unique_stale_path_count -gt 0) -and
  ([int]$duplicateGuidance.summary.authority_conflict_topic_count -gt 0)
) {
  $verdict = "coverage-alone-does-not-protect-agent-legibility"
} elseif ($baselineWins) {
  $verdict = "short-map-still-wins-but-repeat-with-a-second-fixture"
} else {
  $verdict = "comparison-inconclusive"
}

$recommendation = "Treat stale authority claims and duplicate source-of-truth claims as garbage-collection failures. A top-level map should stay short, current, and singular about which file owns each topic."

[pscustomobject]@{
  generated_at = (Get-Date).ToString("o")
  baseline = $baseline
  stale_doc = $staleDoc
  duplicate_guidance = $duplicateGuidance
  ranked_by_total_score = @(
    $ranked | ForEach-Object {
      [pscustomobject]@{
        pack_name = $_.pack_name
        total_points = $_.score.total_points
        max_points = $_.score.max_points
        verdict = $_.verdict
      }
    }
  )
  verdict = $verdict
  recommendation = $recommendation
} | ConvertTo-Json -Depth 8
