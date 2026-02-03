# Orionverse AVD Machine - Quick Setup Script
# Run this after extracting ZIP on AVD machine

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   Orionverse AVD Setup Automation" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$ErrorActionPreference = "Continue"

# 1. Check Python
Write-Host "[1/7] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "      ✓ $pythonVersion found" -ForegroundColor Green
} catch {
    Write-Host "      ✗ Python not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python 3.11+ from:" -ForegroundColor Yellow
    Write-Host "https://www.python.org/downloads/" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "⚠️ Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# 2. Check pip
Write-Host "[2/7] Checking pip..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>&1
    Write-Host "      ✓ pip found" -ForegroundColor Green
    
    Write-Host "      Upgrading pip..." -ForegroundColor Yellow
    python -m pip install --upgrade pip --quiet 2>&1 | Out-Null
    Write-Host "      ✓ pip upgraded to latest version" -ForegroundColor Green
} catch {
    Write-Host "      ✗ pip not found" -ForegroundColor Red
}
Write-Host ""

# 3. Install dependencies
Write-Host "[3/7] Installing Python dependencies..." -ForegroundColor Yellow
Write-Host "      This may take 2-3 minutes..." -ForegroundColor Gray

if (Test-Path "requirements.txt") {
    Write-Host ""
    Write-Host "      Installing packages:" -ForegroundColor Gray
    $packages = Get-Content "requirements.txt" | Where-Object {$_ -notmatch "^#" -and $_ -ne ""}
    
    try {
        pip install -r requirements.txt --quiet 2>&1 | Out-Null
        Write-Host ""
        Write-Host "      ✓ All dependencies installed successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "      Installed packages:" -ForegroundColor Gray
        Write-Host "        - Flask (Web framework)" -ForegroundColor White
        Write-Host "        - Flask-CORS (API access)" -ForegroundColor White
        Write-Host "        - psycopg2 (PostgreSQL driver)" -ForegroundColor White
        Write-Host "        - pandas (Data processing)" -ForegroundColor White
        Write-Host "        - SQLAlchemy (Database ORM)" -ForegroundColor White
        Write-Host "        - requests (HTTP client)" -ForegroundColor White
        Write-Host "        - python-dotenv (Environment variables)" -ForegroundColor White
    } catch {
        Write-Host "      ⚠️ Some packages may have failed to install" -ForegroundColor Yellow
        Write-Host "      Error: $_" -ForegroundColor Red
    }
} else {
    Write-Host "      ✗ requirements.txt not found!" -ForegroundColor Red
}
Write-Host ""

# 4. Verify installations
Write-Host "[4/7] Verifying installations..." -ForegroundColor Yellow
$allGood = $true

$requiredPackages = @("flask", "flask_cors", "psycopg2", "pandas", "sqlalchemy", "requests")
foreach ($package in $requiredPackages) {
    try {
        $test = python -c "import $package; print('OK')" 2>&1
        if ($test -like "*OK*") {
            Write-Host "      ✓ $package" -ForegroundColor Green
        } else {
            Write-Host "      ✗ $package not found" -ForegroundColor Red
            $allGood = $false
        }
    } catch {
        Write-Host "      ✗ $package not found" -ForegroundColor Red
        $allGood = $false
    }
}
Write-Host ""

# 5. Test database connection
Write-Host "[5/7] Testing database connection..." -ForegroundColor Yellow
Write-Host "      Connecting to: oso-pstgr-rd.orion.comcast.com:6432" -ForegroundColor Gray

