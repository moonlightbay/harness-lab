$scriptPath = Join-Path $PSScriptRoot "..\\scripts\\export-report.ps1"
$report = & $scriptPath | ConvertFrom-Json

if (-not ($report.PSObject.Properties.Name -contains "name")) {
  throw "Missing name field."
}

if (-not ($report.PSObject.Properties.Name -contains "items")) {
  throw "Missing items field."
}

if (@($report.items).Count -lt 1) {
  throw "Expected at least one item."
}
