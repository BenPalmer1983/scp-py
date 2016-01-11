# !/usr/bin/python
import os, sys, time, shutil, subprocess;

#---------------------------------------------------------------------------
# Begin Functions
#---------------------------------------------------------------------------

def subString(inputStr, start, length):
  a = start-1
  output = inputStr[a:a+length]
  return output

def replaceCI(haystack,needle,replace):  # Replace, case insensitive
  haystackU = haystack.upper()
  needleU = needle.upper()
  output = ""
  i=0
  while i<len(haystackU):
    i = i + 1
    testNeedleU = subString(haystackU,i,len(needle))
    if needleU==testNeedleU:
      i = i + len(needle)-1
      output = output + replace
    else:
      output = output + subString(haystack,i,1)
  return output

def removeSpaces(inputStr):
# Removes spaces
  output = ""
  i=0
  while i<len(inputStr):
    i = i + 1
    testChar = subString(inputStr,i,1)
    if ord(testChar) != 32:
      output = output + testChar
  return output

def removeBlanks(inputStr):
# Removes spaces, tabs, returns
  output = ""
  i=0
  while i<len(inputStr):
    i = i + 1
    testChar = subString(inputStr,i,1)
    if ord(testChar) not in (9,10,13,32):
      output = output + testChar
  return output

def removeTabs(inputStr):
# Removes spaces
  output = ""
  i=0
  while i<len(inputStr):
    i = i + 1
    testChar = subString(inputStr,i,1)
    if ord(testChar) != 9:
      output = output + testChar
  return output

def removeCR(inputStr):
# Removes spaces
  output = ""
  i=0
  while i<len(inputStr):
    i = i + 1
    testChar = subString(inputStr,i,1)
    if ord(testChar) not in (10,13):
      output = output + testChar
  return output

def trim(inputStr):
  output = ""
  i = len(inputStr)
  lastSpace = 0
  while i>0:
    charSelected = subString(inputStr,i,1)
    if lastSpace==0:
      if charSelected!=" ":
        lastSpace = 1
        output = charSelected + output
    else:
      output = charSelected + output
    i = i - 1
  return output

def trimAll(inputStr):
  output = ""
  i = len(inputStr)
  lastSpace = 0
  while i>0:
    charSelected = subString(inputStr,i,1)
    if lastSpace==0:
      if ord(charSelected) not in (9,10,13,32):
        lastSpace = 1
        output = charSelected + output
    else:
      output = charSelected + output
    i = i - 1
  return output

def trimLeading(inputStr):
  output = ""
  i = 0
  iEnd = len(inputStr)
  firstSpace = 1
  while i<iEnd:
    i = i + 1
    charSelected = subString(inputStr,i,1)
    if firstSpace==1:
      if ord(charSelected)!=(32):
        firstSpace = 0
        output = output + charSelected
    else:
      output = output + charSelected
  return output

def countLeading(inputStr):
  i = 0
  iEnd = len(inputStr)
  firstSpace = 1
  counter = 0
  while i<iEnd:
    i = i + 1
    charSelected = subString(inputStr,i,1)
    if firstSpace==1:
      if ord(charSelected)!=(32):
        firstSpace = 0
      else:
        counter = counter + 1
  return counter

def spacesString(length):
  i = 0
  output = ""
  while i<length:
    i = i + 1
    output = output + " "
  return output

def removeTrailingComma(inputStr):
  inputStr = trimAll(inputStr)
  if subString(inputStr,len(inputStr),1)==",":
    inputStr = subString(inputStr,1,len(inputStr)-1)
  return inputStr

def stristr(haystack, needle):
# Finds string in a string - case sensitive
  result = False
  i = 0
  jEnd = len(needle)
  iEnd = len(haystack)-jEnd+1
  while i<iEnd:
    i = i + 1
    testStr = ""
    j=0
    while j<jEnd:
      j = j + 1
      testStr = testStr + subString(haystack,i+j-1,1)
    if testStr==needle:
      result = True
  return result

def stristrci(haystack, needle):
# Finds string in a string - case insensitive
  result = False
  i = 0
  jEnd = len(needle)
  iEnd = len(haystack)-jEnd+1
  haystack = haystack.upper()
  needle = needle.upper()
  while i<iEnd:
    i = i + 1
    testStr = ""
    j=0
    while j<jEnd:
      j = j + 1
      testStr = testStr + subString(haystack,i+j-1,1)
    if testStr==needle:
      result = True
  return result

