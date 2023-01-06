import ffmpeg
import glob

# absolute path to search all text files inside a specific folder
path = r'*\*.png'
files = glob.glob(path)
print(files)
# List of input file names
input_files = files

# Set the output file name
output_file = 'output.mp4'

# Create an empty list of input streams
input_streams = []

# Iterate over the input files and create input streams
for file in input_files:
    stream = ffmpeg.input(file)
    input_streams.append(stream)

print(input_streams)
# Merge the input streams into a single stream
stream = ffmpeg.concat(*input_streams)
print(stream)
# Set the output stream
#output = ffmpeg.output(*input_streams, output_file)
output = ffmpeg.output(stream, output_file, r=1, vcodec='libx264')
# Run the ffmpeg command
try:
    ffmpeg.run(output, capture_stdout=True, capture_stderr=True, overwrite_output=True)

except ffmpeg.Error as e:
    print('stdout:', e.stdout.decode('utf8'))
    print('stderr:', e.stderr.decode('utf8'))
    raise e