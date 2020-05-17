import psutil
import time
import sys
import os

'''def findProcessIdByName(processName, secsRestart, noOfAttempts, intervalsSecs, genLogs):'''
def findProcessIdByName(processName):
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


processNameVal = sys.argv[1]

'''listOfProcessIds = findProcessIdByName(args.processName, args.secsRestart, args.noOfAttempts, args.intervalsSecs, args.genLogs)'''
listOfProcessIds = findProcessIdByName(processNameVal)
print(processNameVal)

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
      secsRestart = raw_input("Seconds to wait between attempts to restart service : ")
      noOfAttempts = raw_input("Number of attempts before giving up : ")
      intervalsSecs = raw_input("Check interval in seconds : ")
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
   else :
      print('Unable to start the service')
