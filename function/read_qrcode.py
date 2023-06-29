import cv2
import time

def read_qrcode():
    """
    PCのカメラを起動してQRコードを読み込む。


    :return:
    """
    camera_id = 0
    delay = 1
    window_name = 'OpenCV QR Code'

    qcd = cv2.QRCodeDetector()
    cap = cv2.VideoCapture(camera_id)

    str = ''

    while True:
        ret, frame = cap.read()

        if ret:
            ret_qr, decoded_info, points, _ = qcd.detectAndDecodeMulti(frame)
            if ret_qr:
                for s, p in zip(decoded_info, points):
                    if s:
                        str=s
                        color = (0, 255, 0)
                        time.sleep(2)
                        break
                    else:
                        color = (0, 0, 255)
                    frame = cv2.polylines(frame, [p.astype(int)], True, color, 8)
                    if str:
                        break
            cv2.imshow(window_name, frame)

        if str:
            break
        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break

    cv2.destroyWindow(window_name)
    return str