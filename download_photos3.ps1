$ErrorActionPreference = "Continue"
$plan = Get-Content -Raw -Encoding UTF8 "D:\djang\download_plan.json" | ConvertFrom-Json
$mediaDir = "D:\djang\Al_Ven\media\products"
$logPath = "D:\djang\download_log.txt"
$used = New-Object System.Collections.Generic.HashSet[string]
$cache = @{}
$ua = "Mozilla/5.0 (compatible; ProductSeedBot/1.0; educational demo)"
$ok = 0
$fail = 0

# Start fresh: remove previously downloaded numbered photos
Get-ChildItem $mediaDir -Filter "photo_*.jpg" -ErrorAction SilentlyContinue | Remove-Item -Force
Remove-Item $logPath -Force -ErrorAction SilentlyContinue

function Get-Results($query) {
    if ($cache.ContainsKey($query)) { return $cache[$query] }
    $encoded = [uri]::EscapeDataString("$query filemime:image/jpeg")
    $api = "https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=$encoded&gsrnamespace=6&gsrlimit=20&prop=imageinfo&iiprop=url&iiurlwidth=800&format=json"
    $items = @()
    try {
        $resp = Invoke-RestMethod -Uri $api -Headers @{ "User-Agent" = $ua } -TimeoutSec 20
        if ($resp.query.pages) {
            foreach ($p in $resp.query.pages.PSObject.Properties.Value) {
                if ($p.imageinfo -and $p.imageinfo[0].thumburl) {
                    $items += [pscustomobject]@{ title = "$($p.title)"; url = "$($p.imageinfo[0].thumburl)" }
                }
            }
        }
    } catch {}
    $cache[$query] = $items
    return $items
}

function Get-Score($title, $keywords) {
    $t = $title.ToLower()
    $score = 0
    foreach ($k in $keywords) {
        if ($k.Length -gt 2 -and $t.Contains($k.ToLower())) { $score++ }
    }
    return $score
}

foreach ($item in $plan) {
    $n = $item.n
    $dest = Join-Path $mediaDir ("photo_{0}.jpg" -f $n)
    $keywords = @()
    foreach ($w in ($item.query -split '\s+')) { if ($w) { $keywords += $w } }

    $queries = @($item.query, $item.type, "jewelry", "accessories", "gift")
    $done = $false
    foreach ($q in $queries) {
        if ($done) { break }
        $results = @(Get-Results $q | Sort-Object { Get-Score $_.title $keywords } -Descending)
        foreach ($r in $results) {
            if ($used.Contains($r.url)) { continue }
            & curl.exe -L -s -A $ua --max-time 30 -o $dest $r.url 2>$null
            if ((Test-Path $dest) -and ((Get-Item $dest).Length -gt 10000)) {
                $used.Add($r.url) | Out-Null
                Add-Content -Path $logPath -Encoding UTF8 -Value "OK   photo_$n.jpg | q=$q | title=$($r.title) | $($r.url)"
                $done = $true
                $ok++
                break
            } elseif (Test-Path $dest) {
                Remove-Item $dest -Force
            }
        }
        Start-Sleep -Milliseconds 80
    }
    if (-not $done) {
        Add-Content -Path $logPath -Encoding UTF8 -Value "FAIL photo_$n.jpg | q=$($item.query) | $($item.name)"
        $fail++
    }
}

Write-Output "DONE ok=$ok fail=$fail"
