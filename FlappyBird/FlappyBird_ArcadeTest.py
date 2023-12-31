from curses import window
import arcade
import arcade.gui
import random

ScreenWidth = 600
ScreenHeight = 500
ScreenTitle = "Flappy Bird"

PlayerScaling = 0.12
TubeScaling = 0.5
GroundScaling = 0.5

BirdMovementSpeed = 3
BirdJumpHeight = 15

###################################################################################################################################################################################################

class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        
    def on_show_view(self):
        arcade.set_background_color(arcade.color.GRAY)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.box = arcade.gui.UIBoxLayout(space_between=20)

        play_button = arcade.gui.UIFlatButton(ScreenWidth/2-100, 100, text="Resume Game", width=200)
        play_button.on_click = self.on_click_play_button
        self.box.add(play_button)

        restart_button = arcade.gui.UIFlatButton(text="Restart", width=200)
        restart_button.on_click = self.on_click_restart_button
        self.box.add(restart_button)

        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x",anchor_y="center_y",child=self.box))

    def on_draw(self):
        self.clear()
        self.game_view.scene.draw()
        self.manager.draw()
        arcade.draw_text("Paused", ScreenWidth / 2, ScreenHeight - 100, arcade.color.ALABAMA_CRIMSON, font_size=40, anchor_x="center")
        
    def on_click_play_button(self, event):
        self.window.show_view(self.game_view)

    def on_click_restart_button(self, event):
        restart = Flappy()
        self.window.show_view(restart)

###################################################################################################################################################################################################

