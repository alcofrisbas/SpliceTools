import Tkinter as tk

class Example(tk.Frame):
    '''Illustrate how to drag items on a Tkinter canvas'''

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # create a canvas
        self.canvas = tk.Canvas(width=400, height=400)
        self.canvas.pack(fill="both", expand=True)

        # this data is used to keep track of an 
        # item being dragged
        self._drag_data = {"x": 0, "y": 0, "item": None}

        # create a couple of movable objects
        self._create_token((100, 100), "red")
        self._create_token((200, 100), "red")

        self.points = [200,100,100,100]
        self.line = self.canvas.create_line(self.points)
        #self.line = self.canvas.create_line([200,100,100,300])

        # add bindings for clicking, dragging and releasing over
        # any object with the "token" tag
        self.canvas.tag_bind("token", "<ButtonPress-1>", self.on_token_press)
        self.canvas.tag_bind("token", "<ButtonRelease-1>", self.on_token_release)
        self.canvas.tag_bind("token", "<B1-Motion>", self.on_token_motion)

    def redraw(self, coords):
        self.canvas.delete(self.poly)
        self.poly = self.canvas.create_polygon(coords)

    def _create_token(self, coord, color):
        '''Create a token at the given coordinate in the given color'''
        (x,y) = coord
        self.canvas.create_oval(x-5, y-5, x+5, y+5, 
                                outline=color, fill=color, tags="token")

    def on_token_press(self, event):
        '''Begining drag of an object'''
        # record the item and its location
        self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

        #self.

    def on_token_release(self, event):
        '''End drag of an object'''
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0
        #print self.canvas.gettags("token")


    def on_token_motion(self, event):
        '''Handle dragging of an object'''
        # compute how much the mouse has moved
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        # move the object the appropriate amount
        self.canvas.move(self._drag_data["item"], delta_x, delta_y)
        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()