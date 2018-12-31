from Tkinter import *
import ttk
from settings import EditField
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
		l = int(self.lVar.get())
		r = int(self.rVar.get())
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

if __name__ == '__main__':
	root = Tk()
	g = Graphic(root, 10, 100, "Test")
	g.grid()
	root.mainloop()


