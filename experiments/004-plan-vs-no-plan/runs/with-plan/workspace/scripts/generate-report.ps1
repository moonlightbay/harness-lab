param(
  [string]$ConfigPath = (Join-Path $PSScriptRoot "..\\config\\report-items.json")
)

$config = Get-Content -Raw $ConfigPath | ConvertFrom-Json
$items = @($config.items)

[pscustomobject]@{
  name = $config.name
  items = $items
  item_count = $items.Count
  generated_at = (Get-Date).ToUniversalTime().ToString("o")
} | ConvertTo-Json -Depth 3
