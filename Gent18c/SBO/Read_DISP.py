import odbAccess 


names = ['PBCx']  

NodesOfInterest = [1]		   

PreferredExtension = '.dat' 

StepName = 'Step-1'         

PartName = 'PART-1-1'       #Name of the Part

Variable1 = 'U'             #Name of the Variable 


setname= 'SETDISP'

NameOfFile = 'Disp'+PreferredExtension
FileResultsX = open(NameOfFile,'w')
for y in range(len(names)):



	Name = names[y]+'.odb'
	myOdb = odbAccess.openOdb(path=Name)
	lastStep = myOdb.steps[StepName]
	
	for z in range(len(lastStep.frames)):
		lastFrame = myOdb.steps[StepName].frames[z]
		tiempo=lastFrame.frameValue
			
		
	node = myOdb.rootAssembly.instances[PartName].nodeSets[setname]
	displacement = lastFrame.fieldOutputs[Variable1].getSubset(region=node)
			
				
	for val in displacement.values:
		FileResultsX.write('%10.9E\n ' % (val.data[0]))

				
	 
	myOdb.close()
FileResultsX.close()
execfile('C:\\Temp\\YM.py')