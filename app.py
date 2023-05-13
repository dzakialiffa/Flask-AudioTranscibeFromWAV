from flask import Flask, render_template, request, redirect
import speech_recognition as sr
from pydub import AudioSegment
import io

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    transcript = ""
    if request.method == "POST":
        print("FORM DATA RECEIVED")

        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            # Mengompresi audio menggunakan pydub
            audio = AudioSegment.from_wav(file)
            compressed_audio = audio.export(format='wav', bitrate='64k')

            # Membaca audio yang sudah dikompresi menggunakan speech_recognition
            recognizer = sr.Recognizer()
            with io.BytesIO(compressed_audio.read()) as source:
                data = recognizer.record(source)

            # Melakukan pengenalan suara
            transcript = recognizer.recognize_google(data, key=None)

    return render_template('index.html', transcript=transcript)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
