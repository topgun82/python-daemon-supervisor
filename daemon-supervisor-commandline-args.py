import psutil
import time
import sys
import argparse

parser = argparse.ArgumentParser(description='The idea is to create a daemon supervisor. This tool should check that the process is running and at all times and starts it in case is down.', add_help=False)
parser.add_argument('--help', action='help', help='Example format : python daemon-supervisor-commandline-args.py <processName> <secsRestart> <noOfAttempts> <intervalsSecs> <genLogs>, Example Input : python daemon-supervisor-commandline-args.py cron 1 2 1 y')
parser.add_argument('processName', type=open, help='Name of the process to supervise')
parser.add_argument('secsRestart', type=int, help='Seconds to wait between attempts to restart service')
parser.add_argument('noOfAttempts', type=int, help='Number of attempts before giving up')
parser.add_argument('intervalsSecs', type=int, help='Check interval in seconds')
parser.add_argument('genLogs', type=open, help='Generate logs in case of events')

def findProcessIdByName(processName, secsRestart, noOfAttempts, intervalsSecs, genLogs):
    '''
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
    '''

    listOfProcessObjects = []

    #Iterate over the all the running process
    for proc in psutil.process_iter():
       try:
           pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
           # Check if process name contains the given name string.
           if processName.lower() in pinfo['name'].lower() :
               listOfProcessObjects.append(pinfo)
       except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
           pass

    return listOfProcessObjects;


args = parser.parse_args()

listOfProcessIds = findProcessIdByName(args.processName, args.secsRestart, args.noOfAttempts, args.intervalsSecs, args.genLogs)
print(processName)
print(secsRestart)

if len(listOfProcessIds) > 0:
   print('Process Exists | PID and other details are')
   for elem in listOfProcessIds:
       processID = elem['pid']
       processName = elem['name']
       processCreationTime =  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(elem['create_time']))
       print((processID ,processName,processCreationTime ))
else :
   print(processNameVal,'process/service is currently down !')
   getOpt = raw_input("Would you like to start the process?(yes/no)")
   getOptVal = str(getOpt)
   print(getOptVal)

   if any([getOptVal == "yes", getOptVal == "YES", getOptVal == "Y"]):
      print('Start the service------------')
      secsRestart = args.secsRestart
      noOfAttempts = args.noOfAttempts
      intervalsSecs = args.intervalsSecs
      startTime = time.time()
      print(noOfAttempts)
      for i in range(2):
          print('Attemp no :', i)
          # making delay for 1 second
          time.sleep(float(secsRestart))
          os.system("sudo service " +processNameVal+ " restart")
      endTime = time.time()
      elapsedTime = endTime - startTime
      print("Elapsed Time = %s" % elapsedTime)
      print("Process is currently up and running !")
   else :
      print('Unable to start the service')
