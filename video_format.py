from moviepy.editor import VideoFileClip

def convert_mp4_to_mp3(input_path, output_path):
    try:
        # Load the video clip
        video_clip = VideoFileClip(input_path)

        # Extract audio from the video clip
        audio_clip = video_clip.audio

        # Write the audio to an MP3 file
        audio_clip.write_audiofile(output_path)

        # Close the video and audio clips
        video_clip.close()
        audio_clip.close()

        print(f"Conversion successful. MP3 file saved at {output_path}")

    except Exception as e:
        print(f"Error during conversion: {str(e)}")

# Example usage
input_file_path = "D:/Program Files/Desktop/Dodgeball/video/sound_effect.mp4"
output_file_path = "D:/Program Files/Desktop/Dodgeball/video/sound_effect.mp3"

convert_mp4_to_mp3(input_file_path, output_file_path)