def filenamenoext(filename):
  if stristr(filename,".")==False:
    result = filename
  else:
    result = ""
    nameLen = len(filename)
    i = nameLen
    j = 0
    while i>0:
      j = j + 1
      testStr = subString(filename,i,1)
      if(testStr=="."):
        i = 0
      else:
        i = i - 1
    i = 1
    while i<=(nameLen-j):
      result = result+subString(filename,i,1)
      i = i + 1
  return result

# Copies files not more than timeInterval old from course to dest
# Deletes files older than this in destination
def recentDir(source, destination, timeInterval):
  now = time.time()
  if not os.path.exists(destination):
    os.mkdir(destination)
  for file in os.listdir(source):
    sourceFile=source+"/"+file
    if(stristr(file,".")==False):
      destinationDir = destination+"/"+file
      recentDir(sourceFile, destinationDir, timeInterval)
    else:
      fileAge=(now-os.path.getmtime(sourceFile))
      if(fileAge<=timeInterval):
        if not os.path.exists(destination):
          os.mkdir(destination)
        destinationFile=destination+"/"+file
        shutil.copyfile(sourceFile,destinationFile)
        shutil.copystat(sourceFile,destinationFile)
  for file in os.listdir(destination):
    destinationFile=destination+"/"+file
    fileAge=(now-os.path.getmtime(destinationFile))
    if(fileAge>timeInterval):
      os.remove(destinationFile)

def emptyFilesDir(directory, age):  # Empty files from folder older than age - recursive
  now = time.time()
  for file in os.listdir(directory):
    filePath = directory+"/"+file
    if(stristr(file,".")==False):
      emptyFilesDir(filePath, age)
    else:
      fileAge=(now-os.path.getmtime(filePath))
      if(fileAge>age):
        os.remove(filePath)

def archiveDir(dir, dirArc, age):  # Archive files older than age - recursive
  now = time.time()
  if not os.path.exists(dirArc):
    os.mkdir(dirArc)
  for file in os.listdir(dir):
    filePath = dir+"/"+file
    if(stristr(file,".")==False):
      filePathArc = dirArc+"/"+file
      archiveDir(filePath, filePathArc, age)
    else:
      fileAge=(now-os.path.getmtime(filePath))
      if(fileAge>age):
        shutil.copy(filePath,dirArc)

def buildTree(treeRoot):
  cwd = os.getcwd()
  f = open(cwd+'/.pytree.loc','w')
  f.write("")
  f.close()
  buildTreeR(treeRoot)

def buildTreeR(treeBranch):
  cwd = os.getcwd()
  for file in os.listdir(treeBranch):
    filePath = treeBranch+"/"+file
    if(os.path.isdir(filePath)):
      f = open(cwd+'/.pytree.loc','a')
      f.write(filePath+"|"+str(os.path.getmtime(filePath))+"|1\n")
      f.close()
      buildTreeR(filePath)
    else:
      f = open(cwd+'/.pytree.loc','a')
      f.write(filePath+"|"+str(os.path.getmtime(filePath))+"|0\n")
      f.close()

def buildTreeSSH(ssh, sshport, treeRoot):
  cwd = os.getcwd()
  f = open(cwd+'/.runremote.py','w')
  f.write("# !/usr/bin/python"+"\n")
  f.write("import os, sys, time, shutil, subprocess;"+"\n")
  f.write("def buildTree(treeRoot):"+"\n")
  f.write("  cwd = os.getcwd()"+"\n")
  f.write("  f = open(cwd+'/.pytree.rem','w')"+"\n")
  f.write("  f.write(\"\")"+"\n")
  f.write("  f.close()"+"\n")
  f.write("  buildTreeR(treeRoot)"+"\n")
  f.write("def buildTreeR(treeBranch):"+"\n")
  f.write("  cwd = os.getcwd()"+"\n")
  f.write("  for file in os.listdir(treeBranch):"+"\n")
  f.write("    filePath = treeBranch+\"/\"+file"+"\n")
  f.write("    if(os.path.isdir(filePath)):"+"\n")
  f.write("      f = open(cwd+'/.pytree.rem','a')"+"\n")
  f.write("      f.write(filePath+\"|\"+str(os.path.getmtime(filePath))+\"|1\\n\")"+"\n")
  f.write("      f.close()"+"\n")
  f.write("      buildTreeR(filePath)"+"\n")
  f.write("    else:"+"\n")
  f.write("      if(file!=\".pytree.rem\"): "+"\n")
  f.write("        if(file!=\".runremote.py\"): "+"\n")
  f.write("          f = open(cwd+'/.pytree.rem','a')"+"\n")
  f.write("          f.write(filePath+\"|\"+str(os.path.getmtime(filePath))+\"|0\\n\")"+"\n")
  f.write("          f.close()"+"\n")
  f.write("dirRemote = \""+treeRoot+"\""+"\n")
  f.write("buildTree(dirRemote)"+"\n")
  f.close()
