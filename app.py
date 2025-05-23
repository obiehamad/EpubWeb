from flask import Flask, request, render_template, send_file
from ebooklib import epub
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        epub_file = request.files.get('epub_file')
        image_file = request.files.get('image_file')

        if not epub_file or not image_file:
            return "Please upload both an EPUB file and an image."

        epub_path = os.path.join(UPLOAD_FOLDER, secure_filename(epub_file.filename))
        image_path = os.path.join(UPLOAD_FOLDER, secure_filename(image_file.filename))

        epub_file.save(epub_path)
        image_file.save(image_path)

        book = epub.read_epub(epub_path)
        with open(image_path, 'rb') as img_file:
            img_content = img_file.read()

        img_name = os.path.basename(image_path)
        img_item = epub.EpubItem(uid=img_name, file_name='images/' + img_name,
                                 media_type='image/jpeg', content=img_content)
        book.add_item(img_item)

        output_path = os.path.join(UPLOAD_FOLDER, 'modified.epub')
        epub.write_epub(output_path, book)

        return send_file(output_path, as_attachment=True)

    return render_template('index.html')
