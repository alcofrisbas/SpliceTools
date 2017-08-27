from Tkinter import *
import ttk

class GUI:
	def __init__(self, master):
		self.master = master
		
		self.selfVar = BooleanVar()
		self.selfVar.set(True)

		self.mainFrame = ttk.Frame(self.master)
		self.mainFrame.grid(row = 0, column = 0)

		self.entryFrame = ttk.Frame(self.mainFrame)
		self.entryFrame.grid(row = 0, column = 0)

		self.entries(self.entryFrame)

		self.goButton = ttk.Button(self.mainFrame, text = "make widget", command = self.makeWidget)
		self.goButton.grid(row = 1, column = 0)

		self.box = Text(self.mainFrame, width = 80, height = 15)
		self.box.grid(row = 0, column = 2, rowspan = 2)

	def entries(self, parent):
		self.nameLabel = ttk.Label(parent, text = "Variable Name")
		self.nameLabel.grid(row = 0, column = 0)

		self.nameFrame = ttk.Frame(parent)
		self.nameFrame.grid(row = 0, column = 1, sticky = W)

		self.nameEntry = ttk.Entry(self.nameFrame, width = 10)
		self.nameEntry.grid(row = 0, column = 0)

		self.selfCheck = ttk.Checkbutton(self.nameFrame, text = "self", variable = self.selfVar)
		self.selfCheck.grid(row = 0, column = 1)

		self.typeLabel = ttk.Label(parent, text = "Type")
		self.typeLabel.grid(row = 1, column = 0)

		self.typeEntry = ttk.Entry(parent)
		self.typeEntry.grid(row = 1, column = 1)

		self.parentLabel = ttk.Label(parent, text = "parent")
		self.parentLabel.grid(row = 2, column = 0)

		self.parentEntry = ttk.Entry(parent)
		self.parentEntry.grid(row = 2, column = 1)

		self.textLabel = ttk.Label(parent, text = "text")
		self.textLabel.grid(row = 3, column = 0)

		self.textEntry = ttk.Entry(parent)
		self.textEntry.grid(row = 3, column = 1)

		self.otherLabel = ttk.Label(parent, text = "other arguments")
		self.otherLabel.grid(row = 4, column = 0)

		self.otherEntry = ttk.Entry(parent)
		self.otherEntry.grid(row = 4, column = 1)

		self.rowLabel = ttk.Label(parent, text = "row")
		self.rowLabel.grid(row = 5, column = 0)

		self.rowEntry = ttk.Entry(parent)
		self.rowEntry.grid(row = 5, column = 1)

		self.columnLabel = ttk.Label(parent, text = "column")
		self.columnLabel.grid(row = 6, column = 0)

		self.columnEntry = ttk.Entry(parent)
		self.columnEntry.grid(row = 6, column = 1)

		self.gridOptsLabel = ttk.Label(parent, text = "placement options")
		self.gridOptsLabel.grid(row = 7, column = 0)

		self.gridOptsEntry = ttk.Entry(parent)
		self.gridOptsEntry.grid(row = 7, column = 1)

		self.indentLabel = ttk.Label(parent, text = "indent Level")
		self.indentLabel.grid(row = 8, column = 0)

		self.indentEntry = ttk.Entry(parent)
		self.indentEntry.grid(row = 8, column = 1)
		self.indentEntry.insert(0,"2")

	def makeWidget(self):
		str = ""
		str += "\t"*int(self.indentEntry.get())
		name = ""
		parent = ""
		if self.selfVar.get():
			name += "self."
			parent += "self."
		parent += self.parentEntry.get()
		name += self.nameEntry.get()

		str += name+" = ttk."+self.typeEntry.get()+"("+parent
		if self.textEntry.get() != "":
			str += ', text = "'+self.textEntry.get()+'"' 
		if self.otherEntry.get() != "":
			str += ", "+self.otherEntry.get()

		str += ")\n"
		str += "\t"*int(self.indentEntry.get())
		str += name+".grid(row = "+self.rowEntry.get()+", column = "+self.columnEntry.get()
		if self.gridOptsEntry.get() != "":
			str += ", "+self.gridOptsEntry.get() 
		str += ")\n"
		self.box.insert(END, str)
		print str

def makeWidget():
	name = raw_input("variable name: ")
	type = raw_input("widget type: ")
	parent = raw_input("parent: ")
	text = raw_input("text: ")
	other = raw_input("other arguments: ")
	row = raw_input("row: ")
	column = raw_input("column: ")
	gridOpts = raw_input("other placement options: ")


	str = name+" = ttk."+type+"("+parent
	if text != "":
		str += ', text = "'+text+'"' 
	if other != "":
		str += ", "+other

	str += ")\n"
	str += name+".grid(row = "+row+", column = "+column
	if gridOpts != "":
		str += ", "+gridOpts 
	str += ")"
	
	print str

def main():
	root = Tk()
	gui = GUI(root)
	root.mainloop()
	#while True:
	#	makeWidget()

if __name__ == '__main__':
	main()
