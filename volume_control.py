import cv2
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def _get_endpoint():
    speakers = AudioUtilities.GetSpeakers()
    if hasattr(speakers, "EndpointVolume"):      
        return speakers.EndpointVolume
    interface = speakers.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)  
    return cast(interface, POINTER(IAudioEndpointVolume))


class VolumeController:
    def __init__(self, min_ratio=0.25, max_ratio=1.4):
        self.endpoint = _get_endpoint()
        self.level = self.endpoint.GetMasterVolumeLevelScalar()   
        self.min_ratio, self.max_ratio = min_ratio, max_ratio

    def update(self, ratio, locked):
        if locked:
            return
        target = float(np.interp(ratio, (self.min_ratio, self.max_ratio), (0.0, 1.0)))
        self.level += (target - self.level) * 0.3    
        self.endpoint.SetMasterVolumeLevelScalar(self.level, None)

    def draw(self, frame):
        h = frame.shape[0]
        top, bottom, x = 100, h - 80, 40
        fill = int(np.interp(self.level, (0, 1), (bottom, top)))
        cv2.rectangle(frame, (x, top), (x + 30, bottom), (255, 255, 255), 2)
        cv2.rectangle(frame, (x, fill), (x + 30, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, f"{int(self.level * 100)}%", (x - 10, bottom + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)