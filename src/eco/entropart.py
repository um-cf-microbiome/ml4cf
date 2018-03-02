# This file contains subroutines that act as a wrapper for 'entropart'
global entropart_src_dir, R_exe, output_dir, output_file
import subprocess, sys, os
entropart_src_dir = "F:/software/entropart-master/R/"
R_exe = "C:/Program Files/R/R-3.4.3/bin/Rscript.exe"
output_dir = "F:/NTM/analysis/entropart/"
func = "ShannonBeta.R"
output_file = str(func.split(".R",1)[0]+".dat")

def get_value(function,alpha_abd_vector,beta_abd_vector):
 func_name = function.split(".R",1)[0]
 R_script_name = str(output_dir+"temp.R")
 os.chdir(output_dir)
 R_script = open(R_script_name,'w')
 R_script.write(str('library("R.utils")\n'))
 R_script.write(str('library("entropart")\n'))
 if func_name == 'ShannonBeta':
  string = str('output <- '+func_name+'(NorP='+alpha_abd_vector+',NorPexp='+beta_abd_vector+',Correction="Best",CheckArguments=TRUE,Ps=NULL,Ns=NULL,Pexp=NULL,Nexp=NULL)\n')
  R_script.write(string)
 R_script.write(str('write(output,file="'+output_dir+output_file+'")'))
 R_script.close()
 call_cmd = str(R_exe+' '+R_script_name)
 subprocess.call(call_cmd)
 value = open(output_file,'r').read()
 os.remove(R_script_name)
 os.remove(str(output_dir+output_file))
 return(value)

result = get_value(func)
print(result)