# Traces flightpaths of birds from a video
# skittlemittle 2021

import cv2
import numpy as np
import sys

# config
feature_params = dict(maxCorners=200, qualityLevel=0.3, minDistance=7, blockSize=7)
lk_params = dict(
    winSize=(15, 15),
    maxLevel=2,
    criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03),
)


class BirdTracker:
    def __init__(self, video_src, draw: bool):
        self.cap = cv2.VideoCapture(video_src)
        self.find_features_interval = 5
        self.frame_count = 0
        self.tracks = []

        self.draw = draw
        self.colors = np.random.randint(0, 255, (500, 3))

    def _draw(self, frame, lines: list):
        cv2.polylines(frame, [np.int32(l) for l in lines], False, (55, 200, 243), 2)
        cv2.imshow("osas", frame)

    def toggle_draw(self):
        self.draw = not self.draw

    def track(self):
        while True:
            _ret, frame = self.cap.read()
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
                good = d < 30  # NOTE: bigger number for fater bird
                new_tracks = []

                for track, (x, y), good_flag in zip(
                    self.tracks, p1.reshape(-1, 2), good
                ):
                    if not good_flag:
                        continue

                    track.append((x, y))
                    new_tracks.append(track)

                self.tracks = new_tracks
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
    except:
        video = "cropped.mp4"
    BirdTracker(video, True).track()
    cv2.destroyAllWindows()