# Transfer file and run remotely
  process = subprocess.Popen("scp -P "+sshport+" "+cwd+"/.runremote.py bxp912@localhost:"+treeRoot, shell=True, stdout=subprocess.PIPE).stdout.read()
  process = subprocess.Popen("ssh -p "+sshport+" "+ssh+" 'cd "+treeRoot+"; python .runremote.py;'", shell=True, stdout=subprocess.PIPE).stdout.read()
  process = subprocess.Popen("scp -P "+sshport+" "+ssh+":"+treeRoot+"/.pytree.rem "+cwd+"/.pytree.rem" , shell=True, stdout=subprocess.PIPE).stdout.read()
# Clean up remote
  process = subprocess.Popen("ssh -p "+sshport+" "+ssh+" 'cd "+treeRoot+"; rm .runremote.py;'", shell=True, stdout=subprocess.PIPE).stdout.read()
  process = subprocess.Popen("ssh -p "+sshport+" "+ssh+" 'cd "+treeRoot+"; rm .pytree.rem;'", shell=True, stdout=subprocess.PIPE).stdout.read()
# Clean up local
  os.remove(cwd+"/.runremote.py")

def scpSync(dirLocal, dirRemote, ssh, sshport):
# Tar Mode
  tarMode = True
# General vars
  now = time.time()
  cwd = os.getcwd()
# Arrays
  localDirs=[None]*10000
  localFiles=[None]*100000
  localFilesMod=[None]*100000
  remoteDirs=[None]*10000
  remoteFiles=[None]*100000
  remoteFilesMod=[None]*100000
# check if local/remote exist
  dirLocalTemp = dirLocal.replace(' ','\ ')
  dirRemoteTemp = dirRemote.replace(' ','\ ')
  process = subprocess.Popen("mkdir -p "+dirLocalTemp+";", shell=True, stdout=subprocess.PIPE).stdout.read()
  process = subprocess.Popen("ssh -p "+sshport+" "+ssh+" 'mkdir -p "+dirRemoteTemp+"';", shell=True, stdout=subprocess.PIPE).stdout.read()
# Make local tree file
  buildTree(dirLocal)
#load local dirs to array
  fh = open(cwd+"/.pytree.loc", "rw+")
  ldc = 0
  lfc = 0
  for line in fh:
    lineArr = line.split("|")
    if(int(lineArr[2])==1): # Dirs
      makePath = subString(lineArr[0],len(dirLocal)+1,len(lineArr[0])-len(dirLocal))
      ldc = ldc + 1
      localDirs[ldc] = makePath
    if(int(lineArr[2])==0): # Files
      makePath = subString(lineArr[0],len(dirLocal)+1,len(lineArr[0])-len(dirLocal))
      lfc = lfc + 1
      localFiles[lfc] = makePath
      localFilesMod[lfc] = float(lineArr[1])
  fh.close()
# Clean up
  os.remove(cwd+"/.pytree.loc")
# Make remote tree file
  buildTreeSSH(ssh, sshport, dirRemote)
#load remote dirs to array
  fh = open(cwd+"/.pytree.rem", "rw+")
  rdc = 0
  rfc = 0
  for line in fh:
    lineArr = line.split("|")
    if(int(lineArr[2])==1): # Dirs
      makePath = subString(lineArr[0],len(dirRemote)+1,len(lineArr[0])-len(dirRemote))
      rdc = rdc + 1
      remoteDirs[rdc] = makePath
    if(int(lineArr[2])==0): # Files
      makePath = subString(lineArr[0],len(dirRemote)+1,len(lineArr[0])-len(dirRemote))
      rfc = rfc + 1
      remoteFiles[rfc] = makePath
      remoteFilesMod[rfc] = float(lineArr[1])
  fh.close()
