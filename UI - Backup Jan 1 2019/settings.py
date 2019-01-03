from Tkinter import *
import ttk

import matplotlib
matplotlib.use('TkAgg')
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from scripts.soundOps import soundToArray

# The main Settings pane that default applies to 
class MainSettings(ttk.Frame):
	def __init__(self, master, *args, **kwargs):
		self.ID = "MainSettings"
		ttk.Frame.__init__(self, master)#, *args, **kwargs)
		self.master = master
		
		self.mainFrame = ttk.Frame(self.master)
		self.mainFrame.grid()
		self.d = {}
		self.settingsList=kwargs["settings"]

		for i, e in enumerate(self.settingsList):
			self.d[e[0]] = EditField(self.mainFrame, text=e[0], editable=e[1], entryWidth="40")
			self.d[e[0]].grid(row=i%5,column=i/5, sticky=W)
		#self.x = EditField(self.mainFrame,text="this is a test")
		#self.x.grid(row=1)
	def setValues(self, settingsDict):
		for k in settingsDict:
			if self.d.get(k,False):
				self.d[k].setEntry(settingsDict[k])
	def get(self):
		s = {}
		for e in self.d:
			s[e] = self.d[e].get()
		return s





class IndividualSettings(ttk.Frame):
	def __init__(self, master, *args, **kwargs):
		self.ID = "IndividualSettings"
		ttk.Frame.__init__(self, master)#, *args, **kwargs)
		self.master = master
		
		self.mainFrame = ttk.Frame(self.master)
		self.mainFrame.grid()

		f = Figure(figsize=(6, 2), dpi=100)
		a = f.add_subplot(111)
		t = arange(0.0, 3.0, 0.01)
		s = sin(2*pi*t)
		#b = f.add_subplot(212)
		#s2 = sin(4*pi*t)
		
		#consX, consFS = soundToArray(kwargs["consFile"])
		#a.plot(np.arange(consX.size)/float(consFS),consX)
		#a.axis([0, consX.size/float(consFS), min(consX), max(consX)])

		#a.plot(t, s)
		a.axvline(linewidth=4, color='r')
		#b.plot(t, s2)
		#b.axvline(linewidth=4, color='r')

		self.canvas = FigureCanvasTkAgg(f, master=self.mainFrame)
		self.canvas.show()
		self.canvas.get_tk_widget().grid(row=0,column=0,padx=5,pady=0,rowspan=1)

		self.settingsFrame = ttk.Frame(self.mainFrame)
		self.settingsFrame.grid(row=0, column=1,pady=2,padx=2)

		self.settingsPanel = MainSettings(self.settingsFrame,settings=kwargs["settings"])
		self.settingsPanel.grid(row=0,column=0)

		self.buttonFrame = ttk.Frame(self.settingsFrame)
		self.buttonFrame.grid(row=1, column=0)#,sticky=W)

		self.cancel = ttk.Button(self.buttonFrame,text="Cancel",command=self.master.destroy)
		self.cancel.grid(row=0,column=0)

		self.apply = ttk.Button(self.buttonFrame,text="Apply")
		self.apply.grid(row=0,column=1)

	def setValues(self, settingsDict):
		self.settingsPanel.setValues(settingsDict)
		

		

		

	#toolbar = NavigationToolbar2TkAgg(canvas, root)
	#toolbar.update()

class EditField(ttk.Frame):
	def __init__(self,master, *args, **kwargs):
		self.ID = "EditField"
		ttk.Frame.__init__(self, master)#, *args, **kwargs)
		self.master = master
		self.editable = kwargs["editable"]
		self.mainFrame = ttk.Frame(self.master)
		self.mainFrame.grid(sticky=E)

		self.label = ttk.Label(self.mainFrame, text=kwargs["text"])
		self.label.grid(row=0,column=0,sticky=W)

		self.entry = ttk.Entry(self.mainFrame,width=kwargs["entryWidth"])
		self.entry.grid(row=0,column=1, sticky=E)
		if not self.editable:
			self.entry.config(state="readonly")


	def get(self):
		return self.entry.get()
	
	def setEntry(self, value):
		print "setting:",value
		if not self.editable:
			self.entry.config(state=NORMAL)
		self.entry.delete(0, 'end')
		self.entry.insert(0, str(value))
		if not self.editable:
			self.entry.config(state="readonly")

class ConfigSettings(ttk.Frame):
	"""docstring for ConfigSettings"""
	def __init__(self, master):
		ttk.Frame.__init__(self,master)
		self.master = master
		self.mainFrame = ttk.Frame(self.master)
		self.mainFrame.grid()

		self.freqSurvDepthE = EditField(self.mainFrame, text="frequency survey depth", editable=True, entryWidth="40")
		self.freqSurvDepthE.grid(row=0)
		self.freqThresholdE = EditField(self.mainFrame, text="frequency threshold", editable=True, entryWidth="40")
		self.freqThresholdE.grid(row=1)
		self.freqStabValueE = EditField(self.mainFrame, text="frequency stability value", editable=True, entryWidth="40")
		self.freqStabValueE.grid(row=2)
		self.magThresholdE = EditField(self.mainFrame, text="magnitude threshold", editable=True, entryWidth="40")
		self.magThresholdE.grid(row=3)

		self.submit = ttk.Button(self.mainFrame, text="Apply")
		self.submit.grid(row=4, sticky=E+W)
