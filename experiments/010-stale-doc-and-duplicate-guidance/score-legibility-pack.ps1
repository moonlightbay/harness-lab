param(
  [Parameter(Mandatory = $true)]
  [string]$PackName,
  [Parameter(Mandatory = $true)]
  [string]$RootPath,
  [Parameter(Mandatory = $true)]
  [string[]]$RelativePaths,
  [string[]]$RequiredPaths = @(
    "README.md",
    "docs/knowledge/harness-engineering-overview.md",
    "docs/plans/experiment-plan.md",
    "docs/plans/experiment-log.md"
  )
)

$measureScript = Join-Path $PSScriptRoot "..\\shared\\measure-navigation-pack.ps1"
$navigationMetrics = (& $measureScript -RootPath $RootPath -RelativePaths $RelativePaths -RequiredPaths $RequiredPaths) | ConvertFrom-Json

$canonicalAuthorityClaims = @{
  "repository overview" = "docs/knowledge/harness-engineering-overview.md"
  "active roadmap" = "docs/plans/experiment-plan.md"
  "experiment log" = "docs/plans/experiment-log.md"
}

$lineRecords = @()

foreach ($relativePath in $RelativePaths) {
  $fullPath = Join-Path $RootPath $relativePath
  $lines = @(Get-Content $fullPath)

  for ($i = 0; $i -lt $lines.Count; $i++) {
    $lineRecords += [pscustomobject]@{
      file = $relativePath
      line_number = $i + 1
      text = $lines[$i]
    }
  }
}

$pathMentions = @()

foreach ($record in $lineRecords) {
  $matches = [regex]::Matches($record.text, '`([^`]+\.md)`')

  foreach ($match in $matches) {
    $relativePath = $match.Groups[1].Value
    $exists = Test-Path (Join-Path $RootPath $relativePath)

    $pathMentions += [pscustomobject]@{
      path = $relativePath
      exists = $exists
      file = $record.file
      line_number = $record.line_number
    }
  }
}

$uniqueStalePaths = @(
  $pathMentions |
    Where-Object { -not $_.exists } |
    Select-Object -ExpandProperty path -Unique
)

$authorityClaims = @()

foreach ($record in $lineRecords) {
  $match = [regex]::Match(
    $record.text,
    'Source of truth for (?<topic>[^:]+): `(?<path>[^`]+\.md)`',
    [System.Text.RegularExpressions.RegexOptions]::IgnoreCase
  )

  if ($match.Success) {
    $topic = $match.Groups["topic"].Value.Trim().ToLowerInvariant()
    $path = $match.Groups["path"].Value
    $expectedPath = $null

    if ($canonicalAuthorityClaims.ContainsKey($topic)) {
      $expectedPath = $canonicalAuthorityClaims[$topic]
    }

    $authorityClaims += [pscustomobject]@{
      topic = $topic
      path = $path
      exists = Test-Path (Join-Path $RootPath $path)
      expected_path = $expectedPath
      is_expected = ($null -ne $expectedPath) -and ($path -eq $expectedPath)
      file = $record.file
      line_number = $record.line_number
    }
  }
}

$wrongAuthorityTopics = @(
  $authorityClaims |
    Where-Object { ($null -ne $_.expected_path) -and (-not $_.is_expected) } |
    Select-Object -ExpandProperty topic -Unique
)

$authorityConflictTopics = @()

if ($authorityClaims.Count -gt 0) {
  $authorityGroups = $authorityClaims | Group-Object -Property topic

  foreach ($group in $authorityGroups) {
    $distinctPaths = @($group.Group | Select-Object -ExpandProperty path -Unique)

    if ($distinctPaths.Count -gt 1) {
      $authorityConflictTopics += [pscustomobject]@{
        topic = $group.Name
        paths = $distinctPaths
      }
    }
  }
}

$coveragePoints = [int]$navigationMetrics.summary.required_paths_covered
$freshnessPoints = [math]::Max(0, 4 - (2 * $uniqueStalePaths.Count))
$authorityPoints = [math]::Max(0, 4 - $wrongAuthorityTopics.Count - $authorityConflictTopics.Count)
$totalScore = $coveragePoints + $freshnessPoints + $authorityPoints

$findingTags = @()

if ([int]$navigationMetrics.summary.required_paths_covered -lt $RequiredPaths.Count) {
  $findingTags += "missing-required-paths"
}

if ($uniqueStalePaths.Count -gt 0) {
  $findingTags += "stale-references"
}

if ($wrongAuthorityTopics.Count -gt 0) {
  $findingTags += "wrong-authority"
}

if ($authorityConflictTopics.Count -gt 0) {
  $findingTags += "conflicting-authority"
}

if ($findingTags.Count -eq 0) {
  $findingTags += "clean"
}

$verdict = ""

if ($findingTags -contains "clean") {
  $verdict = "clean-short-map"
} elseif (($findingTags -contains "stale-references") -and ($findingTags -contains "wrong-authority")) {
  $verdict = "stale-doc-preserves-coverage-but-points-to-dead-authority"
} elseif ($findingTags -contains "conflicting-authority") {
  $verdict = "duplicate-guidance-preserves-coverage-but-creates-ambiguity"
} elseif ($findingTags -contains "missing-required-paths") {
  $verdict = "pack-loses-required-navigation-context"
} else {
  $verdict = "pack-is-usable-but-higher-risk"
}

[pscustomobject]@{
  generated_at = (Get-Date).ToString("o")
  pack_name = $PackName
  relative_paths = $RelativePaths
  score = [pscustomobject]@{
    coverage_points = $coveragePoints
    freshness_points = $freshnessPoints
    authority_points = $authorityPoints
    total_points = $totalScore
    max_points = 12
  }
  summary = [pscustomobject]@{
    required_paths_covered = [int]$navigationMetrics.summary.required_paths_covered
    required_path_count = [int]$navigationMetrics.summary.required_path_count
    words = [int]$navigationMetrics.summary.words
    lines = [int]$navigationMetrics.summary.lines
    unique_stale_path_count = $uniqueStalePaths.Count
    authority_claim_count = $authorityClaims.Count
    wrong_authority_topic_count = $wrongAuthorityTopics.Count
    authority_conflict_topic_count = $authorityConflictTopics.Count
  }
  unique_stale_paths = $uniqueStalePaths
  wrong_authority_topics = $wrongAuthorityTopics
  authority_conflicts = $authorityConflictTopics
  finding_tags = $findingTags
  verdict = $verdict
  navigation_metrics = $navigationMetrics
} | ConvertTo-Json -Depth 8
