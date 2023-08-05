import os
import shutil

def mycopyfile(srcfile,dstpath):
    if not os.path.isfile(srcfile):
        print ("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(srcfile)
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)
        shutil.copy(srcfile, dstpath + fname)
        print ("copy %s -> %s"%(srcfile, dstpath + fname))
 
 
src_dir = os.path.dirname(__file__) + 'ME.py'
dst_dir = os.path.dirname(__file__)
mycopyfile(src_dir, dst_dir+"\\")
mycopyfile(os.path.dirname(__file__)+"QE_key.py", os.path.dirname(__file__)+"\\")
