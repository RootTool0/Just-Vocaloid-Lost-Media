(function() {
    const playInfo = window.__playinfo__;
    if (!playInfo || !playInfo.data || !playInfo.data.dash) {
        console.log("%c❌ DASH data not found. Please refresh the page.", "color: #ff0000; font-weight: bold;");
        return;
    }

    const audioStreams = playInfo.data.dash.audio || [];
    const videoStreams = playInfo.data.dash.video || [];

    if (videoStreams.length === 0 || audioStreams.length === 0) {
        console.log("❌ Failed to separate media streams.");
        return;
    }

    const videoUrl = videoStreams[0].baseUrl || videoStreams[0].base_url;
    const audioUrl = audioStreams[0].baseUrl || audioStreams[0].base_url;

    // Extract original cover URL
    let coverUrl = '';
    if (window.__INITIAL_STATE__ && window.__INITIAL_STATE__.videoData && window.__INITIAL_STATE__.videoData.pic) {
        coverUrl = window.__INITIAL_STATE__.videoData.pic;
    } else {
        const metaImg = document.querySelector('meta[property="og:image"]');
        if (metaImg) coverUrl = metaImg.getAttribute('content');
    }

    let ext = 'jpg';
    if (coverUrl) {
        if (coverUrl.startsWith('//')) coverUrl = 'https:' + coverUrl;
        if (coverUrl.includes('@')) {
            coverUrl = coverUrl.split('@')[0];
        }
        const match = coverUrl.match(/\.(webp|png|jpg|jpeg|gif)/i);
        if (match) {
            ext = match[0].replace('.', '').toLowerCase();
        }
    }

    // Trim exactly 14 characters from the end of the page title "_哔哩哔哩_bilibili"
    let baseTitle = document.title.trim().slice(0, -14).trim();
    let cleanTitle = baseTitle.replace(/[\\/:*?"<>|]/g, "_");

    // Print links log
    console.clear();
    console.log("%c📋 DIRECT LINKS TO ALL VIDEO RESOURCES:", "color: #ffaa00; font-weight: bold; font-size: 14px;");
    console.log("%c🎬 Video Stream Link:", "color: #00a2ff; font-weight: bold;");
    console.log(videoUrl);
    console.log("%c🎵 Audio Stream Link:", "color: #00ff00; font-weight: bold;");
    console.log(audioUrl);
    console.log("%c📸 HD Cover Link:", "color: #ff00ff; font-weight: bold;");
    console.log(coverUrl);
    console.log("\n" + "═".repeat(60) + "\n");

    // BiliBili player headers variable to bypass CDN restrictions
    const psHeaders = '$h = @{"Referer"="https://bilibili.com"; "User-Agent"="Mozilla/5.0"};';

    let downloadCoverCmd = '';
    if (coverUrl) {
        downloadCoverCmd = `Invoke-WebRequest -Headers $h -Uri "${coverUrl}" -OutFile "${cleanTitle}.${ext}"; `;
    }

    // Complete PowerShell command
    const psCommand = `${psHeaders} Invoke-WebRequest -Headers $h -Uri "${videoUrl}" -OutFile "v_temp.mp4"; Invoke-WebRequest -Headers $h -Uri "${audioUrl}" -OutFile "a_temp.m4a"; ${downloadCoverCmd}ffmpeg -i "v_temp.mp4" -i "a_temp.m4a" -c copy "${cleanTitle}.mp4"; Remove-Item "v_temp.mp4", "a_temp.m4a"`;

    console.log("%c🚀 READY POWERSHELL COMMAND:", "color: #00ff00; font-weight: bold; font-size: 14px;");
    console.log(psCommand);
})();
