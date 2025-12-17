import os
from moviepy.config import change_settings

# --- FORCE IMAGEMAGICK PATH ---
# We point to the 'magick.exe' file inside the folder you installed it in.
# The 'r' before the quote ensures the backslashes don't cause errors.

IMAGEMAGICK_BINARY = r"D:\IMAGEMAGICK\ImageMagick-7.1.2-Q16-HDRI\magick.exe"

if os.path.exists(IMAGEMAGICK_BINARY):
    change_settings({"IMAGEMAGICK_BINARY": IMAGEMAGICK_BINARY})
else:
    print(f"⚠️ Warning: Could not find ImageMagick at {IMAGEMAGICK_BINARY}")

# ... (Keep the rest of your imports like requests, edge_tts, etc. below) ...
import requests
import edge_tts
# etc...

import requests
import edge_tts
import asyncio
import os
from bs4 import BeautifulSoup
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, ColorClip

# --- 1. AI SCRIPT GENERATOR ---
def get_ai_script(topic):
    print(f"🧠 Asking AI about: {topic}...")
    try:
        # Prompt Pollinations for a script
        prompt = f"Write a 2-sentence hook for an Instagram Reel about {topic}. No emojis."
        url = f"https://text.pollinations.ai/{prompt}"
        response = requests.get(url, timeout=5)
        return response.text.strip()
    except:
        return f"Did you know {topic} is fascinating? It changes how we see the world."

# --- 2. SMART VIDEO FINDER ---
def get_video_url(topic):
    print(f"🕵️ Looking for video: {topic}...")
    
    SAFE_BACKUP = "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    clean_topic = topic.lower().strip()
    words = clean_topic.split()
    
    # Search strategies
    search_attempts = [clean_topic.replace(" ", "-")]
    if len(words) > 1:
        search_attempts.append(words[-1]) 
        search_attempts.append(words[0]) 

    for search_term in search_attempts:
        print(f"   🔎 Trying search term: '{search_term}'...")
        try:
            search_url = f"https://mixkit.co/free-stock-video/{search_term}/"
            response = requests.get(search_url, headers=headers, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')
            videos = soup.find_all('video')
            
            if videos:
                for vid in videos:
                    src = vid.get('src')
                    if src and ".mp4" in src:
                        print(f"   ✅ Found video for '{search_term}'!")
                        return src
        except Exception:
            continue

    print(f"⚠️ All searches failed. Using Google Backup.")
    return SAFE_BACKUP

# --- 3. DOWNLOADER ---
def download_file(url, filename):
    print(f"⬇️ Downloading from {url}...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, stream=True, headers=headers, verify=False)
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        
        if os.path.getsize(filename) < 100000:
            print("❌ Downloaded file is corrupt/empty.")
            return False
        return True
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False

# --- 4. CAPTION GENERATOR (The New Feature) ---
def add_captions_to_video(video_path, script_text, output_path):
    """
    Splits the script into chunks and overlays them as stylized captions.
    """
    print("📝 Generating subtitles...")
    try:
        # Load Video
        video = VideoFileClip(video_path)
        video_duration = video.duration
        
        # Process Script into 5-word chunks
        words = script_text.split()
        chunk_size = 5
        text_chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
        
        # Calculate timing
        if len(text_chunks) == 0: return False
        time_per_chunk = video_duration / len(text_chunks)
        
        text_clips = []
        
        # Create Text Clips
        for i, chunk in enumerate(text_chunks):
            start_time = i * time_per_chunk
            
            # Create the text overlay (Yellow text, Black outline)
            # NOTE: ImageMagick must be installed for TextClip to work
            txt_clip = (TextClip(chunk, fontsize=24, color='yellow', font='Arial-Bold', 
                                 stroke_color='black', stroke_width=2, method='caption', 
                                 size=(video.w * 0.9, None))
                        .set_position(('center', 0.80), relative=True) # Center screen
                        .set_start(start_time)
                        .set_duration(time_per_chunk))
            
            text_clips.append(txt_clip)

        # Composite everything
        final_video = CompositeVideoClip([video] + text_clips)
        final_video.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=24, logger=None)
        
        video.close()
        final_video.close()
        return True

    except Exception as e:
        print(f"⚠️ Subtitle generation failed (likely ImageMagick missing): {e}")
        return False

# --- 5. MAIN VIDEO EDITOR ---
def make_reel(topic):
    # Ensure static directory exists
    if not os.path.exists('static'):
        os.makedirs('static')

    video_raw_path = "static/temp_video.mp4"
    audio_path = "static/temp_audio.mp3"
    intermediate_path = "static/temp_reel_no_subs.mp4"
    final_path = "static/final_reel.mp4"
    
    # Cleanup old files
    for p in [final_path, intermediate_path]:
        if os.path.exists(p): os.remove(p)

    print(f"🎬 Starting Reel Generation for: {topic}")

    try:
        # 1. Generate Script & Audio
        script = get_ai_script(topic)
        asyncio.run(edge_tts.Communicate(script, "en-US-ChristopherNeural").save(audio_path))

        # 2. Find & Download Video
        vid_url = get_video_url(topic)
        download_success = download_file(vid_url, video_raw_path)

        # 3. Create Base Video (Crop, Loop, Add Audio)
        audio = AudioFileClip(audio_path)
        
        if download_success:
            video = VideoFileClip(video_raw_path)
            # Loop video to match audio length
            video = video.loop(duration=audio.duration + 1)
            
            # Crop to Vertical 9:16
            w, h = video.size
            target_ratio = 9/16
            if w/h > target_ratio:
                new_w = h * target_ratio
                video = video.crop(x1=w/2 - new_w/2, x2=w/2 + new_w/2, width=new_w, height=h)
        else:
            # Emergency Background (Blue Screen)
            print("⚠️ Video download failed. Generating synthetic background.")
            video = ColorClip(size=(720, 1280), color=(0, 0, 100), duration=audio.duration + 2)
            
        # Combine Video + Audio
        base_video = video.set_audio(audio)
        
        # Save Intermediate Video (Required for clean captioning)
        print("💾 Saving intermediate video...")
        base_video.write_videofile(intermediate_path, codec='libx264', audio_codec='aac', fps=24, logger=None)
        
        # 4. Add Subtitles
        # We pass the intermediate video we just made
        success = add_captions_to_video(intermediate_path, script, final_path)
        
        # Fallback: If subtitles fail, just use the intermediate video as final
        if not success:
            print("⚠️ Using video without subtitles as fallback.")
            # Depending on OS, rename might fail if file exists, so we copy content or just serve intermediate
            # For simplicity in app.py, we will just ensure final_path exists
            import shutil
            shutil.copy(intermediate_path, final_path)

        print("🎉 SUCCESS! Reel Generated.")
        return script

    except Exception as e:
        print(f"❌ Critical Error in make_reel: {e}")
        return f"Error: {e}"