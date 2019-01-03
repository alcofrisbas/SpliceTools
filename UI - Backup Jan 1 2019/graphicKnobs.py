from Tkinter import *
import ttk
from settings import EditField
import math

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

class Graphic(ttk.LabelFrame):
	def __init__(self, master, length,size,name,l=100, r=100, maxRange=400):
		ttk.LabelFrame.__init__(self, master,text=name)
		self.lInit = l
		self.rInit = r
		self.maxRange = maxRange
		self.master = master
		self.size = size
		self.length=length
		self.mainFrame = ttk.Frame(self)
		self.mainFrame.grid()

		self.lVar = StringVar()
		self.rVar = StringVar()
		self.scVar = StringVar()
		self.scVar.set("1")
		
		self.label = ttk.Label(self.mainFrame)
		self.c = Canvas(self.mainFrame, width=self.size, height=self.size)
		self.c.grid(column=1)

		#self.line = self.c.create_line(0,self.size,self.size,self.size)
		self.poly = self.c.create_polygon(0,self.size,
										  self.size, self.size, 
										  self.size, self.size/2,
										  0, self.size/2)


		self.buttonFrame = ttk.Frame(self.mainFrame)
		self.buttonFrame.grid(row = 0, column = 1)

		self.l = ttk.Scale(self.mainFrame, from_=0, to=self.size,
						   orient=VERTICAL, value=0)
		self.l.grid(row=0,column=0)
		self.l.set(self.size/2)

		self.r = ttk.Scale(self.mainFrame, from_=0, to=self.size, 
						   orient=VERTICAL, value=0)
		self.r.grid(row=0,column=2)
		self.r.set(self.size/2)
		
		self.l.config(command=lambda x: self.drawLine("l"))
		self.r.config(command=lambda x: self.drawLine("r"))

		self.lLabel = ttk.Label(self.mainFrame, textvariable=self.lVar)
		self.lLabel.grid(row=1,column=0)

		self.rLabel = ttk.Label(self.mainFrame, textvariable=self.rVar)
		self.rLabel.grid(row=1,column=2)

		self.scaleSlide = ttk.Scale(self.mainFrame, from_=0, to=self.maxRange,command=self.setScale)
		self.scaleSlide.grid(row=2,column=1,sticky=E+W)

		self.scaleLabel = ttk.Label(self.mainFrame, textvariable=self.scVar)
		self.scaleLabel.grid(row=2,column=2)

		#self.drawLine(1)



		#self.b = ttk.Button(self.buttonFrame, text="test", command=self.drawLine)
		#self.b.grid(row=2)

	def drawLine(self, which):
		#print self.scVar.get()
		if which == "r":
			#print int((self.size-int(self.r.get()))*int(self.scVar.get())/float(self.size))
			self.rVar.set(str(int((self.size-int(self.r.get()))*int(self.scVar.get())/float(self.size))))
		elif which == "l":
			self.lVar.set(str(int((self.size-int(self.l.get()))*int(self.scVar.get())/float(self.size))))
		#print a
		#self.c.delete(self.line)
		self.c.delete(self.poly)
		self.yL = int(self.l.get()) if self.l.get() else 0
		self.yR = int(self.r.get()) if self.r.get() else 0

		#self.line = self.c.create_line(0, self.yL, self.size, self.yR)
		self.poly = self.c.create_polygon(0,self.size,
										  self.size, self.size, 
										  self.size, self.yR,
										  0, self.yL,fill="green")

	def setScale(self,p):
		self.scVar.set(str(10*int(self.scaleSlide.get())))
		self.rVar.set(str(int((self.size-int(self.r.get()))*int(self.scVar.get())/float(self.size))))
		self.lVar.set(str(int((self.size-int(self.l.get()))*int(self.scVar.get())/float(self.size))))

	def get(self):
		pads = []
		l = int(self.lVar.get()) if self.lVar.get() else 0
		r = int(self.rVar.get()) if self.rVar.get() else 0
		slope = (float(r)-l)/(float(self.size)-0)
		for p in range(self.length):
			translatedPoint = p*self.size/self.length
			pad = slope*(translatedPoint-0)+l
			pads.append(pad)
		return pads

	def set(self, l, r):
		self.l.set(l)
		self.r.set(r)
		self.yL = l
		self.yR = r


class ClickableGraphicKnob(ttk.LabelFrame):
	def __init__(self, master, length,size,name,l=100, r=100, maxRange=400):
		ttk.LabelFrame.__init__(self, master,text=name)
		self.maxRange = maxRange
		self.master = master
		self.size = size
		self.length=length
		# list of tuples; (x, y)
		self.pts = []


		self.adding = False
		self.removing = False


		self.topBox = ttk.Frame(self)
		self.topBox.grid(row = 0, column = 0)

		self.ctx = Canvas(self.topBox, width=self.size, height=self.size)
		self.ctx.grid(row=0, column=0)

		self.ctx.bind("<Button 1>", self.canvas_onClick1)

		self.buttonVBox = ttk.Frame(self.topBox)
		self.buttonVBox.grid(row = 0, column = 1,sticky=N+W)

		self.edit = ttk.Button(self.buttonVBox, text = "edit", width=0,
			command = self.set_focus)
		self.edit.grid(row = 0 , column = 0,sticky=W )

		self.plus = ttk.Button(self.buttonVBox, text = "+", width=0,
			command = self.add_pt)
		self.plus.grid(row = 1 , column = 0,sticky=W )

		self.minus = ttk.Button(self.buttonVBox, text = "-", width=0,
			command = self.rem_pt)
		self.minus.grid(row = 2 , column = 0,sticky=W )



	def set_focus(self):
		self.ctx.focus_set()

	def canvas_onClick1(self, event):
		#print(event.x, event.y)
		closest = self.find_closest_point((event.x, event.y))
		if self.pts:
			item = self.ctx.find_withtag(str(closest))[0]
			self.highlight_pt(item)
		
		elif self.adding:
			self.pts.append((event.x, event.y))
			self.draw_pts()
			self.adding = False
		
		elif self.removing:
			closest = self.find_closest_point((event.x, event.y))
			self.pts.remove(closest)
			self.draw_pts()
			self.removing = False


	def find_closest_point(self, pt):
		d = 2*self.size
		p = (0,0)
		for pt1 in self.pts:
			dist = math.sqrt((pt[0]-pt1[0])**2+(pt[1]-pt1[1])**2)
			if dist < d:
				p = pt1
		return p
	
	def add_pt(self):
		self.adding = True
		print("adding")

	def rem_pt(self):
		self.removing = True
		print("removing")
	
	def draw_pts(self):
		self.ctx.delete("pt")
		print(self.pts)
		for pt in self.pts:
			self.ctx.create_circle(pt[0], pt[1], 3, tags=("pt", str(pt)))

	def highlight_pt(self, ):
		self.ctx.itemconfig(i, outline='red')

if __name__ == '__main__':
	root = Tk()
	g = ClickableGraphicKnob(root, 10, 100, "Test")
	g.grid()
	root.mainloop()


