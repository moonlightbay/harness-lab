param(
  [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path,
  [string[]]$TopLevelFiles = @("AGENTS.md", "README.md"),
  [string[]]$RequiredPaths = @(
    "README.md",
    "docs/knowledge/harness-engineering-overview.md",
    "docs/plans/experiment-plan.md",
    "docs/plans/experiment-log.md"
  )
)

function Get-WordCount {
  param([string]$Text)

  if ([string]::IsNullOrWhiteSpace($Text)) {
    return 0
  }

  return ([regex]::Matches($Text.Trim(), '\S+')).Count
}

$topLevelMetrics = foreach ($relativePath in $TopLevelFiles) {
  $fullPath = Join-Path $RepoRoot $relativePath
  $content = Get-Content -Raw $fullPath
  $lineCount = (Get-Content $fullPath | Measure-Object -Line).Lines

  [pscustomobject]@{
    path = $relativePath
    lines = $lineCount
    words = Get-WordCount $content
    characters = $content.Length
    referenced_required_paths = @($RequiredPaths | Where-Object { $content.Contains($_) })
  }
}

$combinedContent = ($TopLevelFiles | ForEach-Object {
  Get-Content -Raw (Join-Path $RepoRoot $_)
}) -join "`n"

$requiredCoverage = foreach ($requiredPath in $RequiredPaths) {
  [pscustomobject]@{
    path = $requiredPath
    mentioned_in_top_level_map = $combinedContent.Contains($requiredPath)
  }
}

[pscustomobject]@{
  generated_at = (Get-Date).ToString("o")
  repo_root = $RepoRoot
  top_level_files = $topLevelMetrics
  totals = [pscustomobject]@{
    file_count = $topLevelMetrics.Count
    lines = ($topLevelMetrics | Measure-Object -Property lines -Sum).Sum
    words = ($topLevelMetrics | Measure-Object -Property words -Sum).Sum
    characters = ($topLevelMetrics | Measure-Object -Property characters -Sum).Sum
  }
  required_path_coverage = $requiredCoverage
} | ConvertTo-Json -Depth 5
