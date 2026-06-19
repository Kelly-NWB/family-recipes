# After every push28: live URL must contain the edit. Agent runs this — not Kelly.
param(
  [string]$MustContain = ""
)

$url = "https://kelly-nwb.github.io/family-recipes/"
$data = "https://kelly-nwb.github.io/family-recipes/data/recipes.js"

function Get-Body($u) {
  try {
    return (Invoke-WebRequest -Uri $u -UseBasicParsing -TimeoutSec 25).Content
  } catch {
    return $null
  }
}

$home = Get-Body $url
$js = Get-Body $data

if (-not $home) { Write-Error "FAIL: site not reachable: $url"; exit 1 }
if (-not $js) { Write-Error "FAIL: recipes.js not reachable: $data"; exit 1 }

Write-Host "OK  $url"
Write-Host "OK  $data"

if ($MustContain) {
  $jsHas = $js -match [regex]::Escape($MustContain)
  Write-Host "recipes.js contains '$MustContain': $jsHas"
  if (-not $jsHas) {
    Write-Error "FAIL: live site missing expected text — wait 60s and re-run, or check push"
    exit 1
  }
}

Write-Host "PASS"
exit 0