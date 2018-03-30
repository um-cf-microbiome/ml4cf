import socket, os, sys

class info():
     def __init__(self):
      self.user_name = os.getlogin()
      self.host_name = socket.gethostname()
# Setup computing environment for user 'meek'
      if 'meek' in self.user_name:
       if socket.gethostname() == 'WSPDR062':
        self.host_base = str("F:/")
        self.mothur_path = str(self.host_base+"software/mothur/mothur.exe")
        self.R_path=str('C:/Program Files/R/R-3.4.3/bin/Rscript.exe')
        sys.path.insert(0,str(self.host_base+'software/libsvm/tools'))
        sys.path.insert(0,str(self.host_base+"NTM/src"))
        self.processors=4
       if socket.gethostname() == 'Louie':
        if sys.platform == 'win32': self.host_base = str("D:/")
        if sys.platform == 'linux': self.host_base = str("/mnt/d/")
        self.mothur_path = str(self.host_base+"software/mothur_win/mothur/mothur.exe")
        self.R_path=str('D:/software/R-3.4.4/bin/Rscript.exe')
        sys.path.insert(0,str(self.host_base+'software/libsvm/tools'))
        sys.path.insert(0,str(self.host_base+"NTM/src"))
        self.processors=4
       if socket.gethostname() == 'elbel':
        self.host_base = str("/home/"+os.environ.get('USER')+"/")
        self.mothur_path = str(self.host_base+"software/mothur/")
       if socket.gethostname() == 'flux-login1.arc-ts.umich.edu':
        self.host_base = str("/home/"+os.environ.get('USER')+"/")
        self.mothur_path = str(self.host_base+"software/mothur/")
       if socket.gethostname() == 'sparty':
        self.host_base = str("/home/garrettameek/")
        self.mothur_path = str(self.host_base+"software/mothur/mothur.exe")
        self.R_path=str('C:/Program Files/R/R-3.4.3/bin/Rscript.exe')
        sys.path.insert(0,str(self.host_base+'software/libsvm/tools'))
        sys.path.insert(0,str(self.host_base+"NTM/src"))
        self.processors=4
# Setup computing environment for other users
      if not 'meek' in self.user_name:
       if socket.gethostname() == 'flux-login1.arc-ts.umich.edu':
        self.host_base = str("/home/"+os.environ.get('USER')+"/")
        self.mothur_path = str(self.host_base+"software/mothur/")

