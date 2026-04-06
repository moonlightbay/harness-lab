$scriptPath = Join-Path $PSScriptRoot "..\\scripts\\generate-report.ps1"
$report = & $scriptPath | ConvertFrom-Json

if (-not ($report.PSObject.Properties.Name -contains "name")) {
  throw "Missing name field."
}

if (-not ($report.PSObject.Properties.Name -contains "items")) {
  throw "Missing items field."
}

if (-not ($report.PSObject.Properties.Name -contains "item_count")) {
  throw "Missing item_count field."
}

if (-not ($report.PSObject.Properties.Name -contains "generated_at")) {
  throw "Missing generated_at field."
}

if ([int]$report.item_count -ne @($report.items).Count) {
  throw "item_count does not match items length."
}
