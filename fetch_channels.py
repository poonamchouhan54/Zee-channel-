import os
import requests

# Worker URL jahan se M3U data mil raha hai
WORKER_URL = "https://server.vodep39240327.workers.dev/channel/raw?=m3um3u"

def fetch_and_filter_zee():
    try:
        print("Fetching playlist from worker...")
        response = requests.get(WORKER_URL)
        response.raise_for_status()
        content = response.text
        
        # M3U format ko parse karna aur Zee channels ko filter karna
        lines = content.splitlines()
        zee_playlist = ["#EXTM3U"]
        
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith("#EXTINF"):
                # Check karein ki channel Zee se related hai ya nahi (aap apne mutabiq keyword adjust kar sakte hain)
                if "zee" in line.lower():
                    # EXTINF line aur uske baad wali URL/metadata lines ko capture karein
                    channel_block = [line]
                    i += 1
                    while i < len(lines) and not lines[i].startswith("#EXTINF") and lines[i].strip() != "#EXTM3U":
                        channel_block.append(lines[i])
                        i += 1
                    zee_playlist.extend(channel_block)
                    continue
            i += 1
            
        # Output directory banayein agar na ho
        os.makedirs("output", exist_ok=True)
        
        output_file = "output/zee_channels.m3u"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(zee_playlist))
            
        print(f"Successfully saved Zee channels to {output_file}")
        
    except Exception as e:
        print(f"Error fetching or parsing playlist: {e}")
        exit(1)

if __name__ == "__main__":
    fetch_and_filter_zee()
