# Runs the load test and writes LOAD_START / LOAD_END markers into the HPA capture file,
# so the chart script can measure the real scale-up lag.
# Uses a local hey.exe if found, otherwise the Docker image built from tools/hey.
param(
    [string]$Duration = "3m",
    [int]$Concurrency = 40,
    [string]$Url = "http://localhost:8080/api/v1/complaints",
    [string]$Marker = "docs/evidence/hpa-watch.txt",
    [string]$HeyOut = "docs/evidence/hey-output.txt"
)

New-Item -ItemType Directory -Force -Path (Split-Path $Marker) | Out-Null

Add-Content -Path $Marker -Value ((Get-Date -Format "yyyy-MM-dd HH:mm:ss") + " LOAD_START") -Encoding ascii
Write-Host "LOAD_START recorded. Running for $Duration with $Concurrency workers..."

if (Get-Command hey -ErrorAction SilentlyContinue) {
    hey -z $Duration -c $Concurrency $Url 2>&1 | ForEach-Object { $_; Add-Content -Path $HeyOut -Value $_ -Encoding ascii }
} else {
    $dockerUrl = $Url -replace "localhost", "host.docker.internal"
    docker run --rm civicpulse-hey -z $Duration -c $Concurrency $dockerUrl 2>&1 | ForEach-Object { $_; Add-Content -Path $HeyOut -Value $_ -Encoding ascii }
}

Add-Content -Path $Marker -Value ((Get-Date -Format "yyyy-MM-dd HH:mm:ss") + " LOAD_END") -Encoding ascii
Write-Host "LOAD_END recorded. Keep the watch running ~6 more minutes to capture scale-down."
