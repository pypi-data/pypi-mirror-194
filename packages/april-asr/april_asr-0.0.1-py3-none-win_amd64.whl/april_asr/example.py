import librosa
import april_asr as april
import sys

def example_handler(result_type, tokens):
    s = ""
    for token in tokens:
        s = s + token.token
    
    if result_type == april.Result.FinalRecognition:
        print("@"+s)
    elif result_type == april.Result.PartialRecognition:
        print("-"+s)
    else:
        print("")

def run(model_path, wav_file_path):
    # Load the model
    model = april.Model(model_path)

    # Print the metadata
    print("Name: " + model.get_name())
    print("Description: " + model.get_description())
    print("Language: " + model.get_language())

    # Create a session
    session = april.Session(model, example_handler)

    # Read the audio file, works with any audio filetype librosa supports
    data, sr = librosa.load(wav_file_path, sr=model.get_sample_rate(), mono=True)
    data = (data * 32767).astype("short").astype("<u2").tobytes()

    # Feed the audio data
    session.feed_pcm16(data)

    # Flush to finish off
    session.flush()

def main():
    # Parse arguments
    args = sys.argv
    if len(args) != 3:
        print("Usage: " + args[0] + " /path/to/model.april /path/to/file.wav")
    else:    
        run(args[1], args[2])

if __name__ == "__main__":
    main()