# Clean up
  os.remove(cwd+"/.pytree.rem")
# Make remote dirs on local
  i = 0
  dirCount = 0
  cmd = ""
  while i<rdc:
    i = i + 1
    exists = False
    j = 0
    while j<ldc:
      j = j + 1
      if(remoteDirs[i]==localDirs[j]):
        exists = True
        break
    if(exists==False and remoteDirs[i]!=None):
      cmd = cmd + "mkdir -p "+dirLocal+remoteDirs[i]+"; "
      dirCount = dirCount + 1
  if(dirCount>0):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
    print "Creating "+str(dirCount)+" dirs in local dir"
# Make local directories on remote
  i = 0
  dirCount = 0
  cmd = ""
  while i<ldc:
    i = i + 1
    exists = False
    j = 0
    while j<rdc:
      j = j + 1
      if(localDirs[i]==remoteDirs[j]):
        exists = True
        break
    if(exists==False and localDirs[i]!=None):
      cmd = cmd + "mkdir -p "+dirRemote+localDirs[i]+"; "
      dirCount = dirCount + 1
  if(dirCount>0):
    process = subprocess.Popen("ssh -p "+sshport+" "+ssh+" '"+cmd+"'", shell=True, stdout=subprocess.PIPE).stdout.read()
# Files to remote
  cmdC = ""
  cmdU = ""
  i = 0
  filesCreated = 0
  filesUpdated = 0
  tarLocal = "tar cvzf "+cwd+"/.localT.tar.gz \\\n"
  while i<lfc:
    i = i + 1
    exists = False
    j = 0
    while j<rfc:
      j = j + 1
      if(localFiles[i]==remoteFiles[j]):
        exists = True
        break
    if(exists==False and localFiles[i]!=None):
      filesCreated = filesCreated + 1
      localFileTemp = localFiles[i]
      localFileTemp = localFileTemp.replace(' ','\ ')
      cmdC = cmdC + "scp -p -P "+sshport+" "+dirLocal+localFileTemp+" "+ssh+":'"+dirRemote+localFileTemp+"'; "
      tarLocal = tarLocal + "--add-file="+subString(localFileTemp,2,len(localFileTemp)-1)+" \\\n"
    if(exists==True and localFiles[i]!=None and (localFilesMod[i]-remoteFilesMod[j])>30):
      filesUpdated = filesUpdated + 1
      localFileTemp = localFiles[i]
      localFileTemp = localFileTemp.replace(' ','\ ')
      cmdU = cmdU + "scp -p -P "+sshport+" "+dirLocal+localFileTemp+" "+ssh+":'"+dirRemote+localFileTemp+"'; "
      tarLocal = tarLocal + "--add-file="+subString(localFileTemp,2,len(localFileTemp)-1)+" \\\n"
  if(filesCreated>0):
    if(tarMode==False):
      process = subprocess.Popen(cmdC, shell=True, stdout=subprocess.PIPE).stdout.read()
    print "Creating "+str(filesCreated)+" new files in remote dir"
  if(filesUpdated>0):
    if(tarMode==False):
      process = subprocess.Popen(cmdU, shell=True, stdout=subprocess.PIPE).stdout.read()
    print "Updating "+str(filesUpdated)+" files in remote dir"
  tarLocal = tarLocal + "--exclude=\""+cwd+"/.localT.tar.gz\""
  if(tarMode==True and (filesCreated+filesUpdated)>0):
    process = subprocess.Popen("cd "+dirLocal+"; "+tarLocal+";", shell=True, stdout=subprocess.PIPE).stdout.read()
    cmd = "scp -p -P "+sshport+" "+cwd+"/.localT.tar.gz"+" "+ssh+":'"+dirRemote+"/.localT.tar.gz'; "
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
    process = subprocess.Popen("rm "+cwd+"/.localT.tar.gz;", shell=True, stdout=subprocess.PIPE).stdout.read()
    cmd = "cd "+dirRemote+"; tar xzvf "+dirRemote+"/.localT.tar.gz; rm "+dirRemote+"/.localT.tar.gz;"
    process = subprocess.Popen("ssh -p "+sshport+" "+ssh+" '"+cmd+"'", shell=True, stdout=subprocess.PIPE).stdout.read()
