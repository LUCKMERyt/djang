$ErrorActionPreference = "Continue"
$plan = Get-Content -Raw -Encoding UTF8 "D:\djang\download_plan.json" | ConvertFrom-Json
$mediaDir = "D:\djang\Al_Ven\media\products"
$logPath = "D:\djang\download_log.txt"
$ua = "Mozilla/5.0 (compatible; ProductSeedBot/1.0; educational demo)"
$cache = @{}
$used = New-Object System.Collections.Generic.HashSet[string]
$ok = 0
$fail = 0

# Track already-used URLs from log
if (Test-Path $logPath) {
    Get-Content $logPath -Encoding UTF8 | ForEach-Object {
        if ($_ -match '\| (https?://\S+)$') { $used.Add($Matches[1]) | Out-Null }
    }
}

$have = @()
Get-ChildItem $mediaDir -Filter "photo_*.jpg" -ErrorAction SilentlyContinue | ForEach-Object {
    $have += [int]($_.BaseName -replace 'photo_','')
}

$missing = @()
foreach ($p in $plan) { if ($have -notcontains $p.n) { $missing += $p } }
# Priority: first 50 photos (n <= 65) first
$ordered = @($missing | Where-Object { $_.n -le 65 } | Sort-Object n) + @($missing | Where-Object { $_.n -gt 65 } | Sort-Object n)

function Get-Results($query) {
    if ($cache.ContainsKey($query)) { return $cache[$query] }
    $encoded = [uri]::EscapeDataString("$query filemime:image/jpeg")
    $api = "https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=$encoded&gsrnamespace=6&gsrlimit=20&prop=imageinfo&iiprop=url&iiurlwidth=800&format=json&maxlag=5"
    $items = @()
    for ($attempt = 1; $attempt -le 3; $attempt++) {
        try {
            $resp = Invoke-RestMethod -Uri $api -Headers @{ "User-Agent" = $ua } -TimeoutSec 25
            if ($resp.query.pages) {
                foreach ($p in $resp.query.pages.PSObject.Properties.Value) {
                    if ($p.imageinfo -and $p.imageinfo[0].thumburl) {
                        $items += [pscustomobject]@{ title = "$($p.title)"; url = "$($p.imageinfo[0].thumburl)" }
                    }
                }
            }
            break
        } catch {
            Start-Sleep -Seconds 4
        }
    }
    $cache[$query] = $items
    return $items
}

foreach ($item in $ordered) {
    $n = $item.n
    $dest = Join-Path $mediaDir ("photo_{0}.jpg" -f $n)
    $queries = @($item.query, $item.type)
    if ($item.category -eq 'Украшения') { $queries += 'jewelry' }
    elseif ($item.category -eq 'Аксессуары') { $queries += 'fashion accessories' }
    else { $queries += 'gift' }

    $done = $false
    foreach ($q in $queries) {
        if ($done) { break }
        $results = Get-Results $q
        foreach ($r in $results) {
            if ($used.Contains($r.url)) { continue }
            & curl.exe -L -s -A $ua --max-time 40 -o $dest $r.url 2>$null
            if ((Test-Path $dest) -and ((Get-Item $dest).Length -gt 10000)) {
                $used.Add($r.url) | Out-Null
                Add-Content -Path $logPath -Encoding UTF8 -Value "OK   photo_$n.jpg | q=$q | title=$($r.title) | $($r.url)"
                $done = $true
                $ok++
                break
            } elseif (Test-Path $dest) {
                Remove-Item $dest -Force
            }
            Start-Sleep -Milliseconds 300
        }
        Start-Sleep -Milliseconds 900
    }
    if (-not $done) {
        Add-Content -Path $logPath -Encoding UTF8 -Value "FAIL photo_$n.jpg | q=$($item.query) | $($item.name)"
        $fail++
    }
}

Write-Output "DONE ok=$ok fail=$fail"
