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

$sharedScript = Join-Path $PSScriptRoot "..\\shared\\measure-navigation-pack.ps1"

& $sharedScript -RootPath $RepoRoot -RelativePaths $TopLevelFiles -RequiredPaths $RequiredPaths
