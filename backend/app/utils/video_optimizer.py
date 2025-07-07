import os
from moviepy.editor import VideoFileClip
from flask import current_app


def process_video_compression(
    input_path,
    output_path=None,
    target_bitrate=None,
    target_resolution=None
):
    """
    Compress and convert a video file to standard .mp4 format.

    Args:
        input_path (str): Path to original uploaded video (absolute).
        output_path (str): Optional; if not provided, saves as *_compressed.mp4 in same directory.
        target_bitrate (str): Bitrate string (e.g., '800k'). If None, use app config or default.
        target_resolution (tuple): (width, height). If None, use app config or original size.

    Returns:
        str: Absolute path to compressed video file.

    Raises:
        FileNotFoundError: If input file does not exist.
        RuntimeError: For compression failures.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Video not found at: {input_path}")

    # Get defaults from app config or fallback
    target_bitrate = target_bitrate or current_app.config.get("VIDEO_BITRATE", "800k")
    target_resolution = target_resolution or current_app.config.get("VIDEO_RESOLUTION", (720, 480))

    # Ensure output path
    if not output_path:
        base, _ = os.path.splitext(input_path)
        output_path = f"{base}_compressed.mp4"

    try:
        clip = VideoFileClip(input_path)

        # Resize (if resolution provided)
        if target_resolution:
            clip = clip.resize(newsize=target_resolution)

        # Write video with compression
        clip.write_videofile(
            output_path,
            bitrate=target_bitrate,
            codec="libx264",
            audio_codec="aac",
            preset="medium",
            threads=4,
            remove_temp=True,
            logger=None  # Suppress output in production
        )

        return output_path

    except Exception as e:
        raise RuntimeError(f"Video compression failed: {str(e)}")

    finally:
        # Explicitly close resources to avoid locks/memory leaks
        if 'clip' in locals():
            clip.close()
