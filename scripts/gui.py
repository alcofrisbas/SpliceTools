from Tkinter import *
import ttk, tkFileDialog

import splice

class GUI:
	def __init__(self, master):
		self.sounds = splice.Splice()
		self.master = master

		self.Mode = StringVar()
		self.Mode.set("I")

		self.mainFrame = ttk.Frame(self.master)
		self.mainFrame.grid()
		
		self.files(self.mainFrame, 0 ,0)

		self.settings(self.mainFrame, 0, 1)


	def settings(self, parent, r, c):
		self.settingsFrame = ttk.LabelFrame(parent, text = "Settings")
		self.settingsFrame.grid(row = r, column = c)

		



	def files(self, parent, r, c):
		
		self.filesFrame = ttk.LabelFrame(parent, text = "Files")
		self.filesFrame.grid(row = r, column = c)

		self.attackButton = ttk.Button(self.filesFrame, text = "Attack File", command = self.getAttack)
		self.attackButton.grid(row = 0, column = 0)

		self.toneButton = ttk.Button(self.filesFrame, text = "Tone File", command = self.getTone)
		self.toneButton.grid(row = 1, column = 0)
		
		self.rBI = ttk.Radiobutton(self.filesFrame, text = "I", variable=self.Mode, value="I")
		self.rBI.grid(row = 0, column = 1)
		

		self.rBB = ttk.Radiobutton(self.filesFrame, text = "B", variable=self.Mode, value="B")
		self.rBB.grid(row = 1, column = 1)

		self.trimLabel = ttk.Label(self.filesFrame, text = "Trim amount")
		self.trimLabel.grid(row = 2, column = 0)

		self.trimEntry = ttk.Entry(self.filesFrame, width = 6)
		self.trimEntry.grid(row = 2, column = 1)
		self.trimEntry.insert(0, "0")

		self.playButton = ttk.Button(self.filesFrame, text = "Play Back And Save", command = self.playTone)
		self.playButton.grid(row = 3, column = 0, columnspan = 2, sticky = E+W)

	def getTone(self):
		self.sounds.tone(tkFileDialog.askopenfilename())

	def getAttack(self):
		print self.Mode.get()
		if self.Mode.get() == "I":
			self.sounds.attack(tkFileDialog.askopenfilename())

	def playTone(self):
		trimAmount = int(self.trimEntry.get())
		print trimAmount
		self.sounds.trimTone(trimAmount)
		self.sounds.playBack("l")


def main():
	root = Tk()
	gui = GUI(root)
	root.mainloop()

if __name__ == '__main__':
	main()