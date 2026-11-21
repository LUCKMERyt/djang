$ErrorActionPreference = "Continue"
$plan = Get-Content -Raw -Encoding UTF8 "D:\djang\download_plan.json" | ConvertFrom-Json
$mediaDir = "D:\djang\Al_Ven\media\products"
$log = New-Object System.Collections.Generic.List[string]
$used = New-Object System.Collections.Generic.HashSet[string]
$ua = @{ "User-Agent" = "Mozilla/5.0 (compatible; ProductSeedBot/1.0; educational demo)" }
$ok = 0
$fail = 0

function Get-ThumbUrls($query) {
    $encoded = [uri]::EscapeDataString("$query filemime:image/jpeg")
    $api = "https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=$encoded&gsrnamespace=6&gsrlimit=10&prop=imageinfo&iiprop=url&iiurlwidth=800&format=json"
    try {
        $resp = Invoke-RestMethod -Uri $api -Headers $ua -TimeoutSec 25
        if ($null -eq $resp.query.pages) { return @() }
        $urls = @()
        foreach ($p in $resp.query.pages.PSObject.Properties.Value) {
            if ($p.imageinfo -and $p.imageinfo[0].thumburl) { $urls += $p.imageinfo[0].thumburl }
        }
        return $urls
    } catch {
        return @()
    }
}

foreach ($item in $plan) {
    $n = $item.n
    $dest = Join-Path $mediaDir ("photo_{0}.jpg" -f $n)
    if (Test-Path $dest) { Remove-Item $dest -Force }

    $queries = @($item.query, "jewelry", "accessories", "gift")
    $done = $false
    foreach ($q in $queries) {
        if ($done) { break }
        $urls = Get-ThumbUrls $q
        foreach ($u in $urls) {
            if ($used.Contains($u)) { continue }
            try {
                Invoke-WebRequest -Uri $u -OutFile $dest -Headers $ua -TimeoutSec 40
                if ((Get-Item $dest).Length -gt 10000) {
                    $used.Add($u) | Out-Null
                    $log.Add("OK   photo_$n.jpg <- $q | $u")
                    $done = $true
                    $ok++
                    break
                } else {
                    Remove-Item $dest -Force
                }
            } catch {
                if (Test-Path $dest) { Remove-Item $dest -Force }
            }
        }
        Start-Sleep -Milliseconds 120
    }
    if (-not $done) {
        $log.Add("FAIL photo_$n.jpg <- $($item.query) | $($item.name)")
        $fail++
    }
}

$log | Set-Content -Encoding UTF8 "D:\djang\download_log.txt"
Write-Output "DOWNLOADED OK: $ok"
Write-Output "FAILED: $fail"
