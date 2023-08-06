from xes import AIspeak
class Speak(object):
  '''说话'''
  def __init__(self,text=''):
    '''构造函数'''
    self.speak=AIspeak.speak
    self.text=text
  def setMode(self,mode="boy"):
    '''设置语音模式'''
    AIspeak.setmode(mode)
  def setHigh(self):
    '''设置高'''
    AIspeak.sethigh()
  def speak(self,text='defaut'):
    '''开始说话'''
    if text=="defaut":
      text2=self.text
    else:
      text2=text
    self.speak(text2)
  pass