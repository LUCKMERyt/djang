$ErrorActionPreference = "Continue"
$plan = Get-Content -Raw -Encoding UTF8 "D:\djang\download_plan.json" | ConvertFrom-Json
$mediaDir = "D:\djang\Al_Ven\media\products"
$logPath = "D:\djang\download_log.txt"
$used = New-Object System.Collections.Generic.HashSet[string]
$cache = @{}
$ua = "Mozilla/5.0 (compatible; ProductSeedBot/1.0; educational demo)"
$ok = 0
$skip = 0
$fail = 0

# Mark already-used URLs from existing successful log
if (Test-Path $logPath) {
    Get-Content $logPath -Encoding UTF8 | ForEach-Object {
        if ($_ -match '\| (https?://\S+)$') { $used.Add($Matches[1]) | Out-Null }
    }
}

function Get-ThumbUrls($query) {
    if ($cache.ContainsKey($query)) { return $cache[$query] }
    $encoded = [uri]::EscapeDataString("$query filemime:image/jpeg")
    $api = "https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=$encoded&gsrnamespace=6&gsrlimit=15&prop=imageinfo&iiprop=url&iiurlwidth=800&format=json"
    $urls = @()
    try {
        $resp = Invoke-RestMethod -Uri $api -Headers @{ "User-Agent" = $ua } -TimeoutSec 20
        if ($resp.query.pages) {
            foreach ($p in $resp.query.pages.PSObject.Properties.Value) {
                if ($p.imageinfo -and $p.imageinfo[0].thumburl) { $urls += $p.imageinfo[0].thumburl }
            }
        }
    } catch {}
    $cache[$query] = $urls
    return $urls
}

foreach ($item in $plan) {
    $n = $item.n
    $dest = Join-Path $mediaDir ("photo_{0}.jpg" -f $n)

    if ((Test-Path $dest) -and ((Get-Item $dest).Length -gt 10000)) {
        $skip++
        continue
    }

    $queries = @($item.query, "jewelry", "accessories", "gift")
    $done = $false
    foreach ($q in $queries) {
        if ($done) { break }
        foreach ($u in (Get-ThumbUrls $q)) {
            if ($used.Contains($u)) { continue }
            & curl.exe -L -s -A $ua --max-time 30 -o $dest $u 2>$null
            if ((Test-Path $dest) -and ((Get-Item $dest).Length -gt 10000)) {
                $used.Add($u) | Out-Null
                Add-Content -Path $logPath -Encoding UTF8 -Value "OK   photo_$n.jpg <- $q | $u"
                $done = $true
                $ok++
                break
            } elseif (Test-Path $dest) {
                Remove-Item $dest -Force
            }
        }
    }
    if (-not $done) {
        Add-Content -Path $logPath -Encoding UTF8 -Value "FAIL photo_$n.jpg <- $($item.query) | $($item.name)"
        $fail++
    }
}

Write-Output "DONE ok=$ok skip=$skip fail=$fail"
