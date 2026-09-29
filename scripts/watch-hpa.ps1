# Timestamped HPA capture. Run in its OWN terminal before the load test. Ctrl+C to stop.
# Writes one line every few seconds: "<time> <kubectl get hpa row>"
param(
    [string]$Out = "docs/evidence/hpa-watch.txt",
    [int]$IntervalSeconds = 5
)

New-Item -ItemType Directory -Force -Path (Split-Path $Out) | Out-Null
Write-Host "Capturing HPA every $IntervalSeconds s to $Out  (Ctrl+C to stop)"

while ($true) {
    $stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $row = kubectl get hpa backend-hpa -n civicpulse --no-headers 2>&1
    $line = "$stamp $row"
    Write-Host $line
    Add-Content -Path $Out -Value $line -Encoding ascii
    Start-Sleep -Seconds $IntervalSeconds
}
