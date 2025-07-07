import os
import subprocess
from backend.app.workers import celery
from backend.app.utils.file_storage import save_processed_file
from backend.app.utils.video_optimizer import generate_thumbnail

@celery.task(name="process_video")
def process_video(video_path, output_dir=None):
    """
    Compresses and optimizes a video asynchronously.

    Args:
        video_path (str): Path to the uploaded raw video.
        output_dir (str, optional): Directory to save optimized video and thumbnail.
    """
    try:
        print(f"[🔄] Starting video processing for {video_path}...")

        # Default output directory
        output_dir = output_dir or os.path.dirname(video_path)

        filename = os.path.basename(video_path)
        name, ext = os.path.splitext(filename)
        output_video_path = os.path.join(output_dir, f"{name}_compressed{ext}")
        thumbnail_path = os.path.join(output_dir, f"{name}_thumb.jpg")

        # Compress video using ffmpeg (adjust bitrate as needed)
        command = [
            "ffmpeg", "-i", video_path,
            "-b:v", "1M", "-vcodec", "libx264", "-preset", "fast",
            output_video_path
        ]
        subprocess.run(command, check=True)

        print(f"[✅] Compressed video saved: {output_video_path}")

        # Generate a thumbnail
        generate_thumbnail(video_path, thumbnail_path)
        print(f"[🖼️] Thumbnail saved: {thumbnail_path}")

        # Optional: save to cloud / move to media folder
        save_processed_file(output_video_path)
        save_processed_file(thumbnail_path)

        print(f"[✅] Video processing completed for {video_path}")

    except subprocess.CalledProcessError as e:
        print(f"[❌] FFmpeg processing failed: {e}")
    except Exception as e:
        print(f"[❌] Video processing error: {e}")
