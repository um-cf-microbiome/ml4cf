# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 15:42:39 2018

@author: gameek
"""

import subprocess
#subprocess.check_call(["F:\\software\\mothur\\mothur.exe"])
#subprocess.check_call(["F:\\software\\mothur\\mothur.exe"," < ","F:\\NTM\\analysis\\mothur\\stability.batch"," > ","F:\\NTM\\analysis\\mothur\\mothur.out"])
subprocess.check_call(["F:\\software\\mothur\\mothur.exe","F:\\NTM\\analysis\\mothur\\stability.batch"])
#subprocess.check_call(["F:\\software\\mothur\\mothur.exe","F:\\NTM\\analysis\\mothur\\stability.batch",">","F:\\NTM\\analysis\\mothur\\mothur.out"])
#subprocess.check_call(["F:\\software\\mothur\\mothur.exe < F:\\NTM\\analysis\\mothur\\stability.batch > F:\\NTM\\analysis\\mothur\\mothur.out"])
quit()