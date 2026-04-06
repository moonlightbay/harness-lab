param(
  [Parameter(Mandatory = $true)]
  [string]$TargetRoot
)

function Add-Finding {
  param(
    [ref]$Bucket,
    [string]$Category,
    [string]$Message,
    [string[]]$Paths = @()
  )

  $Bucket.Value += [pscustomobject]@{
    category = $Category
    message = $Message
    paths = $Paths
  }
}

function Get-BulletItemsFromSection {
  param(
    [string[]]$Lines,
    [string]$SectionHeader
  )

  $items = @()
  $inSection = $false

  foreach ($line in $Lines) {
    $trimmed = $line.Trim()

    if (-not $inSection) {
      if ($trimmed -eq $SectionHeader) {
        $inSection = $true
      }
      continue
    }

    if ($trimmed -eq "") {
      if ($items.Count -gt 0) {
        break
      }
      continue
    }

    if ($trimmed.StartsWith("- ")) {
      if ($trimmed -match '`([^`]+)`') {
        $items += $matches[1]
      } else {
        $items += $trimmed.Substring(2).Trim()
      }
      continue
    }

    if ($items.Count -gt 0) {
      break
    }
  }

  return $items
}

$resolvedTarget = (Resolve-Path $TargetRoot).Path
$findings = @()

$experimentsReadmePath = Join-Path $resolvedTarget "experiments/README.md"
if (Test-Path $experimentsReadmePath) {
  $experimentsReadmeLines = Get-Content $experimentsReadmePath
  $currentExperiments = @(Get-BulletItemsFromSection -Lines $experimentsReadmeLines -SectionHeader "Current experiments:")
  $plannedExperiments = @(Get-BulletItemsFromSection -Lines $experimentsReadmeLines -SectionHeader "Planned next experiments:")
  $overlap = @($currentExperiments | Where-Object { $plannedExperiments -contains $_ })

  if ($overlap.Count -gt 0) {
    Add-Finding -Bucket ([ref]$findings) -Category "planned-current-overlap" -Message "Experiments are listed as both current and planned." -Paths $overlap
  }
}

$experimentLogPath = Join-Path $resolvedTarget "docs/plans/experiment-log.md"
$logContent = ""
if (Test-Path $experimentLogPath) {
  $logContent = Get-Content -Raw $experimentLogPath
}

$experimentRoot = Join-Path $resolvedTarget "experiments"
if (Test-Path $experimentRoot) {
  $experimentDirs = @(Get-ChildItem $experimentRoot -Directory | Where-Object { $_.Name -match "^\d{3}-" })

  foreach ($experimentDir in $experimentDirs) {
    $experimentId = [regex]::Match($experimentDir.Name, "^\d{3}").Value
    $shortId = [int]$experimentId
    $logPattern = "Experiment\s+(?:$experimentId|$shortId)\b"

    if ($logContent -notmatch $logPattern) {
      Add-Finding -Bucket ([ref]$findings) -Category "missing-log-entry" -Message "Experiment directory exists without a matching log entry." -Paths @($experimentDir.FullName.Replace($resolvedTarget + "\", ""))
    }

    $readmePath = Join-Path $experimentDir.FullName "README.md"
    $artifactsPath = Join-Path $experimentDir.FullName "artifacts"

    if ((Test-Path $readmePath) -and (Test-Path $artifactsPath)) {
      $readmeContent = Get-Content -Raw $readmePath
      $artifactFiles = @(Get-ChildItem $artifactsPath -File -Recurse)

      foreach ($artifactFile in $artifactFiles) {
        if ($readmeContent -notlike "*$($artifactFile.Name)*") {
          Add-Finding -Bucket ([ref]$findings) -Category "orphan-artifact" -Message "Artifact is not referenced by the experiment README." -Paths @($artifactFile.FullName.Replace($resolvedTarget + "\", ""))
        }
      }
    }
  }
}

$scriptRoot = Join-Path $resolvedTarget "scripts"
if (Test-Path $scriptRoot) {
  $scriptFiles = @(Get-ChildItem $scriptRoot -File -Recurse -Filter "*.ps1")
  $scriptHashes = foreach ($scriptFile in $scriptFiles) {
    [pscustomobject]@{
      path = $scriptFile.FullName
      hash = (Get-FileHash $scriptFile.FullName -Algorithm SHA256).Hash
    }
  }

  $duplicateGroups = @($scriptHashes | Group-Object hash | Where-Object { $_.Count -gt 1 })

  foreach ($duplicateGroup in $duplicateGroups) {
    Add-Finding -Bucket ([ref]$findings) -Category "duplicate-helper" -Message "Multiple helper scripts share identical content." -Paths @($duplicateGroup.Group.path | ForEach-Object { $_.Replace($resolvedTarget + "\", "") })
  }
}

$placeholderFiles = @(Get-ChildItem $resolvedTarget -File -Recurse | Where-Object {
  $_.Name -match "^(PLACEHOLDER|TODO|TEMP|DRAFT)([._-].*)?$" -or $_.Name -match "(?i)placeholder"
})

foreach ($placeholderFile in $placeholderFiles) {
  Add-Finding -Bucket ([ref]$findings) -Category "placeholder-file" -Message "Placeholder file should be deleted or converted into a tracked work item." -Paths @($placeholderFile.FullName.Replace($resolvedTarget + "\", ""))
}

$categoryCounts = $findings | Group-Object category | Sort-Object Name | ForEach-Object {
  [pscustomobject]@{
    category = $_.Name
    count = $_.Count
  }
}

[pscustomobject]@{
  generated_at = (Get-Date).ToString("o")
  target_root = $resolvedTarget
  total_findings = @($findings).Count
  category_counts = @($categoryCounts)
  findings = @($findings)
} | ConvertTo-Json -Depth 6
