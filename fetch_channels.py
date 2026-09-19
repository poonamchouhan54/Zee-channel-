import os
import requests
import re

WORKER_URL = "https://server.vodep39240327.workers.dev/channel/raw?=m3um3u"

def fetch_and_filter_zee():
    try:
        print("Fetching playlist from worker...")
        response = requests.get(WORKER_URL)
        response.raise_for_status()
        content = response.text
        
        lines = content.splitlines()
        zee_playlist = ["#EXTM3U"]
        
        i = 0
        extracted_count = 0
        
        while i < len(lines):
            line = lines[i]
            if line.startswith("#EXTINF"):
                line_lower = line.lower()
                
                # 1. Group-title ko dhoondhne ke liye regex (group-title="..." ya group-title='...')
                group_match = re.search(r'group-title=["\']([^"\']+)["\']', line, re.IGNORECASE)
                group_title = group_match.group(1).lower() if group_match else ""
                
                # 2. Strict Check: Group ka naam strictly "zee5" ya "zee" hona chahiye 
                # (aur isme movies, webseries, ya dusre IPTV categories nahi aane chahiye)
                is_target_group = "zee5" in group_title or group_title == "zee"
                
                # 3. News channels ko ignore karne ki condition
                is_news = "news" in line_lower or "news" in group_title
                
                # Agar group strict Zee5 hai AUR wo news nahi hai, tabhi allow karo
                if is_target_group and not is_news:
                    channel_block = [line]
                    i += 1
                    # Us channel ki baaki lines (jaise headers, user-agent, stream URL) capture karo
                    while i < len(lines) and not lines[i].startswith("#EXTINF") and lines[i].strip() != "#EXTM3U":
                        channel_block.append(lines[i])
                        i += 1
                    zee_playlist.extend(channel_block)
                    extracted_count += 1
                    continue
            i += 1
            
        os.makedirs("output", exist_ok=True)
        output_file = "output/zee_channels.m3u"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(zee_playlist))
            
        print(f"Successfully saved {extracted_count} clean Zee5 channels to {output_file}")
        
    except Exception as e:
        print(f"Error fetching or parsing playlist: {e}")
        exit(1)

if __name__ == "__main__":
    fetch_and_filter_zee()
