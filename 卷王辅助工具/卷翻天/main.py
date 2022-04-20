import cv2
import win32gui
import win32con
import time
# from pygame import mixer # 需要提示音的的话先安装pygame


def main():
    # mixer.init() # 音频初始化
    # mixer.music.load('红警核弹发射音效.mp3') # 加载提示音
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW) # 打开usb摄像头，第一个参数是0还是1自己试一下
    detector=cv2.CascadeClassifier("haarcascade_frontalface_default.xml") # 读取opencv级联分类器人脸识别文件

    while cap.isOpened():
        start = time.time() # 记录开始时间
        ok, img = cap.read() # 读如一帧画面
        if not ok: # 没有画面，退出
            print("未读取到图片!")
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # RGB转灰度图，进行人脸识别
        faces = detector.detectMultiScale(gray, 1.3, 5) # 人脸检测

        for (x, y, w, h) in faces: # 遍历识别到的人脸
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2) # 框出人脸

        if len(faces) > 0: # 检测到了人脸
            hwnd = win32gui.FindWindow(None, "植物大战僵尸中文版") # 获取应用窗口句柄，第二个参数为应用名称
            if win32gui.IsIconic(hwnd): # 如果该应用界面没有最大化，把它最大化，已经最大化了不做任何操作
                # mixer.music.play() # 播放红警核弹发射提示音
                win32gui.ShowWindow(hwnd, win32con.SW_SHOWMAXIMIZED) # 将该应用最大化

        key = cv2.waitKey(80) # 每帧延时80ms
        end = time.time() # 记录结束时间
        cv2.putText(img, "FPS:%.1f" % (1 / (end-start)), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1) # 计算帧率
        cv2.imshow("frame", img) # 显示画面

        if key & 0xFF == ord("q"): # 按q退出（鼠标指针在摄像头画面上点一下，输入英文q）
            break

    cap.release() # 释放摄像头并销毁所有窗口
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
    print("end")


