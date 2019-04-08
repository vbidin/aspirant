import pyautogui
import cv2


class Screen:

    def __init__(self):
        pyautogui.PAUSE = 0
        self.root = 'img'
        self.ext = '.png'
        self.source_path = self.root + '\\' + 'source' + self.ext
        self.method = eval('cv2.TM_CCORR_NORMED')

    def read_source(self):
        path = self.path('source')
        pyautogui.screenshot(path)
        return cv2.imread(path, 0)
        
    def read_template(self, path):
        img = cv2.imread(path, 0)
        if img is None:
            raise ValueError('Invalid image path: ' + path)
        return img
        
    def path(self, name):
        return self.root + '\\' + name + self.ext
        
    def locate(self, name, threshold=0):
        path = self.path(name)
        source = self.read_source()
        template = self.read_template(path)
        
        res = cv2.matchTemplate(source, template, self.method)
        min, max, min_loc, max_loc = cv2.minMaxLoc(res)
        print(name + " similiarity: " + str(max))
        
        if max < threshold:
            return None
        
        x, y = max_loc
        w, h = template.shape[::-1]        
        return x, y, w, h