#Импорт
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'img')
ALLOWED = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024


def allowed(name):
    return '.' in name and name.rsplit('.', 1)[1].lower() in ALLOWED


def unique_name(folder, filename):
    base, ext = os.path.splitext(filename)
    i = 1
    while os.path.exists(os.path.join(folder, filename)):
        filename = f"{base}_{i}{ext}"
        i += 1
    return filename


def get_images():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    return sorted(os.listdir(UPLOAD_FOLDER))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('image')
        if file and file.filename:
            if allowed(file.filename):
                filename = unique_name(UPLOAD_FOLDER, secure_filename(file.filename))
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                return redirect(url_for('index', selected=filename))
            return redirect(url_for('index'))

        return render_template(
            'index.html',
            selected_image=request.form.get('image-selector', 'logo.svg'),
            text_top=request.form.get('textTop'),
            text_bottom=request.form.get('textBottom'),
            text_top_y=request.form.get('textTop_y'),
            text_bottom_y=request.form.get('textBottom_y'),
            selected_color=request.form.get('color-selector'),
            images=get_images()
        )

    return render_template(
        'index.html',
        selected_image=request.args.get('selected', 'logo.svg'),
        images=get_images()
    )


@app.route('/download/<path:filename>')
def downloadFile(filename):
    return send_from_directory(UPLOAD_FOLDER, os.path.basename(filename), as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)