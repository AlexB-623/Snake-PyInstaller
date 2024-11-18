from os import path
import sys
import tkinter as tk
from random import randint
from PIL import Image, ImageTk

MOVE_INCREMENT = 20
moves_per_second = 5
GAME_SPEED = 1000 // moves_per_second

class Snek(tk.Canvas):
    def __init__(self):
        super().__init__(width=600, height=620, background="black", highlightthickness=0)
        self.snek_positions = [(100, 100), (80, 100), (60, 100)]
        self.food_position = self.set_new_food_position()
        self.score = 0
        self.direction = "Right"
        self.bind_all("<Key>", self.on_key_press)

        self.load_assets()
        self.create_objects()

        self.after(GAME_SPEED, self.perform_actions)


    def load_assets(self):
        try:
            bundle_dir = getattr(sys, "_MEIPASS", path.abspath(path.dirname(__file__)))
            path_to_snek = path.join(bundle_dir, "assets", "snek.png")
            #self.snek_body_image = Image.open("./assets/snek.png")
            self.snek_body_image = Image.open(path_to_snek)
            self.snek_body = ImageTk.PhotoImage(self.snek_body_image)
            path_to_food = path.join(bundle_dir, "assets", "food.png")
            #self.food_image = Image.open("./assets/food.png")
            self.food_image = Image.open(path_to_food)
            self.food = ImageTk.PhotoImage(self.food_image)
        except IOError as error:
            print(error)
            input("\n\n\nFinished. Press enter to exit...")
            root.destroy()

    def create_objects(self):
        self.create_text(
            45, 12, text=f"Score: {self.score}", tag="score", fill="#fff", font=("TkDefaultFont", 14)
        )
        for x_position, y_position in self.snek_positions:
            self.create_image(x_position, y_position, image=self.snek_body, tag="snek")

        self.create_image(*self.food_position, image=self.food, tag="food")
        self.create_rectangle(7, 27, 593, 613, outline="#525d69")

    def move_snek(self):
        head_x_position, head_y_position = self.snek_positions[0]

        if self.direction == "Left":
            new_head_position = (head_x_position - MOVE_INCREMENT, head_y_position)
        elif self.direction == "Right":
            new_head_position = (head_x_position + MOVE_INCREMENT, head_y_position)
        elif self.direction == "Down":
            new_head_position = (head_x_position, head_y_position + MOVE_INCREMENT)
        elif self.direction == "Up":
            new_head_position = (head_x_position, head_y_position - MOVE_INCREMENT)

        self.snek_positions = [new_head_position] + self.snek_positions[:-1]

        for segment, position in zip(self.find_withtag("snek"), self.snek_positions):
            self.coords(segment, position)

    def perform_actions(self):
        if self.check_collisions():
            self.end_game()
            return

        self.check_food_collision()
        self.move_snek()
        self.after(GAME_SPEED, self.perform_actions)

    def check_collisions(self):
        head_x_position, head_y_position = self.snek_positions[0]

        return (
            head_x_position in (0, 600)
            or head_y_position in (20, 620)
            or (head_x_position, head_y_position) in self.snek_positions[1:]
        )

    def on_key_press(self, e):
        new_direction = e.keysym
        all_directions = ("Up", "Down", "Left", "Right")
        opposites = ({"Up", "Down"}, {"Left", "Right"})

        if (
            new_direction in all_directions
            and {new_direction, self.direction} not in opposites
        ):
            self.direction = new_direction

    def check_food_collision(self):
        if self.snek_positions[0] == self.food_position:
            self.score += 1
            self.snek_positions.append(self.snek_positions[-1])

            if self.score % 5 == 0:
                global moves_per_second
                moves_per_second += 1

            self.create_image(
                *self.snek_positions[-1], image=self.snek_body,tag="snek"
            )

            self.food_position = self.set_new_food_position()
            self.coords(self.find_withtag("food"), self.food_position)

            score = self.find_withtag("score")
            self.itemconfigure(score, text=f"Score: {self.score}", tag="score")

    def set_new_food_position(self):
        while True:
            x_position = randint(1, 29) * MOVE_INCREMENT
            y_position = randint(3, 30) * MOVE_INCREMENT
            food_position = (x_position, y_position)

            if food_position not in self.snek_positions:
                return food_position

    def end_game(self):
        self.delete(tk.ALL)
        self.create_text(
            self.winfo_width() / 2,
            self.winfo_height() / 2,
            text=f"Game Over! Your Score: {self.score}",
            fill="#fff",
            font=("TkDefaultFont", 24)
        )


try:
    root = tk.Tk()
    root.title("Snek")
    root.resizable(False, False)

    board = Snek()
    board.pack()


    root.mainloop()
except:
    import traceback
    traceback.print_exc()
    input("Press enter to exit...")