import os
import sys
import shutil
import time
import argparse
from yt_dlp import YoutubeDL
from moviepy.editor import AudioFileClip, concatenate_audioclips, afx

# --- Configuration & Setup ---
ROLL_NUMBER = "102483084" 
TEMP_DIR = f"temp_mashup_{ROLL_NUMBER}"

def setup_environment():
    """
    Automatically detects ffmpeg.exe in the current folder 
    and tells the system to use it.
    """
    local_ffmpeg = os.path.join(os.getcwd(), "ffmpeg.exe")
    if os.path.exists(local_ffmpeg):
        os.environ["IMAGEIO_FFMPEG_EXE"] = local_ffmpeg
        # print(f"[System] Found local FFmpeg: {local_ffmpeg}")

def parse_arguments():
    """
    Parses command line arguments professionally using argparse.
    """
    parser = argparse.ArgumentParser(
        description="YouTube Mashup Generator",
        usage=f"python {sys.argv[0]} <Singer> <Count> <Duration> <Output>"
    )
    
    # Positional Arguments
    parser.add_argument("singer", help="Name of the singer (e.g., 'Ed Sheeran')")
    parser.add_argument("count", type=int, help="Number of videos (Must be > 10)")
    parser.add_argument("duration", type=int, help="Duration in seconds (Must be > 20)")
    parser.add_argument("output", help="Output filename (e.g., mashup.mp3)")

    args = parser.parse_args()

    # Business Logic Validation (Assignment Constraints)
    if args.count <= 10:
        parser.error(f"Number of videos must be > 10. You provided: {args.count}")
    if args.duration <= 20:
        parser.error(f"Duration must be > 20 seconds. You provided: {args.duration}")
    
    # Ensure output has .mp3 extension
    if not args.output.lower().endswith('.mp3'):
        args.output += '.mp3'
        
    return args

def download_audio(singer, count):
    """
    Downloads audio streams using yt-dlp.
    """
    print(f"\n[1/3] Downloading {count} tracks for '{singer}'...")
    
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        # Download slightly more to account for failures
        'max_downloads': count + 5, 
        'outtmpl': f'{TEMP_DIR}/%(title)s.%(ext)s',
        'ignoreerrors': True,
        'quiet': True,
        'no_warnings': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([f"ytsearch{count + 5}:{singer}"])
        except Exception as e:
            # We ignore max-download errors as they are expected when limit is reached
            pass

def process_audio(count, duration, output_file):
    """
    Cuts, processes, and merges audio using MoviePy.
    """
    print(f"\n[2/3] Processing audio (Trimming first {duration}s)...")
    
    # Find all supported audio files in the temp directory
    supported_exts = ('.webm', '.m4a', '.mp3', '.mp4')
    files = [f for f in os.listdir(TEMP_DIR) if f.lower().endswith(supported_exts)]
    
    if len(files) < count:
        print(f"Warning: Only found {len(files)} valid files (Requested {count}).")
    
    clips = []
    processed_count = 0

    # Sort files to ensure the order is consistent
    files.sort()

    for filename in files:
        if processed_count >= count:
            break
            
        filepath = os.path.join(TEMP_DIR, filename)
        try:
            # Load Audio
            clip = AudioFileClip(filepath)
            
            # Smart Cut: Don't crash if video is shorter than duration
            cut_time = min(duration, clip.duration)
            subclip = clip.subclip(0, cut_time)
            
            # Audio Polish: Fade In/Out individual clips slightly for smoothness
            subclip = subclip.fx(afx.audio_fadein, 0.5).fx(afx.audio_fadeout, 0.5)
            
            clips.append(subclip)
            processed_count += 1
            
            # Print a clean progress indicator
            print(f"  [+] Processed: {filename[:40]}...")
            
        except Exception as e:
            print(f"  [!] Skipping corrupt file: {filename}")

    if not clips:
        print("Error: No audio clips could be processed.")
        return

    print(f"\n[3/3] Merging {len(clips)} clips into final Mashup...")
    
    try:
        final_mashup = concatenate_audioclips(clips)
        
        # Premium Feature: Fade in start and fade out end of the Master Track
        final_mashup = final_mashup.fx(afx.audio_fadein, 2).fx(afx.audio_fadeout, 2)
        
        final_mashup.write_audiofile(output_file, verbose=False, logger=None)
        
        print(f"\n" + "="*50)
        print(f" SUCCESSFULLY COMPLETED ")
        print(f" Output File: {os.path.abspath(output_file)}")
        print(f"="*50)
        
        # Close handles to release files
        final_mashup.close()
        for c in clips:
            c.close()
            
    except Exception as e:
        print(f"Merge Failed: {e}")

def cleanup():
    """Safe cleanup of temp directories."""
    if os.path.exists(TEMP_DIR):
        try:
            shutil.rmtree(TEMP_DIR)
            print("\n[System] Cleaned up temporary files.")
        except Exception:
            pass

def main():
    setup_environment()
    
    # Use argparse to handle inputs robustly
    try:
        args = parse_arguments()
    except SystemExit:
        # If arguments are wrong, argparse handles the error message and exits
        return

    start_time = time.time()
    
    try:
        download_audio(args.singer, args.count)
        process_audio(args.count, args.duration, args.output)
    except KeyboardInterrupt:
        print("\n[!] Process cancelled by user.")
    except Exception as e:
        print(f"\n[!] Critical Error: {e}")
    finally:
        cleanup()
        elapsed = time.time() - start_time
        print(f"Total execution time: {elapsed:.2f} seconds")

if __name__ == "__main__":
    main()