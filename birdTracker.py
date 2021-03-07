# Traces flightpaths of birds from a video
# skittlemittle 2021

import cv2
import numpy as np
import serial
import sys
import threading
import queue

# config
feature_params = dict(maxCorners=200, qualityLevel=0.3, minDistance=7, blockSize=7)
lk_params = dict(
    winSize=(15, 15),
    maxLevel=2,
    criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03),
)
rawPaths = queue.Queue()
pathMap = {}  # the current paths, excuse the stupid naming

# runs on a separate thread and keeps drawin
def plot():
    while True:
        lines = rawPaths.get()
        lKeys = []
        # update
        for l in lines:
            pathMap[l[0]] = l
            lKeys.append(l[0])
            print(l[0])
        print("")

        # send "finished" lines to be plotted
        r = []
        for k in pathMap:
            if not (k in lKeys):
                print("drawing", k)
                serialPort.write(pathMap[k])
                r.append(k)

        for i in r:
            pathMap.pop(i)


class BirdTracker:
    def __init__(self, video_src, rawPaths: queue, draw: bool):
        self.cap = cv2.VideoCapture(video_src)
        self.draw = draw
        self.rawPaths = rawPaths

        self.find_features_interval = 5
        self.frame_count = 0
        self.birdSpeed = [50, 2]  # bigger number for faster bird
        self.tracks = []

    def _draw(self, frame, lines: list):
        cv2.polylines(frame, [np.int32(l) for l in lines], False, (55, 200, 243), 2)
        cv2.imshow("", frame)

    def toggle_draw(self):
        self.draw = not self.draw

    def track(self):
        while True:
            _ret, frame = self.cap.read()
            if not _ret:
                break
            frame = cv2.resize(
                frame, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR
            )
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            vis = frame.copy()

            # we have something to track
            if len(self.tracks) > 0:
                # yea
                img0, img1 = self.prev_gray, frame_gray
                p0 = np.float32([t[-1] for t in self.tracks]).reshape(-1, 1, 2)
                p1, _st, _err = cv2.calcOpticalFlowPyrLK(
                    img0, img1, p0, None, **lk_params
                )
                p0r, _st, _err = cv2.calcOpticalFlowPyrLK(
                    img0, img1, p1, None, **lk_params
                )
                d = abs(p0 - p0r).reshape(-1, 2).max(-1)
                good = d[(d < self.birdSpeed[0]) & (d > self.birdSpeed[1])]
                new_tracks = []

                for track, (x, y), good_flag in zip(
                    self.tracks, p1.reshape(-1, 2), good
                ):
                    if not good_flag:
                        continue
                    track.append((x, y))
                    new_tracks.append(track)

                self.tracks = new_tracks
                self.rawPaths.put(self.tracks)
                if self.draw:
                    self._draw(vis, self.tracks)

            # find stuff to track
            if self.frame_count % self.find_features_interval == 0:
                mask = np.zeros_like(frame_gray)
                mask[:] = 255
                for x, y in [np.int32(t[-1]) for t in self.tracks]:
                    cv2.circle(mask, (x, y), 5, 0, -1)

                p = cv2.goodFeaturesToTrack(frame_gray, mask=mask, **feature_params)
                if p is not None:
                    for x, y in np.float32(p).reshape(-1, 2):
                        self.tracks.append([(x, y)])

            self.frame_count += 1
            self.prev_gray = frame_gray

            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break


if __name__ == "__main__":
    try:
        video = sys.argv[1]
        port = sys.argv[2]
    except:
        video = "cropped.mp4"
        port = "/dev/USB0"

    serialPort = serial.Serial(port, 115200, timeout=10)
    p = threading.Thread(target=plot, daemon=True)
    p.start()
    BirdTracker(video, rawPaths, True).track()
    cv2.destroyAllWindows()
