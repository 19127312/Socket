import codecs
import winreg
import os
regFile = codecs.open ("fileReg.reg", encoding="utf-8")
reg = regFile.read ()
regFile.close ()
print (reg)