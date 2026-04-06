param(
  [string]$ConfigPath = (Join-Path $PSScriptRoot "..\\config\\report-items.json")
)

$config = Get-Content -Raw $ConfigPath | ConvertFrom-Json

[pscustomobject]@{
  name = $config.name
  items = @($config.items)
} | ConvertTo-Json -Depth 3