class Flappy(arcade.View):

    def __init__(self):
        super().__init__()
        self.scene = None
        self.bird_sprite = None
        self.physics_engine = None
        self.score = 0
        self.speed = -2
        self.GRAVITY = 0
        self.start = False
        arcade.set_background_color(arcade.color.FRENCH_SKY_BLUE)
        self.setup()
        
    def on_show_view(self):
        arcade.set_background_color(arcade.color.FRENCH_SKY_BLUE)

    def setup(self):
        self.scene = arcade.Scene()

        self.scene.add_sprite_list("Bird")
        self.scene.add_sprite_list("tube")
        self.scene.add_sprite_list("ground", use_spatial_hash=True)

        self.bird_sprite = arcade.Sprite("download-removebg-preview.png", PlayerScaling)
        self.bird_sprite.center_x = 150
        self.bird_sprite.center_y = ScreenHeight / 2
        self.scene.add_sprite("Bird", self.bird_sprite)

        self.tube1top = arcade.Sprite("210-2104021_mario-pipe-pixel-mario-tube-png-removebg-preview copy.png", TubeScaling)
        self.tube1top.center_x = 500
        self.tube1top.center_y = ScreenHeight
        self.scene.add_sprite("tube", self.tube1top)
        self.physics_engineTT1 = arcade.PhysicsEnginePlatformer(self.tube1top, gravity_constant = 0)

        self.tube2top = arcade.Sprite("210-2104021_mario-pipe-pixel-mario-tube-png-removebg-preview copy.png", TubeScaling)
        self.tube2top.center_x = 900
        self.tube2top.center_y = random.randint(ScreenHeight - 50, ScreenHeight)
        self.scene.add_sprite("tube", self.tube2top)
        self.physics_engineTT2 = arcade.PhysicsEnginePlatformer(self.tube2top, gravity_constant = 0)

        self.tube1bot = arcade.Sprite("210-2104021_mario-pipe-pixel-mario-tube-png-removebg-preview.png", TubeScaling)
        self.tube1bot.center_x = 500
        self.tube1bot.center_y = 0
        self.scene.add_sprite("tube", self.tube1bot)
        self.physics_engineTB1 = arcade.PhysicsEnginePlatformer(self.tube1bot, gravity_constant = 0)

        self.tube2bot = arcade.Sprite("210-2104021_mario-pipe-pixel-mario-tube-png-removebg-preview.png", TubeScaling)
        self.tube2bot.center_x = 900
        self.tube2bot.center_y = random.randint(0,70)
        self.scene.add_sprite("tube", self.tube2bot)
        self.physics_engineTB2 = arcade.PhysicsEnginePlatformer(self.tube2bot, gravity_constant = 0)
        
        for x in range(ScreenWidth):
            ground = arcade.Sprite("74218fbf063b580-removebg-preview.png", GroundScaling)
            ground.center_y = 0
            ground.center_x = x
            self.scene.add_sprite("ground", ground)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.bird_sprite, gravity_constant = self.GRAVITY, walls=self.scene["ground"])
    
    def on_draw(self):
        self.clear()
        self.scene.draw()
        arcade.draw_text(self.score, ScreenWidth / 2, ScreenHeight - 100, arcade.color.BLACK, font_size=40, font_name="Kenney Mini Square", anchor_x="center")        

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                 self.GRAVITY = 0.75
                 if not self.start:
                    self.setup()
                 self.start = True
                 self.bird_sprite.change_y = BirdJumpHeight

    def on_key_release(self, key, modifiers):
        if key == arcade.key.SPACE:
             self.bird_sprite.change_y = 0
        elif key == arcade.key.ESCAPE:
            Pause = PauseView(self)
            self.window.show_view(Pause)
    
    def collides_with_tube(self):
        self.start = False
        self.physics_engine.disable_multi_jump()
        self.tube1top.change_x = 0
        self.tube1bot.change_x = 0
        self.tube2top.change_x = 0
        self.tube2bot.change_x = 0
        self.bird_sprite.change_x = 0
        self.bird_sprite.change_y = 0
        self.bird_sprite.kill()
        GameOver = GameOverView()
        self.window.show_view(GameOver)

    def on_update(self, delta_time):
        print(self.score)
        if self.start:
            if self.tube1top.center_x == -2:
                self.tube1top.center_x = self.tube2top.center_x + 400
                self.tube1top.center_y = random.randint(ScreenHeight - 100, ScreenHeight)
                self.tube1bot.center_x = self.tube2bot.center_x + 400
                self.tube1bot.center_y = random.randint(0,70)
            else:
                self.tube1top.change_x = self.speed
                self.tube1bot.change_x = self.speed

            if self.tube2top.center_x <= -2:
                self.tube2top.center_x = self.tube1top.center_x + 400
                self.tube2top.center_y = random.randint(ScreenHeight - 75, ScreenHeight)
                self.tube2bot.center_x = self.tube1bot.center_x + 400
                self.tube2bot.center_y = random.randint(0,70)
            else:
                self.tube2top.change_x = self.speed
                self.tube2bot.change_x = self.speed
        
        if self.bird_sprite.center_x == self.tube1bot.center_x or self.bird_sprite.center_x == self.tube2top.center_x:
            self.score += 1
            
        if self.bird_sprite.collides_with_list(self.scene.get_sprite_list("tube")):
            self.collides_with_tube()

        self.physics_engine.enable_multi_jump(float('inf'))
        self.physics_engine.update()
        self.physics_engineTT1.update()
        self.physics_engineTT2.update()
        self.physics_engineTB1.update()
        self.physics_engineTB2.update()

###################################################################################################################################################################################################

class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
    
    def on_show_view(self):
        arcade.set_background_color(arcade.color.GRAY_ASPARAGUS)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.box = arcade.gui.UIBoxLayout(space_between=20)

        restart_button = arcade.gui.UIFlatButton(text="Restart", width=200)
        restart_button.on_click = self.on_click_restart_button
        self.box.add(restart_button)

        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x",anchor_y="center_y",child=self.box))

    def on_draw(self):
        self.clear()
        self.manager.draw()
        arcade.draw_text("Game Over", ScreenWidth / 2, ScreenHeight - 100, arcade.color.ALABAMA_CRIMSON, font_size=40, anchor_x="center")

    def on_click_restart_button(self, event):
        start = Flappy()
        self.window.show_view(start)

###################################################################################################################################################################################################

def main():
     window = arcade.Window(ScreenWidth, ScreenHeight, ScreenTitle)
     start_view = Flappy()
     window.show_view(start_view)
     start_view.on_show_view()
     arcade.run()

if __name__ == "__main__":
    main()