if (Test-Path "backend\database.py") {
    try {
        cd backend
        $dbTest = python -c "import database; conn = database.get_db_connection(); print('CONNECTED' if conn else 'FAILED')" 2>&1
        cd ..
        
        if ($dbTest -like "*CONNECTED*") {
            Write-Host "      ✓ Database connection successful!" -ForegroundColor Green
        } else {
            Write-Host "      ✗ Database connection failed" -ForegroundColor Red
            Write-Host "      ⚠️ Make sure you're connected to Comcast network/VPN" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "      ✗ Could not test database connection" -ForegroundColor Red
        Write-Host "      Error: $_" -ForegroundColor Yellow
    }
} else {
    Write-Host "      ⚠️ backend\database.py not found - skipping test" -ForegroundColor Yellow
}
Write-Host ""

# 6. Configure Windows Firewall
Write-Host "[6/7] Configuring Windows Firewall..." -ForegroundColor Yellow

$rule = Get-NetFirewallRule -DisplayName "Flask Backend 5001" -ErrorAction SilentlyContinue
if ($rule) {
    Write-Host "      ✓ Firewall rule already exists" -ForegroundColor Green
} else {
    Write-Host "      Creating firewall rule for port 5001..." -ForegroundColor Gray
    try {
        New-NetFirewallRule -DisplayName "Flask Backend 5001" -Direction Inbound -LocalPort 5001 -Protocol TCP -Action Allow -ErrorAction Stop | Out-Null
        Write-Host "      ✓ Firewall rule created successfully" -ForegroundColor Green
    } catch {
        Write-Host "      ⚠️ Could not create firewall rule automatically" -ForegroundColor Yellow
        Write-Host "      Run this script as Administrator, or manually allow port 5001" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "      Manual command (run as Administrator):" -ForegroundColor Gray
        Write-Host "      New-NetFirewallRule -DisplayName 'Flask Backend 5001' -Direction Inbound -LocalPort 5001 -Protocol TCP -Action Allow" -ForegroundColor Cyan
    }
}
Write-Host ""

# 7. Get IP Address
Write-Host "[7/7] Getting network information..." -ForegroundColor Yellow

$ipAddresses = Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notlike "*Loopback*" -and $_.IPAddress -notlike "169.254.*"}
if ($ipAddresses) {
    Write-Host "      ✓ Network IP addresses:" -ForegroundColor Green
    foreach ($ip in $ipAddresses) {
        Write-Host "        - $($ip.InterfaceAlias): $($ip.IPAddress)" -ForegroundColor White
    }
    $mainIP = ($ipAddresses | Select-Object -First 1).IPAddress
} else {
    Write-Host "      ⚠️ No network IP found" -ForegroundColor Yellow
    $mainIP = "localhost"
}
Write-Host ""

# Summary
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   SETUP SUMMARY" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

if ($allGood) {
    Write-Host "✅ Setup completed successfully!" -ForegroundColor Green
} else {
    Write-Host "⚠️ Setup completed with some warnings" -ForegroundColor Yellow
    Write-Host "Review the output above for details" -ForegroundColor Yellow
}
Write-Host ""

# Instructions
Write-Host "📋 NEXT STEPS:" -ForegroundColor White
Write-Host ""
Write-Host "1. Start Backend:" -ForegroundColor Yellow
Write-Host "   .\START_NETWORK_BACKEND.bat" -ForegroundColor Cyan
Write-Host "   or" -ForegroundColor Gray
Write-Host "   cd backend ; python app.py" -ForegroundColor Cyan
Write-Host ""

Write-Host "2. Access URLs:" -ForegroundColor Yellow
Write-Host "   Local:   http://127.0.0.1:5001" -ForegroundColor Cyan
Write-Host "   Network: http://$mainIP:5001" -ForegroundColor Cyan
Write-Host ""

Write-Host "3. Test API:" -ForegroundColor Yellow
Write-Host "   curl http://localhost:5001/api/search/all" -ForegroundColor Cyan
Write-Host "   or open in browser" -ForegroundColor Gray
Write-Host ""

Write-Host "4. Open in VS Code:" -ForegroundColor Yellow
Write-Host "   code ." -ForegroundColor Cyan
Write-Host ""

Write-Host "5. Run diagnostics (if needed):" -ForegroundColor Yellow
Write-Host "   .\test_network_access.ps1" -ForegroundColor Cyan
Write-Host ""

Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if we should start backend now
$startNow = Read-Host "Would you like to start the backend now? (y/n)"
if ($startNow -eq "y" -or $startNow -eq "Y") {
    Write-Host ""
    Write-Host "Starting backend..." -ForegroundColor Yellow
    Write-Host ""
    
    if (Test-Path "START_NETWORK_BACKEND.bat") {
        Start-Process -FilePath "START_NETWORK_BACKEND.bat"
    } else {
        Write-Host "Starting backend manually..." -ForegroundColor Yellow
        cd backend
        python app.py
    }
} else {
    Write-Host ""
    Write-Host "Setup complete! Run .\START_NETWORK_BACKEND.bat when ready." -ForegroundColor Green
    Write-Host ""
}

Read-Host "Press Enter to exit"





