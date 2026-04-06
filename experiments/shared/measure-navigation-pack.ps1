param(
  [Parameter(Mandatory = $true)]
  [string]$RootPath,
  [Parameter(Mandatory = $true)]
  [string[]]$RelativePaths,
  [string[]]$RequiredPaths = @()
)

function Get-WordCount {
  param([string]$Text)

  if ([string]::IsNullOrWhiteSpace($Text)) {
    return 0
  }

  return ([regex]::Matches($Text.Trim(), '\S+')).Count
}

$packFiles = @()
$packLineCursor = 1

foreach ($relativePath in $RelativePaths) {
  $fullPath = Join-Path $RootPath $relativePath
  $content = Get-Content -Raw $fullPath
  $lines = @(Get-Content $fullPath)
  $lineCount = $lines.Count

  $packFiles += [pscustomobject]@{
    path = $relativePath
    lines = $lineCount
    words = Get-WordCount $content
    characters = $content.Length
    pack_line_start = $packLineCursor
    pack_line_end = if ($lineCount -gt 0) { $packLineCursor + $lineCount - 1 } else { $packLineCursor }
    referenced_required_paths = @($RequiredPaths | Where-Object { $content.Contains($_) })
    content = $content
    line_items = $lines
  }

  $packLineCursor += if ($lineCount -gt 0) { $lineCount } else { 1 }
}

$requiredPathCoverage = foreach ($requiredPath in $RequiredPaths) {
  $mentions = @()

  foreach ($file in $packFiles) {
    for ($i = 0; $i -lt $file.line_items.Count; $i++) {
      if ($file.line_items[$i].Contains($requiredPath)) {
        $mentions += [pscustomobject]@{
          file = $file.path
          line_in_file = $i + 1
          pack_line = $file.pack_line_start + $i
        }
      }
    }
  }

  $firstMention = $mentions | Sort-Object pack_line | Select-Object -First 1

  [pscustomobject]@{
    path = $requiredPath
    mentioned_in_pack = $mentions.Count -gt 0
    mention_count = $mentions.Count
    first_mention_file = if ($null -ne $firstMention) { $firstMention.file } else { $null }
    first_mention_line_in_file = if ($null -ne $firstMention) { $firstMention.line_in_file } else { $null }
    first_mention_pack_line = if ($null -ne $firstMention) { $firstMention.pack_line } else { $null }
  }
}

$coveredPaths = @($requiredPathCoverage | Where-Object { $_.mentioned_in_pack })
$missingPaths = @($requiredPathCoverage | Where-Object { -not $_.mentioned_in_pack } | Select-Object -ExpandProperty path)
$firstMentionLines = @($coveredPaths | Select-Object -ExpandProperty first_mention_pack_line)
$totalWords = ($packFiles | Measure-Object -Property words -Sum).Sum
$totalMentions = ($requiredPathCoverage | Measure-Object -Property mention_count -Sum).Sum

[pscustomobject]@{
  generated_at = (Get-Date).ToString("o")
  root_path = $RootPath
  relative_paths = $RelativePaths
  files = @($packFiles | ForEach-Object {
    [pscustomobject]@{
      path = $_.path
      lines = $_.lines
      words = $_.words
      characters = $_.characters
      pack_line_start = $_.pack_line_start
      pack_line_end = $_.pack_line_end
      referenced_required_paths = $_.referenced_required_paths
    }
  })
  summary = [pscustomobject]@{
    file_count = $packFiles.Count
    lines = ($packFiles | Measure-Object -Property lines -Sum).Sum
    words = $totalWords
    characters = ($packFiles | Measure-Object -Property characters -Sum).Sum
    required_path_count = $RequiredPaths.Count
    required_paths_covered = $coveredPaths.Count
    required_coverage_rate = if ($RequiredPaths.Count -gt 0) {
      [math]::Round(($coveredPaths.Count / $RequiredPaths.Count), 2)
    } else {
      0
    }
    first_required_mention_pack_line = if ($firstMentionLines.Count -gt 0) {
      ($firstMentionLines | Measure-Object -Minimum).Minimum
    } else {
      $null
    }
    average_first_mention_pack_line = if ($firstMentionLines.Count -gt 0) {
      [math]::Round(($firstMentionLines | Measure-Object -Average).Average, 2)
    } else {
      $null
    }
    total_required_path_mentions = $totalMentions
    required_path_mentions_per_100_words = if ($totalWords -gt 0) {
      [math]::Round((($totalMentions / $totalWords) * 100), 2)
    } else {
      0
    }
    missing_required_paths = $missingPaths
  }
  required_path_coverage = $requiredPathCoverage
} | ConvertTo-Json -Depth 6
