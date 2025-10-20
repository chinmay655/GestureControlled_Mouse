import pyautogui, time, numpy as np
from PIL import ImageGrab

# try optional volume control library (Windows)
try:
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    from comtypes import CLSCTX_ALL
    has_pycaw = True
except Exception:
    has_pycaw = False

class MouseController:
    def __init__(self, smoothening=5):
        self.smoothening = smoothening
        self.prev_x, self.prev_y = 0, 0
        self.curr_x, self.curr_y = 0, 0
        self.dragging = False
        self.screen_w, self.screen_h = pyautogui.size()

        # volume control setup (Windows)
        if has_pycaw:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self.volume = interface.QueryInterface(IAudioEndpointVolume)
            self.vol_min, self.vol_max = self.volume.GetVolumeRange()[:2]
        else:
            self.volume = None

    def _map_to_screen(self, x, y, cam_w, cam_h):
        # landmarks are pixel coordinates wrt camera frame; map to screen coords
        screen_x = np.interp(x, [0, cam_w], [0, self.screen_w])
        screen_y = np.interp(y, [0, cam_h], [0, self.screen_h])
        # smoothing
        self.curr_x = self.prev_x + (screen_x - self.prev_x) / self.smoothening
        self.curr_y = self.prev_y + (screen_y - self.prev_y) / self.smoothening
        self.prev_x, self.prev_y = self.curr_x, self.curr_y
        return int(self.curr_x), int(self.curr_y)

    def perform_action(self, gesture, landmarks, frame):
        action = gesture.get('action', 'none')
        if action == 'none':
            return
        cam_h, cam_w = frame.shape[0], frame.shape[1]

        # move: use index fingertip
        if action == 'move':
            idx = landmarks[8]
            x, y = self._map_to_screen(idx['x'], idx['y'], cam_w, cam_h)
            pyautogui.moveTo(x, y, duration=0)  # instant move

            # optionally handle volume control when far apart (caller passed distance)
            dist = gesture.get('distance_idx_thumb', None)
            if dist is not None and dist > 120:
                self._set_volume_by_distance(dist, min_d=120, max_d=300)
            return

        if action == 'left_click':
            idx = landmarks[8]
            x, y = self._map_to_screen(idx['x'], idx['y'], cam_w, cam_h)
            pyautogui.click(x, y, button='left')
            return

        if action == 'right_click':
            idx = landmarks[8]
            x, y = self._map_to_screen(idx['x'], idx['y'], cam_w, cam_h)
            pyautogui.click(x, y, button='right')
            return

        if action == 'drag':
            idx = landmarks[8]
            x, y = self._map_to_screen(idx['x'], idx['y'], cam_w, cam_h)
            if not self.dragging:
                pyautogui.mouseDown(x, y, button='left')
                self.dragging = True
            else:
                pyautogui.moveTo(x, y)
            return

        if action == 'screenshot':
            # take screenshot of the screen and save to file
            timestamp = int(time.time())
            img = ImageGrab.grab()
            filename = f'screenshot_{timestamp}.png'
            img.save(filename)
            print(f'[+] Screenshot saved: {filename}')
            return

    def _set_volume_by_distance(self, dist, min_d=100, max_d=350):
        # Map distance to volume level between -65.25 and 0.0 (if pycaw available)
        if self.volume:
            # clamp
            d = max(min(dist, max_d), min_d)
            vol_norm = (d - min_d) / (max_d - min_d)  # 0..1
            vol_db = self.vol_min + vol_norm * (self.vol_max - self.vol_min)
            self.volume.SetMasterVolumeLevel(vol_db, None)
            print(f'[VOL] Set volume (pycaw) to db: {vol_db:.2f}')
        else:
            # fallback: just print or use scroll to demo
            print(f'[VOL] (fallback) distance={dist} -> adjust system volume manually or install pycaw.')
