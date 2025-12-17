# 🧞‍♂️ Reel Genie AI (AutoReel Studio)
**“Your wish is our command.”**

An AI-powered automated video generator that creates **viral Instagram Reels, YouTube Shorts, and TikToks** from a simple text prompt.

---

## ✨ Overview

**Reel Genie AI** is a full-stack web application that acts as your personal AI video production team.  
Just enter a topic (for example: *“The history of coffee”* or *“Cyberpunk city”*), and the Genie will automatically:

- 🧠 Write a viral script with a strong hook and engaging narrative  
- 🎙️ Generate realistic voiceovers using Neural Text-to-Speech  
- 🎬 Fetch relevant stock footage automatically  
- 📝 Add burned-in, timed captions (Alex Hormozi style)  
- 🎥 Render a ready-to-post vertical video (9:16)  

All this happens in **one click**, with **zero video editing skills required**.

---

## 🚀 Features

- One-Click Reel Generation  
- AI Script Writing  
- Neural Voiceovers (Microsoft Edge TTS)  
- Smart Stock Video Search  
- Auto Captions (Yellow-Black Style)  
- Cinematic Genie-Themed UI  
- HD Vertical Output (9:16)

---

## 🛠️ Tech Stack

### Backend
- Python  
- Flask  

### Video & Audio Processing
- MoviePy  
- ImageMagick  
- Edge-TTS  

### Web Scraping
- BeautifulSoup4  
- Requests  

### Frontend
- HTML5  
- CSS3  
- JavaScript  
- Bootstrap 5  

---

## ⚙️ Prerequisites

Ensure the following are installed:

- Python 3.8+  
- ImageMagick (Critical for subtitles)

### ImageMagick Installation (Windows)

During installation, make sure to:
- ✅ Check **“Install legacy utilities (e.g. convert)”**  
- ✅ Check **“Add to system PATH”**

---

## Project Structure

    reel-genie-ai/
    │ 
    ├──app.py                  # Main Flask server
    ├── logic.py                
    ├── requirements.txt        # Python dependencies
    │
    ├── static/
    │       ├── genie-logo.png      # Landing page logo
    │       ├── genie-loading.png   # Loading animation
    │       ├── temp_video.mp4      # Temporary video file
    │       ├── temp_audio.mp3      # Generated voiceover
    │       └── final_reel.mp4      # Final output video
    │
    ├── templates/
    │   ├── landing.html        # Cinematic entry page
    │   └── index.html          # Main interface player
    │
    └── README.md               # Documentation

---

## 🤝 Contributing

Pull requests are welcome.

For major changes, please open an issue first.

---

## 🌟 Future Enhancements

- Multi-language voiceovers

- User-uploaded media

- Background music selection

- Prompt history & project saving

- Cloud deployment
