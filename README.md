# 🎵 Mashup Generator

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web_App-black?style=for-the-badge&logo=flask)
![FFmpeg](https://img.shields.io/badge/FFmpeg-Audio_Processing-green?style=for-the-badge&logo=ffmpeg)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

> A Python-based application that creates audio mashups by combining multiple audio files into a single track using **FFmpeg**, with both **CLI and Web Interface support**.

---

## ✨ Features

- 🎧 Generate mashups from multiple audio files  
- ⚡ Fast processing powered by **FFmpeg**  
- 🖥️ Command-line interface for quick usage  
- 🌐 Flask-based web application  
- 🔊 Outputs high-quality `.mp3` files  
- 💡 Beginner-friendly and easy to extend  

---

## 📸 Demo Workflow

Upload Audio Files → Processing → Mashup Generated → Download Output

---

## 📁 Project Structure

    ├── 102303830.py        # Core Logic (CLI Script)
    ├── app.py             # Flask Web Application
    ├── requirements.txt   # Dependencies
    ├── output.mp3         # Generated Output File
    ├── .gitignore         # Ignored Files
    └── README.md          # Project Documentation

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|--------|
| Python 🐍 | Core logic |
| Flask 🌐 | Web framework |
| FFmpeg 🎶 | Audio processing |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

    git clone https://github.com/Kashish101204/mashup.git
    cd mashup

---

### 2️⃣ Create Virtual Environment (Recommended)

    python -m venv venv

Activate it:

**Windows**

    venv\Scripts\activate

**Mac/Linux**

    source venv/bin/activate

---

### 3️⃣ Install Dependencies

    pip install -r requirements.txt

---

### 4️⃣ Install FFmpeg

Download FFmpeg from:  
👉 https://ffmpeg.org/download.html  

Add it to your system PATH.

Check installation:

    ffmpeg -version

---

## ▶️ Usage

### 🔹 Run CLI Version

    python 10230830.py

---

### 🔹 Run Web Application

    python app.py

Open in browser:

    http://127.0.0.1:5000/

---

## ⚡ How It Works

1. User provides multiple audio files  
2. Files are processed using **FFmpeg**  
3. Audio streams are merged into one track  
4. Final mashup is saved as `output.mp3`  

---

## 📦 Requirements

Install all dependencies:

    pip install -r requirements.txt

---

## 🚀 Future Enhancements

- 🎚️ Add volume balancing  
- ⏱️ Trim and fade effects  
- 🎼 Beat synchronization  
- 📱 Deploy as a web app  
- 🎤 Live recording mashups  

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository  
2. Create your branch (`git checkout -b feature-name`)  
3. Commit changes (`git commit -m "Add feature"`)  
4. Push (`git push origin feature-name`)  
5. Open a Pull Request  

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 💡 Author

**Avnoor Kamboj**

---

## ⭐ Support

If you like this project:

- ⭐ Star the repository  
- 🍴 Fork it  
- 🧑‍💻 Share with others  

---

> "Code + Creativity = Music Magic 🎶"
