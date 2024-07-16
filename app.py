from flask import Flask, request, render_template, redirect
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/')
def index():
    return render_template('index.html', title="ColorAnalyzer")


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect('/')

    file = request.files['file']

    if file.filename == '':
        return redirect('/')

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        colors = get_colors(filepath)
        return render_template('colors.html', colors=colors, title="ColorAnalyzer")


def get_colors(image_path):
    image = Image.open(image_path)
    image_rgb = image.convert("RGB")
    colors = image_rgb.getcolors(maxcolors=1000000)
    colors = sorted(colors, reverse=True, key=lambda x: x[0])
    top_colors = colors[:10]
    return top_colors


if __name__ == '__main__':
    app.run(debug=True)
