import os, sys

audio_extensions = ["mp3", "aac", "m4a", "wav", "flac", "alac", "mka", "dts", "ac3", "ogg", "opus", "3gp", "MTS"]
video_extensions = ['mp4', 'mkv', 'mov', 'flv', 'wmv', 'avi', 'webm']

def select_file(relevant_extensions, audio_or_video):
    
    compatible_file_list = [filename for filename in os.listdir() if filename.split(".")[-1] in relevant_extensions]
    num_compatible_files = len(compatible_file_list)

    if num_compatible_files >= 1:

        for i in range(len(compatible_file_list)):
            print("{}. {} ".format(i+1, compatible_file_list[i]))

        chosen_file = input("Please select your desired {} file by entering its associated integer: "
            .format(audio_or_video))

        chosen_file_index = int(chosen_file)
        chosen_file = compatible_file_list[chosen_file_index - 1]
        return chosen_file
    
video_file = select_file(video_extensions, 'audio')
audio_file = select_file(audio_extensions, 'video')

audio_codecs = ['MP3', 'AAC', '16-bit WAV', '24-bit WAV', 'FLAC']

for i in range(len(audio_codecs)):
    print("{}. {} ".format(i+1, audio_codecs[i]))

chosen_codec = input("Enter a number between 1 and 5, where the number corresponds to your desired audio format: ")
codec_options = ['libmp3lame -q:a 0', 'aac -q:a 2', 'pcm_s16le', 'pcm_s24le', 'flac']

audio_codec = codec_options[int(chosen_codec) - 1]

if audio_codec == 'libmp3lame -q:a 0':
    sample_rate_options = ['44.1 kHz', '48 kHz']
else:
    sample_rate_options = ['44.1 kHz', '48 kHz', '96 kHz', '192 kHz']

for i in range(len(sample_rate_options)):
    print("{}. {} ".format(i+1, sample_rate_options[i]))

chosen_sr = input("Enter a number between 1 and 4, where the number corresponds to your desired audio sample rate: ")
sample_rate = sample_rate_options[int(chosen_sr) - 1]

output_name = input("What would you like the output video to be named? ")

os.system('ffmpeg -i "{}" -i "{}" -filter_complex "[0:a:0]loudnorm[va];[1:a:0]loudnorm[aa];[va][aa]amix=2:first[aout]" \
    -map 0:V:0 -map "[aout]" -c:v copy -c:a {} -resampler soxr -ar {} "{}".mkv'
    .format(video_file, audio_file, audio_codec, sample_rate, output_name))

input('Done!')