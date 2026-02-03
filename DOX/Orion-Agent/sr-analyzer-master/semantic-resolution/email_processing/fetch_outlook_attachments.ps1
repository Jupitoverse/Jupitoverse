# ============================================================
# PowerShell Script to Fetch Today's Excel Attachments from Outlook
# Searches for emails FROM: GSSUTSMail@amdocs.com
# ============================================================

param(
    [string]$DownloadFolder = ".\downloads",
    [string]$SenderEmail = "GSSUTSMail@amdocs.com",
    [int]$DaysBack = 0  # 0 = today only, 1 = today and yesterday, etc.
)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Outlook Email Attachment Fetcher" -ForegroundColor Cyan
Write-Host "  Sender: $SenderEmail" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Create download folder if it doesn't exist
if (-not (Test-Path $DownloadFolder)) {
    New-Item -ItemType Directory -Path $DownloadFolder -Force | Out-Null
}

# Calculate date range
$today = Get-Date -Format "yyyy-MM-dd"
$startDate = (Get-Date).AddDays(-$DaysBack).Date
$endDate = (Get-Date).Date.AddDays(1)

Write-Host "[INFO] Looking for emails from: $($startDate.ToString('yyyy-MM-dd')) to today" -ForegroundColor Yellow
Write-Host "[INFO] Sender filter: $SenderEmail" -ForegroundColor Yellow
Write-Host ""

