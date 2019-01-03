# gui
from Tkinter import *
import ttk, tkFileDialog
# builtin module for working with files
import os
# custom ui and organization modules
from settings import MainSettings,IndividualSettings,ConfigSettings
from tray import Tray
from graphicKnobs import Graphic

from services import *
# working with json formatting for settings
import json
# this imports the splicing methods 'setup' and 'splice'
from scripts.batchSplice import *


class MainView:
	def __init__(self, master):
		self.master = master
		self.ID = "main"
		#============ Menu ======================

		self.menubar = Menu(master)
		self.filemenu = Menu(self.menubar, tearoff=0)
		self.filemenu.add_command(label="Save")
		self.filemenu.add_command(label="Open")
		self.filemenu.add_command(label="New")
		self.filemenu.add_separator()
		self.filemenu.add_command(label="Audio Settings",command=self.openConfigSettings)
		self.menubar.add_cascade(label="File",menu=self.filemenu)

		self.master.config(menu=self.menubar)

		# True/False is Editable or Not.
		self.mainSettingsList = [["consFolder",False],
							 ["vowelFolder",False],
							 ["outFolder",False],
							 ["fred",True],
							 ["initial frequency",True],
							 ["xFade Length",True],
							 ["Vowel Pad",True],
							 ["Splice Point",True],
							 ["Tuning Bounds",True],
							 ["Pad First",True],
							 ["Pad Last",True],
							 ["Crossfade First",True],
							 ["Crossfade Last",True]]


		self.indivSettingsList = [["consFile",True],
							 ["vowelFile",True],
							 ["initial frequency",True],
							 ["xFade Length",True],
							 ["InitPad",True],
							 ["EndPad",True],
							 ["Vowel Pad",True],
							 ["Splice Point",True],
							 ["Tuning Bounds",True],
							 ["outFile",True]]
		self.readSettings()
		#============ vars ==================

		#self.toneFolderPath = StringVar()
		#self.attackFolderPath = StringVar()

		#============ frames ================

		self.mainFrame = ttk.Frame(self.master)
		self.mainFrame.grid()

		self.leftWrapper = ttk.Frame(self.mainFrame)
		self.leftWrapper.grid(row=0,column=0,sticky=N)

		self.inFrame = ttk.LabelFrame(self.leftWrapper, text="File Setup")
		self.inFrame.grid(row=0, column=0,sticky=N)

		self.settingsFrame = ttk.LabelFrame(self.mainFrame, text="Main Settings")
		self.settingsFrame.grid(row=0, column=1)

		self.trayFrame = ttk.LabelFrame(self.leftWrapper, text="Tray")
		self.trayFrame.grid(row=2,column=0,sticky=N+W)

		self.goFrame = ttk.Frame(self.leftWrapper)
		self.goFrame.grid(row=1, column=0, sticky=E+W)

		self.graphicsFrame = ttk.LabelFrame(self.mainFrame, text="Editing")
		self.graphicsFrame.grid(row = 0, column=2,sticky=N)



		#============ inFrame ==========================

		self.chooseAttackButton = ttk.Button(self.inFrame, text="Choose Attack Folder",
											 command=lambda: self.chooseFolder("consFolder"))
		self.chooseAttackButton.grid(row=0,column=0)

		self.chooseToneButton = ttk.Button(self.inFrame, text="Choose Tone Folder",
										   command=lambda: self.chooseFolder("vowelFolder"))
		self.chooseToneButton.grid(row=0,column=1)

		self.chooseFred = ttk.Button(self.inFrame, text="Choose fred",
											 command=lambda: self.chooseFolder("fred"))
		self.chooseFred.grid(row=0,column=2)

		self.chooseDestinationButton = ttk.Button(self.inFrame, text="Choose Destination Folder",
												  command=lambda: self.chooseFolder("outFolder"))
		self.chooseDestinationButton.grid(row=1,column=0,columnspan=2,sticky=W)

		#============ goFrame =============================

		self.goButton = ttk.Button(self.goFrame, text="Process Batch",
								   command=self.spliceByBatch)
		self.goButton.grid(row=0, column=0)

		self.statusLabel = ttk.Label(self.goFrame,text="IDLE")
		self.statusLabel.grid(row=0, column=1)

		#============ settingsFrame =======================

		self.mainSettings = MainSettings(self.settingsFrame,settings=self.mainSettingsList)
		self.mainSettings.grid(row=0,column=0,sticky=E)

		print "  "
		print "============ SETTINGS IMPORTED FROM json ============="
		self.mainSettings.setValues(self.settings)
		print "============ END OF json IMPORT ============="

		self.applySettingsButton = ttk.Button(self.settingsFrame, text="Apply",
											  command=self.applyMainSettings)
		self.applySettingsButton.grid(row=1)

		#============ trayFrame ============================

		self.tray = Tray(self.trayFrame, settings=self.indivSettingsList)#,initialSettings=self.settings)
		self.tray.grid()
		#for i in range(11):
		#	self.tray.addItem(json.loads(open('settings.json').read()))

		# self.placeHolder = ttk.Button(self.trayFrame, text="Placeholder",
		# 							  command=self.placeholderButton)
		# self.placeHolder.grid()

		#============ graphicsFrame ============================
		self.graphs = {}
		
		self.padGraph = Graphic(self.graphicsFrame,self.numFiles,100,"Padding")
		self.padGraph.grid(row=0, column=0)
		self.graphs["pads"] = self.padGraph

		self.padGraph = Graphic(self.graphicsFrame,self.numFiles,100,"Cross Fade Length",maxRange=800)
		self.padGraph.grid(row=0, column=1)
		self.graphs["cfls"] = self.padGraph
		

	def graphGet(self,category):
		self.setupOut[category] = self.graphs[category].get()
		print category, self.setupOut[category]
		#print self.setupOut

	def readSettings(self):
		if not os.path.exists('settings.json'):
			with open('default_settings.json') as r:
				with open('settings.json','w') as w: 
					w.write(r.read())
		self.settings = json.loads(open('settings.json').read())
		self.setupOut = setup(self.settings)
		self.numFiles = len(self.setupOut["outFiles"])

	#def readIndivSettings(self):
	#	pass

	def chooseFolder(self, var):
		f = tkFileDialog.askdirectory(initialdir = ".")
		#print(os.getcwd())
		#print(f)
		the_dir = f.split(os.getcwd())[-1][1:]
		self.settings[var] = the_dir
		self.mainSettings.setValues(self.settings)
		#print var.get()

	def loadProject(self):
		directory = tkFileDialog.askdirectory()
		if checkFileSystem(directory):
			os.chdir(directory)
			self.readSettings()



	def applyMainSettings(self):
		self.settings = self.mainSettings.get()
		print "================ APPLY MAIN SETTINGS ====================="
		print self.settings

		with open('settings.json','w') as w:
			w.write(json.dumps(self.settings))

		self.readSettings()

	def spliceByBatch(self):
		#names = batch(self.settings)
		#setupOut = setup(self.settings)
		#for n in names:
		#self.tray.clear()
		#self.tray.update_idletasks()
		print "  "
		print "===================================================================="
		print "========================= BEGIN spiceByBatch ======================="
		print "===================================================================="
		self.statusLabel.config(text="WORKING")
		self.master.update_idletasks()
		self.applyMainSettings()
		print "============ graphicKnobs ============="
		for g in self.graphs:
			self.graphGet(g)
		print "============ Frequencies ============="
		print "setupOut[freqs] = ", self.setupOut["freqs"]
		print "Length ::: len(self.setupOut[freqs]) = ", len(self.setupOut["freqs"])
		print "  "
		print "============================================"
		print "============= NOW BEGIN LOOP ==============="
		for i in range(len(self.setupOut["freqs"])):
			splice(i, self.setupOut, self.settings)
			print "  "
			print "NOW WE'RE IN self.tray.addItem TERRITORY"
			self.tray.addItem(json.loads(open('settings.json').read()),buttonText=self.setupOut["outFiles"][i].split("/")[-1],consFile=self.setupOut["consFiles"][i])
			self.tray.update_idletasks()
			print "  "
			print "  "
		print "======================================================================="
		print "============================ PROCESS DONE ============================="
		print "======================================================================="
		print "  "
		print "  "
		print "  "
		self.statusLabel.config(text="IDLE")

	def placeholderButton(self):
		t = Toplevel(self.master)
		i = IndividualSettings(t)
		i.grid()

	def openConfigSettings(self):
		t = Toplevel(self.master)
		s = ConfigSettings(t)
		s.grid()

if __name__ == '__main__':
	root = Tk()
	m = MainView(root)
	root.mainloop()
