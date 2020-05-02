# -*- coding: mbcs -*-
# rot_x= [10]
# rot_y= [10]
# rot_z= [10] 


numero_seeds=.5
E_matrice=68900
NU_matrice=.3
E_particella=380000
NU_particella=.19

text=open("DATI.py", "r")

data = [line.strip() for line in text]
numero_sfere=int(round(float(data[0])))

x=range(0,numero_sfere)
y=range(0,numero_sfere)
z=range(0,numero_sfere)
scala=range(0,numero_sfere)
riga=1
text.close()
for i in range (0,numero_sfere):
	x[i]=float(data[riga])
	riga=riga+1
for i in range (0,numero_sfere):
	y[i]=float(data[riga])
	riga=riga+1
for i in range (0,numero_sfere):
	z[i]=float(data[riga])
	riga=riga+1
for i in range (0,numero_sfere):
	scala[i]=float(data[riga])
	riga=riga+1
director=str(data[riga])	
os.chdir(director)
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
from sys import *
import odbAccess 
# importo matrice
mdb.openAcis(director+'\Griglia_part.sat', 
    scaleFromFile=OFF)
mdb.models['Model-1'].PartFromGeometryFile(combine=False, dimensionality=
    THREE_D, geometryFile=mdb.acis, name='Matrice', type=DEFORMABLE_BODY)
for sfere in range (0,numero_sfere):	
	mdb.openAcis(director+'\Sfera_r_1.sat', scaleFromFile=
		OFF)
	mdb.models['Model-1'].PartFromGeometryFile(combine=False, dimensionality=
		THREE_D, geometryFile=mdb.acis, name='sfera-%s' %(sfere),scale=scala[sfere], type=DEFORMABLE_BODY) 
# Creo i punti
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='DUMMY-1', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['DUMMY-1'].ReferencePoint(point=(10.0, 5.0, 5.0))
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='DUMMY-2', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['DUMMY-2'].ReferencePoint(point=(5.0, 10.0, 5.0))
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='DUMMY-3', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['DUMMY-3'].ReferencePoint(point=(5.0, 5.0, 10.0))
mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='DUMMY-1-1', 
    part=mdb.models['Model-1'].parts['DUMMY-1'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='DUMMY-2-1', 
    part=mdb.models['Model-1'].parts['DUMMY-2'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='DUMMY-3-1', 
    part=mdb.models['Model-1'].parts['DUMMY-3'])	
# Instance		
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Matrice-1', 
    part=mdb.models['Model-1'].parts['Matrice'])
for sfere in range (0,numero_sfere):	
	mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Sfera-%s' %(sfere), 
		part=mdb.models['Model-1'].parts['sfera-%s' %(sfere)])
# Traslazione sfere	
for sfere in range (0,numero_sfere) :
	# mdb.models['Model-1'].rootAssembly.rotate(angle=90.0, axisDirection=(rot_x[sfere], rot_y[sfere], 
		# rot_x[sfere]), axisPoint=(0.0, 0.0, 0.0),instanceList=('Sfera-%s' %(sfere), ))	
	mdb.models['Model-1'].rootAssembly.translate(instanceList=('Sfera-%s' %(sfere), ), 
		vector=(x[sfere],y[sfere],z[sfere]))
	
mdb.models['Model-1'].rootAssembly.features['Matrice-1'].resume()	
mdb.models['Model-1'].rootAssembly.InstanceFromBooleanCut(cuttingInstances=(
    mdb.models['Model-1'].rootAssembly.instances['Sfera-0'], ), 
    instanceToBeCut=mdb.models['Model-1'].rootAssembly.instances['Matrice-1'], 
    name='bucata-0', originalInstances=SUPPRESS)	
for sfere in range (1,numero_sfere):
	mdb.models['Model-1'].rootAssembly.InstanceFromBooleanCut(cuttingInstances=(
		mdb.models['Model-1'].rootAssembly.instances['Sfera-%s'% (sfere)] , ), 
		instanceToBeCut=mdb.models['Model-1'].rootAssembly.instances['bucata-%s-1' %(sfere-1)], 
		name='bucata-%s' % (sfere), originalInstances=SUPPRESS)
for sfere in range (0,numero_sfere):		
	mdb.models['Model-1'].rootAssembly.features['Sfera-%s' % (sfere)].resume()	
mdb.models['Model-1'].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY, 
    instances=(mdb.models['Model-1'].rootAssembly.instances['Sfera-0'], 
    mdb.models['Model-1'].rootAssembly.instances['bucata-%s-1' %(numero_sfere-1)]), 
    keepIntersections=ON, name='assieme-0', originalInstances=DELETE)	
for sfere in range (1,numero_sfere):	
	mdb.models['Model-1'].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY, 
	  instances=(mdb.models['Model-1'].rootAssembly.instances['Sfera-%s'% (sfere)], 
	  mdb.models['Model-1'].rootAssembly.instances['assieme-%s-1' %(sfere-1)]), 
	  keepIntersections=ON, name='assieme-%s' %(sfere), originalInstances=DELETE)
del mdb.models['Model-1'].parts['Matrice']	
# delete  
for sfere in range (0,numero_sfere):
	del mdb.models['Model-1'].parts['sfera-%s' %(sfere)]
	del mdb.models['Model-1'].parts['bucata-%s' %(sfere)]
del mdb.models['Model-1'].rootAssembly.features['Matrice-1']
for sfere in range(0,numero_sfere-1):	
	del mdb.models['Model-1'].parts['assieme-%s' %(sfere)]
	del mdb.models['Model-1'].rootAssembly.features['bucata-%s-1' %(sfere)]