# Files to local
  cmdC = ""
  cmdU = ""
  i = 0
  filesCreated = 0
  filesUpdated = 0
  tarRemote = "tar cvzf "+dirRemote+"/.remoteT.tar.gz \\\n"
  while i<rfc:
    i = i + 1
    exists = False
    j = 0
    while j<lfc:
      j = j + 1
      if(remoteFiles[i]==localFiles[j]):
        exists = True
        break
    if(exists==False and remoteFiles[i]!=None):
      filesCreated = filesCreated + 1
      remoteFileTemp = remoteFiles[i]
      remoteFileTemp = remoteFileTemp.replace(' ','\ ')
      cmdC = cmdC + "scp -p -P "+sshport+" "+ssh+":'"+dirRemote+remoteFileTemp+"' "+dirLocal+remoteFileTemp+"; "
      tarRemote = tarRemote + "--add-file="+subString(remoteFileTemp,2,len(remoteFileTemp)-1)+" \\\n"
    if(exists==True and remoteFiles[i]!=None and (remoteFilesMod[i]-localFilesMod[j])>30):
      filesUpdated = filesUpdated + 1
      remoteFileTemp = remoteFiles[i]
      remoteFileTemp = remoteFileTemp.replace(' ','\ ')
      cmdU = cmdU + "scp -p -P "+sshport+" "+ssh+":'"+dirRemote+remoteFileTemp+"' "+dirLocal+remoteFileTemp+"; "
      tarRemote = tarRemote + "--add-file="+subString(remoteFileTemp,2,len(remoteFileTemp)-1)+" \\\n"
  if(filesCreated>0):
    if(tarMode==False):
      process = subprocess.Popen(cmdC, shell=True, stdout=subprocess.PIPE).stdout.read()
    print "Creating "+str(filesCreated)+" new files in local dir"
  if(filesUpdated>0):
    if(tarMode==False):
      process = subprocess.Popen(cmdU, shell=True, stdout=subprocess.PIPE).stdout.read()
    print "Updating "+str(filesUpdated)+" files in local dir"
  tarRemote = tarRemote + "--exclude=\""+dirRemote+"/.remoteT.tar.gz\""
  if(tarMode==True and (filesCreated+filesUpdated)>0):
    cmd = "cd "+dirRemote+"; "+tarRemote+";"
    process = subprocess.Popen("ssh -p "+sshport+" "+ssh+" '"+cmd+"'", shell=True, stdout=subprocess.PIPE).stdout.read()
    cmd = "scp -p -P "+sshport+" "+ssh+":'"+dirRemote+"/.remoteT.tar.gz' "+" "+cwd+"/.remoteT.tar.gz"
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
    cmd = "rm "+dirRemote+"/.remoteT.tar.gz;"
    process = subprocess.Popen("ssh -p "+sshport+" "+ssh+" '"+cmd+"'", shell=True, stdout=subprocess.PIPE).stdout.read()
    cmd = "cd "+dirLocal+"; tar xzvf "+cwd+"/.remoteT.tar.gz; rm "+cwd+"/.remoteT.tar.gz;"
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()

#---------------------------------------------------------------------------
# End Functions
#---------------------------------------------------------------------------

#input arguments
arguments=[None]*10
counter = 0

for arg in sys.argv:
  counter = counter + 1
  arguments[counter] = arg

# Option
option = arguments[2]

# Process option
if(option=="copyrecent"):
  source = arguments[3]
  destination = arguments[4]
  timeInterval = int(arguments[5])
  recentDir(source, destination, timeInterval)

if(option=="removeold"):
  emptyDir = arguments[3]
  timeInterval = int(arguments[4])
  emptyFilesDir(emptyDir, timeInterval)

if(option=="archive"):
  source = arguments[3]
  destination = arguments[4]
  timeInterval = int(arguments[5])
  archiveDir(source, destination, timeInterval)

if(option=="scpsync"):
  local = arguments[3]
  remote = arguments[4]
  ssh = arguments[5]
  sshport = arguments[6]
  scpSync(local, remote, ssh, sshport)
