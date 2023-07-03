from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

def gen_employee_card(employee, img_file_name):

    file_path = os.path.expanduser('C://Users/koharu/PycharmProjects/最終課題/work_with_tech/static/images/employee_card')
    page = canvas.Canvas(file_path +'/pdf' + employee[0] + '.pdf', pagesize=portrait(A4))

    # フォントを指定する
    pdfmetrics.registerFont(TTFont('HGRGE', 'C:/Windows/Fonts/HGRGE.ttc'))
    page.setFont('HGRGE', 20)

    # 文字列を書き込む
    page.drawString(70, 150, 'STAFF CARD')
    page.drawString(70, 120, employee[1])
    page.drawString(70, 80, employee[0])

    # 画像の書き込み
    img_file_path = os.path.expanduser('C://Users/koharu/PycharmProjects/最終課題/work_with_tech/static/images/employee_qrcode')
    page.drawImage(img_file_path + img_file_name, 180, 80, 100, 100)

    # 線の書き込み
    # 線の色、幅
    page.setStrokeColorRGB(0, 0, 0)
    page.setLineWidth(1)

    # 線の始点と終点の座標
    page.line(50, 50, 300, 50)
    page.line(50, 50, 50, 200)
    page.line(50, 200, 300, 200)
    page.line(300, 50, 300, 200)

    page.save()

