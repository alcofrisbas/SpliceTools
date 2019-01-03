from Tkinter import *
import ttk
from settings import IndividualSettings

class Tray(ttk.Frame):
	def __init__(self, master, *args, **kwargs):
		self.ID = "Tray"
		self.items = []
		self.settingsList = kwargs["settings"]
		#self.initialSettings = kwargs["initialSettings"]
		ttk.Frame.__init__(self, master)#, *args, **kwargs)
		self.master = master
		
		self.mainFrame = ttk.Frame(self.master)
		self.mainFrame.grid()
		#self.count = 0
		
		#self.placeholder = TrayItem(self.master, buttonText="placeholder", settings=kwargs["settings"])
		#self.placeholder.grid()


	def addItem(self, item,buttonText="", consFile=""):
		temp = TrayItem(self.mainFrame, settings=self.settingsList,initialSettings=item,buttonText=buttonText, consFile=consFile)
		print "TEMP",temp
		self.items.append(temp)
		self.items[-1].grid(row=(len(self.items)-1)%8, column=(len(self.items)-1)/8)
		#print "Tray Item::::::::", self.items[-1]
		#temp.exec_()

	def clear(self):
		# for i in self.items:
		# 	print "i=======",i
		# 	i.grid_remove()
		# 	del(i)
		#for widget in self.mainFrame.winfo_children():
			#widget.destroy()
		# make better delete
		#self.items = []
		pass



class TrayItem(ttk.Button):
	def __init__(self, master, *args, **kwargs):
		self.ID="TrayItem"
		#k = {"command":"self.exec"}
		print kwargs
		self.settingsList = kwargs["settings"]
		self.initialSettings = kwargs["initialSettings"]
		t = "{} + {}".format(self.initialSettings.get("consFile"),self.initialSettings.get("consFile"))
		#print "================================",t
		ttk.Button.__init__(self,master, text=kwargs["buttonText"],command=self.exec_)

	def exec_(self):
		print "woot!"
		t = Toplevel(self.master)
		i = IndividualSettings(t, settings=self.settingsList)#, consFile=consFile)
		i.setValues(self.initialSettings)
		i.grid()

	#def erase()
