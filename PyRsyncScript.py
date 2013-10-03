#! /usr/bin//python -tt

import sys
import os
import subprocess
import logging
import time
import datetime


def getFileList(path):
  #Currently unused
  onlyfiles = [ f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f)) ]
  return onlyfiles

def rsyncFile(SRC, DST):
  #Include trailing '/' to sync files not directories
  logging.info(str(datetime.datetime.now()) + SRC +" -> " + DST)
  command = ['rsync','-av','--list-only',SRC+'/',DST+'/'] 
  output = subprocess.check_output(command) 
  logging.info(str(datetime.datetime.now()) +': Rsync File List: ' + output)
  #Remove the '--list-only' argument
  command.pop(2)
  output = subprocess.check_output(command)
  logging.info(str(datetime.datetime.now()) + ': Rsync Output: ' + output)

def main():
  if len(sys.argv) != 5:
    print "usage: backup.py <SRC> <DST> <logfile> <h | f>"
    sys.exit(1)
  
  SRC = sys.argv[1] 
  DST = sys.argv[2]
  LOGFILE = sys.argv[3]
  DUPLEX = sys.argv[4]
  
  #Attempt to establish logging with supplied path
  try:
    logging.basicConfig(filename=LOGFILE, level=logging.DEBUG) 
    logging.info(str(datetime.datetime.now()) +" : Running...")
  except IOError:
    print 'IOError with logfile!'
  
  #Check that paths exist as directories, if not, exit
  if not os.path.isdir(SRC) or not os.path.isdir(DST):
    logging.warning(str(datetime.datetime.now()) + ': Check that paths exist!')
    sys.exit(1) 

  #Check that DUPLEX is valid  
  if not (DUPLEX == 'h' or DUPLEX == 'f'):
    logging.warning(str(datetime.datetime.now()) + ': Invalid DUPLEX value!  Must be h or f!')
    sys.exit(1) 
  
#  synclist = []
#  srclist = getFileList(SRC)
#  dstlist = getFileList(DST)
#  for f in srclist:
#    if f not in dstlist:
#      synclist.extend(f)  
#  print synclist
  rsyncFile(SRC, DST)
  if DUPLEX == 'f':
    rsyncFile(DST, SRC)

if __name__ == '__main__':
  main()