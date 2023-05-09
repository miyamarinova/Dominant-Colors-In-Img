from flask import Flask, render_template, url_for, request, send_from_directory
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from colorthief import ColorThief
import matplotlib.pyplot as plt
from colormap import rgb2hex

import os
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ahbchdj'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos,'Only images are allowed'),
            FileRequired('File field should not be empty')
        ]
    )
    submit =SubmitField('Upload')

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

def hextriplet(palette):
    hexi_palette = []
    for colortuple in palette:
        print('#' + ''.join(f'{i:02X}' for i in colortuple))
        hexi_palette.append('#' + ''.join(f'{i:02X}' for i in colortuple))
    return hexi_palette


@app.route('/', methods=['GET','POST'])
def upload_image():
    palette = []
    hexi_palette = []
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_file', filename=filename)
        path = "./uploads/"
        ct = ColorThief(path + filename)
        palette = ct.get_palette(color_count=5)
        hexi_palette = hextriplet(palette)

    else:
        file_url = None
    return render_template('index.html', form=form, file_url=file_url, palette_list=hexi_palette)



if __name__ == '__main__':
    app.run(debug=True)