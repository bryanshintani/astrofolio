from flask import current_app
import secrets
import os

def save_image(form_image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_fn = random_hex + f_ext
    image_path = os.path.join(current_app.root_path, 'static/blog_pics', image_fn)
    form_image.save(image_path)

    return image_fn
