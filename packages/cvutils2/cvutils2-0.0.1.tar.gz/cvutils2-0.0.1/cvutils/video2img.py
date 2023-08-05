import cv2


def Video2Pic(videoPath, imgPath, step):
    cap = cv2.VideoCapture(videoPath)
    # fps = cap.get(cv2.CAP_PROP_FPS)  # 获取帧率
    # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 获取宽度
    # height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 获取高度
    suc = cap.isOpened()  # 是否成功打开
    frame_count = 0
    while suc:
        frame_count += 1
        suc, frame = cap.read()
        if frame_count % step == 0:
            cv2.imwrite(imgPath + str(frame_count).zfill(5) + '.jpg', frame)
            # cv2.waitKey(1)
    cap.release()
    print("视频转图片结束！")


if __name__ == '__main__':
    Video2Pic(videoPath=r'C:\Programs\workspace\deep_learning\data\Float\VID_20211001_063550.mp4',
              imgPath=r'C:\Programs\workspace\deep_learning\data\Float\img\VID_20211001_063550',
              step=10)
