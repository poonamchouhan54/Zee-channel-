import os
import requests

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
        while i < len(lines):
            line = lines[i]
            if line.startswith("#EXTINF"):
                line_lower = line.lower()
                
                # Check karein ki group-title "zee5" hai ya nahi
                # M3U mein aamtaur par group-title='ZEE5' ya group-title="ZEE5" hota hai
                is_zee5_group = 'group-title="zee5"' in line_lower or "group-title='zee5'" in line_lower or 'group-title="zee 5"' in line_lower or 'group-title="zee-5"' in line_lower or 'group-title="zee5' in line_lower
                
                # Check karein ki title ya line mein "news" toh nahi hai (news channels ignore karne ke liye)
                is_news = "news" in line_lower
                
                # Agar group zee5 ka hai AUR wo news channel nahi hai, tabhi uthao
                if is_zee5_group and not is_news:
                    channel_block = [line]
                    i += 1
                    while i < len(lines) and not lines[i].startswith("#EXTINF") and lines[i].strip() != "#EXTM3U":
                        channel_block.append(lines[i])
                        i += 1
                    zee_playlist.extend(channel_block)
                    continue
            i += 1
            
        os.makedirs("output", exist_ok=True)
        output_file = "output/zee_channels.m3u"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(zee_playlist))
            
        print(f"Successfully saved targeted Zee5 channels to {output_file}")
        
    except Exception as e:
        print(f"Error fetching or parsing playlist: {e}")
        exit(1)

if __name__ == "__main__":
    fetch_and_filter_zee()
