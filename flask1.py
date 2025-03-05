from flask import Flask, request, render_template, send_file
from PIL import Image
import io
import base64
import tester

app = Flask(__name__)


def resize_image(image, size=(500, 300)):

    return image.resize(size)


@app.route('/', methods=['GET', 'POST'])
def index():
    images_info = []

    if request.method == 'POST':
        files = request.files.getlist('file')

        for file in files:
            if file and file.filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
                # Opens the image file using Pillow
                image = Image.open(file) # webkitdirectory

                # gets normal size, resizes, gets new size
                result,image2 = tester.classify_web(image)

                for x in range(len(image2)):
                    # Save processed image to in-memory buffer
                    buffer = io.BytesIO()
                    image2[x].save(buffer, format='PNG')
                    buffer.seek(0)

                    # Encode the image to base64
                    encoded_image = base64.b64encode(buffer.read()).decode('utf-8')
                    data_uri = f"data:image/png;base64,{encoded_image}"
                    

                    # Store the original size, new size, and image URI
                    images_info.append({
                        'data_uri': data_uri,
                        'result': result[x]
                    })

    return render_template('index.html', images_info=images_info)

if __name__ == '__main__':
    app.run(debug=False)
