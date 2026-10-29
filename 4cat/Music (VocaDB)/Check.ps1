Get-ChildItem -Directory | ForEach-Object {
    $hasFiles = [bool](Get-ChildItem -Path $_.FullName -File -Force)
    if ($hasFiles) {
        Write-Host "[$($_.Name)] --> HAS FILES" -ForegroundColor Green
    } else {
        Write-Host "[$($_.Name)] --> EMPTY" -ForegroundColor Red
    }
}

pause
