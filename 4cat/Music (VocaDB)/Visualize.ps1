$html = "<html><head><style>"
$html += "body { font-family: sans-serif; background: #1e1e1e; color: #fff; padding: 20px; margin: 0; }"
$html += ".grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 20px; }"
$html += ".card { background: #252526; border: 1px solid #3e3e42; border-radius: 8px; padding: 10px; display: flex; flex-direction: column; justify-content: space-between; min-height: 150px; }"
$html += ".img-box { display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px; margin-bottom: 10px; flex-grow: 1; }"
$html += ".thumb { width: 100%; height: 100px; border: 1px solid #555; border-radius: 4px; object-fit: cover; }"
$html += ".empty-box { grid-column: span 2; display: flex; align-items: center; justify-content: center; height: 100px; background: #1a1a1a; border: 1px dashed #555; border-radius: 4px; color: #666; font-size: 12px; }"
$html += ".folder-title { font-size: 13px; font-weight: bold; color: #00adb5; text-align: center; word-break: break-all; margin-top: 5px; }"
$html += "</style></head><body>"
$html += "<h2>Folder Grid Index (All Folders)</h2><div class='grid'>"

Get-ChildItem -Directory | ForEach-Object {
    $folderName = $_.Name
    $images = Get-ChildItem -Path $_.FullName -File -Force | Where-Object { $_.Extension -match '\.(jpg|jpeg|png|gif|webp|bmp)' }
    $totalImg = if ($images) { $images.Count } else { 0 }
    
    $html += "<div class='card' title='$folderName ($totalImg items)'>"
    $html += "<div class='img-box'>"
    
    if ($totalImg -gt 0) {
        # Показываем до 4 крупных картинок (плиткой 2х2)
        $displayCount = if ($totalImg -gt 4) { 4 } else { $totalImg }
        for ($i = 0; $i -lt $displayCount; $i++) {
            $encodedPath = [Uri]::EscapeDataString($folderName) + "/" + [Uri]::EscapeDataString($images[$i].Name)
            $html += "<img src='$encodedPath' class='thumb'>"
        }
    } else {
        # Красивая заглушка, если папка пустая или без картинок
        $html += "<div class='empty-box'>No Images</div>"
    }
    
    $html += "</div>"
    # Название папки крупно снизу (выводится ВСЕГДА)
    $html += "<div class='folder-title'>$folderName ($totalImg)</div>"
    $html += "</div>"
}

$html += "</div></body></html>"
$html | Out-File -FilePath "Visualize.html" -Encoding utf8
Start-Process "Visualize.html"
