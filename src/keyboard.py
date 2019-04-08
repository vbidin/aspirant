import pyautogui


class Keyboard:

    def __init__(self):
        pyautogui.PAUSE = 0
        
    def hold(self, key):
        pyautogui.keyDown(key)
        
    def release(self, key):
        pyautogui.keyUp(key)
        
    def press(self, key):
        self.hold(key)
        self.release(key)
    
    def hotkey(self, keys):
        for key in keys:
            self.hold(key)
        for key in reversed(keys):
            self.release(key)