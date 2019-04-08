import time

from mouse import Mouse
from keyboard import Keyboard
from screen import Screen


class MiningBot:

    def __init__(self):
        self.mouse = Mouse()
        self.keyboard = Keyboard()
        self.screen = Screen()
        
    def start(self):
        while True:
            self.warp_to_system(self.get_system())    
            if not self.belts_exist():
                continue
            
            self.warp_to_belt()
            while True:
                if not self.asteroids_exist('ore'):
                    break
                if self.mine() == 'full':
                    self.unload()
                    break
            
    def warp_to_system(self, name):
        self.set_destination(name)
        self.toggle('autopilot')
        while self.is_in_autopilot():
            time.sleep(10)
                    
    def warp_to_belt(self):
        self.select_hotspot()
        self.select_image('warp_button')
        time.sleep(60)
        
    def mine(self):
        self.approach()
        self.lock()
        self.toggle('miners')
        while True:
            time.sleep(10)
            if not self.is_locked():
                return 'depleted'
            if self.is_full():
                return 'full'
            
    def unload(self):
        self.warp_to_system('home')
        time.sleep(10)
        for ore in ['veldspar', 'dense_veldspar', 'concentrated_veldspar']:
            rect = self.screen.locate(ore, 0.9)
            if (rect != None):
                self.mouse.move_to_rect(rect)
                x, y, w, h = rect
                x -= 400
                rect = x, y, w, h
                self.mouse.drag_to_rect(rect, 'left')
        self.undock()
        
    def approach(self):
        self.select_hotspot()
        self.select_image('approach_button')
        time.sleep(60)
        
    def undock(self):
        self.select_image('undock_button')
        while self.is_in_station():
            time.sleep(10)
        
    def lock(self):
        self.select_image('lock_button')
        time.sleep(10)
            
    def set_destination(self, name):
        rect = self.screen.locate(name + '_system', 0.9)
        if rect == None:
            raise ValueError('Invalid destination: ' + name)
        self.mouse.click_rect(rect, 'right')
        self.mouse.move(30, 42)
        self.mouse.click('left')
        
    def change_overview(self, tab):
        rect = self.screen.locate(tab + '_overview')
        self.mouse.click_rect(rect, 'left')
        
    def toggle(self, module):
        if module == 'autopilot':
            self.select_image('autopilot_off')
        elif module == 'miners':
            for index in [1, 2]:
                self.keyboard.press('f' + str(index))
        else:
            raise ValueError('Invalid module: ' + module)
            
    def select_hotspot(self):
        self.mouse.click_point(1597, 195, 'left')
        time.sleep(1)
        
    def select_image(self, name):
        rect = self.screen.locate(name)
        self.mouse.click_rect(rect, 'left')
        time.sleep(1)
        self.mouse.move_to_point(1000, 500)
        time.sleep(1)
            
    def belts_exist(self):
        self.change_overview('belts')
        rect = self.screen.locate('asteroid_belt', 0.85)
        if rect == None:
            return False
        return True
            
    def asteroids_exist(self, type):
        self.change_overview('asteroids')
        if type not in ['ore', 'ice']:
            raise ValueError('Invalid asteroid type: ' + type)
        for size in ['large', 'medium', 'small']:
            rect = self.screen.locate(size + '_' + type + '_asteroid', 0.9)
            if rect != None:
                return True
        return False
        
    def get_system(self):
        return 'mine'
    
    def is_in_space(self):
        if self.screen.locate('autopilot_off', 0.9) == None:
            return False
        return True
        
    def is_in_station(self):
        return not self.is_in_space()
        
    def is_in_autopilot(self):
        if self.screen.locate('autopilot_on', 0.98) == None:
            return False
        return True
        
    def is_locked(self):
        if self.screen.locate('lock', 0.9) == None:
            return False
        return True    
        
    def is_full(self):
        if self.screen.locate('cargo_full', 0.98) == None:
            return False
        return True
        
if __name__ == "__main__":
    bot = MiningBot()
    time.sleep(2)
    bot.start()