#Creazione materiali
mdb.models['Model-1'].Material(name='Material-matrice')
mdb.models['Model-1'].Material(name='Material-sfere')
mdb.models['Model-1'].materials['Material-matrice'].Elastic(table=((E_matrice,NU_matrice), ))
mdb.models['Model-1'].materials['Material-sfere'].Elastic(table=((E_particella, NU_particella), ))
#Definizione section
mdb.models['Model-1'].HomogeneousSolidSection(material='Material-sfere', name=
    'section-sfere', thickness=None)
mdb.models['Model-1'].HomogeneousSolidSection(material='Material-matrice', 
    name='section-matrice', thickness=None)	
#Set e section sfere 
mdb.models['Model-1'].parts['assieme-%s' %(numero_sfere-1)].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    cells=mdb.models['Model-1'].parts['assieme-%s' %(numero_sfere-1)].cells.findAt(((0,0,0),), )), sectionName='section-matrice', thicknessAssignment=
    FROM_SECTION)

mdb.models['Model-1'].parts['assieme-%s' %(numero_sfere-1)].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    cells=mdb.models['Model-1'].parts['assieme-%s' %(numero_sfere-1)].cells.getByBoundingBox(.1,.1,.1,9.9,9.9,9.9)), sectionName='section-sfere', thicknessAssignment=
    FROM_SECTION)
	
mdb.models['Model-1'].rootAssembly.Set(cells=
    mdb.models['Model-1'].rootAssembly.instances['assieme-%s-1' %(numero_sfere-1)].cells.getByBoundingBox(-1,-1,-1,11,11,11), name='ASET')

#DUMMY	
mdb.models['Model-1'].rootAssembly.Set(name='DUMMY-1', referencePoints=(
    mdb.models['Model-1'].rootAssembly.instances['DUMMY-1-1'].referencePoints[1], 
    ))
mdb.models['Model-1'].rootAssembly.Set(name='DUMMY-2', referencePoints=(
    mdb.models['Model-1'].rootAssembly.instances['DUMMY-2-1'].referencePoints[1], 
    ))
mdb.models['Model-1'].rootAssembly.Set(name='DUMMY-3', referencePoints=(
    mdb.models['Model-1'].rootAssembly.instances['DUMMY-3-1'].referencePoints[1], 
    ))	
#Mesh	
mdb.models['Model-1'].parts['assieme-%s' %(numero_sfere-1)].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size= numero_seeds)

mdb.models['Model-1'].parts['assieme-%s' %(numero_sfere-1)].setMeshControls(elemShape=TET, 
    regions=mdb.models['Model-1'].parts['assieme-%s' %(numero_sfere-1)].cells.getByBoundingBox(-1,-1,-1,11,11,11), technique=FREE)

mdb.models['Model-1'].parts['assieme-%s' %(numero_sfere-1)].generateMesh()
mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial')

mdb.models['Model-1'].parts.changeKey(fromName='assieme-%s' %(numero_sfere-1), toName='Part-1')
mdb.models['Model-1'].rootAssembly.features.changeKey(fromName='assieme-%s-1' %(numero_sfere-1), 
    toName='Part-1-1')
mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial')
mdb.models['Model-1'].parts['Part-1'].Set(name='SETDISP', nodes=
    mdb.models['Model-1'].parts['Part-1'].nodes.getByBoundingSphere((0,5,5),.05)+\
	mdb.models['Model-1'].parts['Part-1'].nodes.getByBoundingSphere((10,5,5),.05))

#Field Output
mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
    'S','U'))
#Loads
mdb.models['Model-1'].ConcentratedForce(cf1=10000.0, createStepName='Step-1', 
    distributionType=UNIFORM, field='', localCsys=None, name='P100', region=
    mdb.models['Model-1'].rootAssembly.sets['DUMMY-1'])
#-----------------------------------------------------------------------------
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
    distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name='X'
    , region=mdb.models['Model-1'].rootAssembly.sets['DUMMY-1'], u1=UNSET,u2=0.0
    , u3=0.0, ur1=UNSET, ur2=UNSET, ur3=UNSET)
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
    distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name='Y'
    , region=mdb.models['Model-1'].rootAssembly.sets['DUMMY-2'], u1=0.0, u2=
    UNSET, u3=0.0, ur1=UNSET, ur2=UNSET, ur3=UNSET)

mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
    distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name='Z'
    , region=mdb.models['Model-1'].rootAssembly.sets['DUMMY-3'], u1=0.0, u2=0.0
    , u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
mdb.models['Model-1'].rootAssembly.regenerate()

# PBC
execfile(director+'\PBCx_lorenzo.py')
# JOB
mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, 
    multiprocessingMode=THREADS, name='PBCx', nodalOutputPrecision=SINGLE, 
    numCpus=1, numDomains=1, numGPUs=0, queue=None, scratch='', type=ANALYSIS, 
    userSubroutine='', waitHours=0, waitMinutes=0)
mdb.jobs['PBCx'].submit(consistencyChecking=OFF)
mdb.jobs['PBCx'].waitForCompletion()


names = ['PBCx']  

NodesOfInterest = [1]		   

PreferredExtension = '.dat' 

StepName = 'Step-1'         

PartName = 'PART-1-1'       #Name of the Part

Variable1 = 'U'             #Name of the Variable 


setname= 'SETDISP'

NameOfFile = director+'\Disp'+PreferredExtension
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
# time.sleep(0.5)	
FileResultsX.close()
text=open(NameOfFile, "r")
data = [line.strip() for line in text]
x1=float(data[0])
x2=float(data[1])
text.close()
E=(1000/(x2-x1))
es=str(E)
NameOfFile = director+'\YM_calc.txt'
FileResultsX = open(NameOfFile,'w')
FileResultsX.write('%f \n' %(E) )
FileResultsX.close()
	
sys.exit(0)
