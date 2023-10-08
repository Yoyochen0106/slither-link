
from typing_extensions import final
import pygame as pg

# represents transformation of origin from parent to child
class TF():
    def __init__(self, scale, pos) -> None:
        self.scale = scale
        self.pos = pos
    def fw_pt(self, pt):
        return pg.Vector2(
            pt[0]*self.scale+self.pos[0],
            pt[1]*self.scale+self.pos[1],
        )
    def bw_pt(self, pt):
        return pg.Vector2(
            (pt[0]-self.pos[0])/self.scale,
            (pt[1]-self.pos[1])/self.scale,
        )

class Game():
    def __init__(self, size) -> None:
        self.size = size

    # self.clues[y][x]
    def load_file(self, file):
        def parse_item(item):
            if item == '.':
                return -1
            return int(item)
        with open(file, 'r') as f:
            clues = [[parse_item(item) for item in line.strip()] for line in f.readlines()]
        self.clues = clues
    def draw(self, canvas, tf):
        self.font = pg.font.SysFont('Consolas', 30)
        for x in range(self.size[0]+1):
            for y in range(self.size[1]+1):
                color = (0, 0, 0)
                thickness = 5
                x_middle = x != self.size[0]
                y_middle = y != self.size[1]
                if x_middle:
                    pg.draw.line(canvas, color, tf.fw_pt((x, y)), tf.fw_pt((x+1, y)), thickness)
                if y_middle:
                    pg.draw.line(canvas, color, tf.fw_pt((x, y)), tf.fw_pt((x, y+1)), thickness)
                if x_middle and y_middle:
                    clue = self.clues[y][x]
                    if clue != -1:
                        text = self.font.render(str(clue), True, (0, 0, 0))
                        canvas.blit(text, tf.fw_pt((x, y)))

class GameControl():
    def __init__(self, game) -> None:
        self.game = game
    def handle_event(self, event):
        holding_left = False
        holding_right = False
        if event.type == pg.MOUSEBUTTONDOWN:
            game_pos = self.game_ctrl.tf.bw_pt(event.pos)``
            if event.button == pg.BUTTON_LEFT:
                holding_left = True
                self.fill_edge(game_pos)
            if event.button == pg.BUTTON_RIGHT:
                holding_right = True
                self.unfill_edge(game_pos)
        if event.type == pg.MOUSEMOTION:
            game_pos = self.game_ctrl.tf.bw_pt(event.pos)``
            if holding_left:
                self.fill_edge(game_pos)
            if holding_right:
                self.unfill_edge(game_pos)
        if event.type == pg.MOUSEBUTTONUP:
            holding_left = False
            holding_right = False
    def fill_edge(self, pos):
        pass
    def unfill_edge(self, pos):
        pass
    def nearest_edge(self, pos):
        x = int(pos[0])
        y = int(pos[1])
        if x+y < 1:
            if x < y:
                return ()
        
        

class App():
    def __init__(self):
        self.screen_size = (800, 600)

    def start(self):
        try:
            self._start()
        finally:
            self.cleanup()

    def _start(self):
        pg.init()
        self.screen = pg.display.set_mode(self.screen_size)
        self.clock = pg.time.Clock()
        self.game = Game((5, 5))
        self.game.load_file('./level.txt')
        self.game_ctrl = GameControl(self.game)
        self.game_ctrl.tf = TF(50, (200, 200))
        while True:
            self.clock.tick(30)
            for event in pg.event.get():
                if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key in (pg.K_F4, pg.K_q):
                    return
                self.game_ctrl.handle_event(event)
            self.screen.fill((192, 192, 192))
            self.game.draw(self.screen, self.game_ctrl.tf)
            pg.display.update()

    def cleanup(self):
        pass

app = App()
app.start()
