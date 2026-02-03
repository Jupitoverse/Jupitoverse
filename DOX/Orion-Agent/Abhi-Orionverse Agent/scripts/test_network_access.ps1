# Orionverse Network Access Test Script
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   Orionverse Network Connectivity Test" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# 1. Get IP Address
Write-Host "[1/6] Getting your machine's IP address..." -ForegroundColor Yellow
$ipAddresses = Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notlike "*Loopback*" -and $_.IPAddress -notlike "169.254.*"}
if ($ipAddresses) {
    foreach ($ip in $ipAddresses) {
        Write-Host "      ✓ $($ip.InterfaceAlias): $($ip.IPAddress)" -ForegroundColor Green
    }
    $mainIP = ($ipAddresses | Select-Object -First 1).IPAddress
} else {
    Write-Host "      ✗ No network IP found" -ForegroundColor Red
    $mainIP = "Unknown"
}
Write-Host ""

# 2. Check if Python is installed
Write-Host "[2/6] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "      ✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "      ✗ Python not found" -ForegroundColor Red
}
Write-Host ""

# 3. Check if backend is running
Write-Host "[3/6] Checking if backend is running..." -ForegroundColor Yellow
$pythonProcess = Get-Process | Where-Object {$_.ProcessName -like "*python*"}
if ($pythonProcess) {
    Write-Host "      ✓ Python process found (PID: $($pythonProcess[0].Id))" -ForegroundColor Green
} else {
    Write-Host "      ✗ No Python process running" -ForegroundColor Red
    Write-Host "      → Run START_NETWORK_BACKEND.bat to start" -ForegroundColor Yellow
}
Write-Host ""

# 4. Test port 5001
Write-Host "[4/6] Testing port 5001..." -ForegroundColor Yellow
try {
    $portTest = Test-NetConnection -ComputerName localhost -Port 5001 -WarningAction SilentlyContinue
    if ($portTest.TcpTestSucceeded) {
        Write-Host "      ✓ Port 5001 is open and listening" -ForegroundColor Green
    } else {
        Write-Host "      ✗ Port 5001 is not accessible" -ForegroundColor Red
    }
} catch {
    Write-Host "      ✗ Could not test port 5001" -ForegroundColor Red
}
Write-Host ""

# 5. Check firewall rules
Write-Host "[5/6] Checking Windows Firewall..." -ForegroundColor Yellow
try {
    $firewallRule = Get-NetFirewallRule -DisplayName "*Flask*" -ErrorAction SilentlyContinue
    if ($firewallRule) {
        Write-Host "      ✓ Firewall rule exists: $($firewallRule.DisplayName)" -ForegroundColor Green
        Write-Host "      ✓ Enabled: $($firewallRule.Enabled)" -ForegroundColor Green
    } else {
        Write-Host "      ⚠ No firewall rule found" -ForegroundColor Yellow
        Write-Host "      → Run as Administrator to create rule:" -ForegroundColor Yellow
        Write-Host "      New-NetFirewallRule -DisplayName 'Flask Backend 5001' -Direction Inbound -LocalPort 5001 -Protocol TCP -Action Allow" -ForegroundColor Cyan
    }
} catch {
    Write-Host "      ⚠ Could not check firewall rules" -ForegroundColor Yellow
}
Write-Host ""

# 6. Test API endpoint
Write-Host "[6/6] Testing API endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5001/api/search/all" -Method GET -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "      ✓ API is responding correctly!" -ForegroundColor Green
        $data = $response.Content | ConvertFrom-Json
        Write-Host "      ✓ SR Data: $($data.total_counts.sr_total) records" -ForegroundColor Green
        Write-Host "      ✓ Defect Data: $($data.total_counts.defect_total) records" -ForegroundColor Green
    }
} catch {
    Write-Host "      ✗ API not responding: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "      → Make sure backend is running" -ForegroundColor Yellow
}
Write-Host ""

# Summary
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   SUMMARY" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your machine IP: $mainIP" -ForegroundColor White
Write-Host ""
Write-Host "Access URLs:" -ForegroundColor White
Write-Host "  Local:   http://127.0.0.1:5001/api/search/all" -ForegroundColor Cyan
Write-Host "  Network: http://$mainIP:5001/api/search/all" -ForegroundColor Cyan
Write-Host ""
Write-Host "Frontend (index.html):" -ForegroundColor White
Write-Host "  Will automatically connect to: http://$mainIP:5001" -ForegroundColor Cyan
Write-Host ""
Write-Host "Share with team:" -ForegroundColor White
Write-Host "  1. Start backend: START_NETWORK_BACKEND.bat" -ForegroundColor Yellow
Write-Host "  2. Share this URL: http://$mainIP/path/to/index.html" -ForegroundColor Yellow
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan

Write-Host ""
Read-Host "Press Enter to exit"