try {
    # Create Outlook COM object
    Write-Host "[1/3] Connecting to Outlook..." -ForegroundColor White
    $outlook = New-Object -ComObject Outlook.Application
    $namespace = $outlook.GetNamespace("MAPI")
    
    # Get Inbox folder
    $inbox = $namespace.GetDefaultFolder(6)  # 6 = Inbox
    Write-Host "      [OK] Connected to Inbox" -ForegroundColor Green
    Write-Host ""
    
    # Get emails from the Inbox
    Write-Host "[2/3] Scanning for emails from $SenderEmail..." -ForegroundColor White
    
    $items = $inbox.Items
    
    # Filter by sender and date using Restrict method for better performance
    $filterDate = $startDate.ToString("MM/dd/yyyy")
    $filter = "[ReceivedTime] >= '$filterDate' AND [SenderEmailAddress] = '$SenderEmail'"
    
    Write-Host "      Filter: $filter" -ForegroundColor Gray
    
    # Try filtered search first
    $filteredItems = $null
    try {
        $filteredItems = $items.Restrict($filter)
    } catch {
        Write-Host "      [WARN] Restrict filter failed, using manual scan..." -ForegroundColor Yellow
        $filteredItems = $null
    }
    
    $downloadedFiles = @()
    $emailCount = 0
    $attachmentCount = 0
    
    # If filter worked, use filtered items; otherwise scan all
    if ($filteredItems -and $filteredItems.Count -gt 0) {
        Write-Host "      Found $($filteredItems.Count) matching email(s)" -ForegroundColor Green
        
        foreach ($item in $filteredItems) {
            try {
                $emailCount++
                
                # Check for attachments
                if ($item.Attachments.Count -gt 0) {
                    foreach ($attachment in $item.Attachments) {
                        $fileName = $attachment.FileName
                        
                        # Check if it's an Excel file
                        if ($fileName -match '\.(xls|xlsx)$') {
                            $attachmentCount++
                            
                            # Generate unique filename with timestamp
                            $timestamp = $item.ReceivedTime.ToString("yyyyMMdd_HHmmss")
                            $newFileName = "${timestamp}_${fileName}"
                            $savePath = Join-Path $DownloadFolder $newFileName
                            
                            # Check if already downloaded
                            if (-not (Test-Path $savePath)) {
                                Write-Host "      Downloading: $fileName" -ForegroundColor Cyan
                                Write-Host "        Subject: $($item.Subject)" -ForegroundColor Gray
                                Write-Host "        Received: $($item.ReceivedTime)" -ForegroundColor Gray
                                
                                $attachment.SaveAsFile($savePath)
                                $downloadedFiles += $newFileName
                            } else {
                                Write-Host "      [Skip] Already exists: $newFileName" -ForegroundColor Yellow
                            }
                        }
                    }
                }
            } catch {
                # Skip problematic items
                continue
            }
        }
    } else {
        # Manual scan through all items
        Write-Host "      Scanning inbox manually..." -ForegroundColor Gray
        $items.Sort("[ReceivedTime]", $true)  # Sort by newest first
        
        foreach ($item in $items) {
            try {
                # Check if it's within date range
                if ($item.ReceivedTime -ge $startDate -and $item.ReceivedTime -lt $endDate) {
                    # Check sender
                    $senderAddr = ""
                    try {
                        $senderAddr = $item.SenderEmailAddress
                        if (-not $senderAddr) {
                            $senderAddr = $item.Sender.Address
                        }
                    } catch {
                        continue
                    }
                    
                    # Match sender (case-insensitive)
                    if ($senderAddr -like "*$($SenderEmail.Split('@')[0])*" -or 
                        $senderAddr -like "*GSSUTSMail*" -or
                        $item.SenderName -like "*GSS UTS*") {
                        
                        $emailCount++
                        
                        # Check for attachments
                        if ($item.Attachments.Count -gt 0) {
                            foreach ($attachment in $item.Attachments) {
                                $fileName = $attachment.FileName
                                
                                # Check if it's an Excel file
                                if ($fileName -match '\.(xls|xlsx)$') {
                                    $attachmentCount++
                                    
                                    # Generate unique filename with timestamp
                                    $timestamp = $item.ReceivedTime.ToString("yyyyMMdd_HHmmss")
                                    $newFileName = "${timestamp}_${fileName}"
                                    $savePath = Join-Path $DownloadFolder $newFileName
                                    
                                    # Check if already downloaded
                                    if (-not (Test-Path $savePath)) {
                                        Write-Host "      Downloading: $fileName" -ForegroundColor Cyan
                                        Write-Host "        Subject: $($item.Subject)" -ForegroundColor Gray
                                        Write-Host "        From: $($item.SenderName)" -ForegroundColor Gray
                                        Write-Host "        Received: $($item.ReceivedTime)" -ForegroundColor Gray
                                        
                                        $attachment.SaveAsFile($savePath)
                                        $downloadedFiles += $newFileName
                                    } else {
                                        Write-Host "      [Skip] Already exists: $newFileName" -ForegroundColor Yellow
                                    }
                                }
                            }
                        }
                    }
                } elseif ($item.ReceivedTime -lt $startDate) {
                    # Emails are sorted newest first, so we can stop when we hit older emails
                    break
                }
            } catch {
                # Skip problematic items
                continue
            }
        }
    }
    
    Write-Host ""
    Write-Host "[3/3] Summary" -ForegroundColor White
    Write-Host "      Emails from GSS UTS Mail: $emailCount" -ForegroundColor Gray
    Write-Host "      Excel attachments found: $attachmentCount" -ForegroundColor Gray
    Write-Host "      New files downloaded: $($downloadedFiles.Count)" -ForegroundColor Green
    
    if ($downloadedFiles.Count -gt 0) {
        Write-Host ""
        Write-Host "      Downloaded files:" -ForegroundColor Cyan
        foreach ($file in $downloadedFiles) {
            Write-Host "        - $file" -ForegroundColor White
        }
    } elseif ($emailCount -eq 0) {
        Write-Host ""
        Write-Host "      [INFO] No emails from GSS UTS Mail found for today." -ForegroundColor Yellow
        Write-Host "             Try increasing DaysBack parameter to check older emails." -ForegroundColor Gray
    }
    
    Write-Host ""
    Write-Host "[OK] Outlook fetch complete!" -ForegroundColor Green
    
    # Release COM objects
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($outlook) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
    
    exit 0
    
} catch {
    Write-Host "[ERROR] $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "  1. Make sure Outlook is running" -ForegroundColor Gray
    Write-Host "  2. Check if you have emails from GSSUTSMail@amdocs.com" -ForegroundColor Gray
    Write-Host "  3. Try running this script as Administrator" -ForegroundColor Gray
    exit 1
}
