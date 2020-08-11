# api.py
# -*- coding: utf-8 -*-

import requests
import asyncio

import cv2


SERVER_ADDRESS = 'http://127.0.0.1:80/imageprocess'
# SERVER_ADDRESS = 'https://separecog-srv.herokuapp.com/imageprocess'
WAIT_TIME_SECONDS = 1

cv2.namedWindow("Face recognition", cv2.WINDOW_AUTOSIZE)
vc = cv2.VideoCapture(0)
vc.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

content_type = 'image/jpeg'
headers = {'content-type': content_type}


async def processframe(j):
    try:
        tmpr = requests.post(SERVER_ADDRESS, data=j, headers=headers).json()
        # print(tmpr)
        return tmpr
    except Exception as e:
        print(e)
    ###


async def main():
    response = []

    if vc.isOpened():  # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        rval, frame = vc.read()

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        ret, jpeg = cv2.imencode('.jpg', image)
        jpeg_converted = jpeg.tostring()

        response = await processframe(jpeg_converted)

        for k in response:
            bounding_box = k['box']
            keypoints = k['keypoints']

            cv2.rectangle(frame,
                          (bounding_box[0], bounding_box[1]),
                          (bounding_box[0] + bounding_box[2], bounding_box[1] + bounding_box[3]),
                          (0, 255, 0),
                          2)

            # cv2.circle(frame, (keypoints['left_eye']), 2, (0, 155, 255), 2)
            # cv2.circle(frame, (keypoints['right_eye']), 2, (0, 155, 255), 2)
            # cv2.circle(frame, (keypoints['nose']), 2, (0, 155, 255), 2)
            # cv2.circle(frame, (keypoints['mouth_left']), 2, (0, 155, 255), 2)
            # cv2.circle(frame, (keypoints['mouth_right']), 2, (0, 155, 255), 2)
        cv2.putText(frame, f'Total faces: {len(response)}', (0, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
        cv2.imshow("Face recognition", frame)

        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break

    vc.release()
    cv2.destroyWindow("Face recognition")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
