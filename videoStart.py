from handGesture import hand
import cv2
import mediapipe as mp
from data import serverData as env
from websockets import serve
import asyncio
import sys
import json

async def Handler(websocket):
    print("waiting for the client messgae")
    print("data from the client:", await websocket.recv())
    try:
        hands = hand.Hand(max_hands=1)
        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            res = hand.DetectHands(frame, hands)
            if not res['status']:
                break

            img = res["image"]
            print(res["data"])
            #send data to the websocket
            await websocket.send(json.dumps(res['data']))
            # Display the resulting image
            cv2.imshow('Hand Gestures', img)
            if cv2.waitKey(1) == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        sys.exit()
    except KeyboardInterrupt:
        print("Force exit operation")
        cap.release()
        cv2.destroyAllWindows()
        sys.exit()

try:
    async def main():
        print(f"server created on {env.PORT} port")
        async with serve(Handler, env.HOST, env.PORT, ping_interval=None):
            await asyncio.Future()  # run forever
    asyncio.run(main())

except KeyboardInterrupt:
    print("Force exit operation")
    cv2.destroyAllWindows()
    sys.exit()
