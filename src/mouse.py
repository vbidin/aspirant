import pyautogui
import random


class Mouse:

    def __init__(self):
        pyautogui.PAUSE = 0

    def move(self, dx, dy):
        x, y = pyautogui.position()
        self.move_to_point(x+dx, y+dy)
        
    def move_to_point(self, x, y):
        pyautogui.moveTo(x, y, 0.5, pyautogui.easeOutQuad)

    def move_to_rect(self, rect):
        x, y = self.random_point(rect)
        self.move_to_point(x, y)
        
    def hold(self, button):
        pyautogui.mouseDown(button=button)
        
    def release(self, button):
        pyautogui.mouseUp(button=button)
        
    def click(self, button):
        self.hold(button)
        self.release(button)
        
    def click_point(self, x, y, button):
        self.move_to_point(x, y)
        self.click(button)
        
    def click_rect(self, rect, button):
        self.move_to_rect(rect)    
        self.click(button)
        
    def drag_to_point(self, x, y, button):
        self.hold(button)
        self.move_to_point(x, y)
        self.release(button)
    
    def drag_to_rect(self, rect, button):
        x, y = self.random_point(rect)
        self.drag_to_point(x, y, button)
        
    def random_point(self, rect):
        x, y, w, h = rect
        x = random.randint(x, x+w)
        y = random.randint(y, y+h)
        return x, y