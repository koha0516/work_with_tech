"""qrコードを生成する"""

import qrcode
import os
from PIL import Image

def gen_qr(employee_id):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)

    qr.add_data(employee_id)

    img = qr.make_image()

    file_name = 'QR' + employee_id + '.png'
    QR_PATH = 'C://Users/koharu/PycharmProjects/最終課題/work_with_tech/static/images/employee_qrcode'
    file_path = os.path.join(QR_PATH, file_name)

    img.save(file_path)

