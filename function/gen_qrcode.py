import qrcode
import os
from PIL import Image

qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)

qr.add_data('watanabe_koharu4224112')

img = qr.make_image()

# file_path = os.path.expanduser('~/Downloads/QRCode.png')
file_path = './images/employee_id/name_id.png'

img.save(file_path)

