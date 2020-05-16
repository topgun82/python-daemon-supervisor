# Find PIDs od all the running instances of process that contains 'chrome' in it's name
listOfProcessIds = findProcessIdByName('chrome')
 
if len(listOfProcessIds) > 0:
   print('Process Exists | PID and other details are')
   for elem in listOfProcessIds:
       processID = elem['pid']
       processName = elem['name']
       processCreationTime =  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(elem['create_time']))
       print((processID ,processName,processCreationTime ))
else :
   print('No Running Process found with given text')
