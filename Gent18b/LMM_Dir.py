 

Model='Model-1'
numero_seeds=1
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
mdb.openAcis('Griglia_part.sat', 
    scaleFromFile=OFF)
mdb.models[Model].PartFromGeometryFile(combine=False, dimensionality=
    THREE_D, geometryFile=mdb.acis, name='Matrice', type=DEFORMABLE_BODY)
for sfere in range (0,numero_sfere):	
	mdb.openAcis('Sfera_r_1.sat', scaleFromFile=
		OFF)
	mdb.models[Model].PartFromGeometryFile(combine=False, dimensionality=
		THREE_D, geometryFile=mdb.acis, name='sfera-%s' %(sfere),scale=scala[sfere], type=DEFORMABLE_BODY) 
# Creo i punti
mdb.models[Model].Part(dimensionality=THREE_D, name='DUMMY-1', type=
    DEFORMABLE_BODY)
mdb.models[Model].parts['DUMMY-1'].ReferencePoint(point=(10.0, 5.0, 5.0))
mdb.models[Model].Part(dimensionality=THREE_D, name='DUMMY-2', type=
    DEFORMABLE_BODY)
mdb.models[Model].parts['DUMMY-2'].ReferencePoint(point=(5.0, 10.0, 5.0))
mdb.models[Model].Part(dimensionality=THREE_D, name='DUMMY-3', type=
    DEFORMABLE_BODY)
mdb.models[Model].parts['DUMMY-3'].ReferencePoint(point=(5.0, 5.0, 10.0))
mdb.models[Model].rootAssembly.DatumCsysByDefault(CARTESIAN)
mdb.models[Model].rootAssembly.Instance(dependent=ON, name='DUMMY-1-1', 
    part=mdb.models[Model].parts['DUMMY-1'])
mdb.models[Model].rootAssembly.Instance(dependent=ON, name='DUMMY-2-1', 
    part=mdb.models[Model].parts['DUMMY-2'])
mdb.models[Model].rootAssembly.Instance(dependent=ON, name='DUMMY-3-1', 
    part=mdb.models[Model].parts['DUMMY-3'])	
# Instance		
mdb.models[Model].rootAssembly.Instance(dependent=ON, name='Matrice-1', 
    part=mdb.models[Model].parts['Matrice'])
for sfere in range (0,numero_sfere):	
	mdb.models[Model].rootAssembly.Instance(dependent=ON, name='Sfera-%s' %(sfere), 
		part=mdb.models[Model].parts['sfera-%s' %(sfere)])
# Traslazione sfere	
for sfere in range (0,numero_sfere) :
	# mdb.models[Model].rootAssembly.rotate(angle=90.0, axisDirection=(rot_x[sfere], rot_y[sfere], 
		# rot_x[sfere]), axisPoint=(0.0, 0.0, 0.0),instanceList=('Sfera-%s' %(sfere), ))	
	mdb.models[Model].rootAssembly.translate(instanceList=('Sfera-%s' %(sfere), ), 
		vector=(x[sfere],y[sfere],z[sfere]))
	
mdb.models[Model].rootAssembly.features['Matrice-1'].resume()	
mdb.models[Model].rootAssembly.InstanceFromBooleanCut(cuttingInstances=(
    mdb.models[Model].rootAssembly.instances['Sfera-0'], ), 
    instanceToBeCut=mdb.models[Model].rootAssembly.instances['Matrice-1'], 
    name='bucata-0', originalInstances=SUPPRESS)	
for sfere in range (1,numero_sfere):
	mdb.models[Model].rootAssembly.InstanceFromBooleanCut(cuttingInstances=(
		mdb.models[Model].rootAssembly.instances['Sfera-%s'% (sfere)] , ), 
		instanceToBeCut=mdb.models[Model].rootAssembly.instances['bucata-%s-1' %(sfere-1)], 
		name='bucata-%s' % (sfere), originalInstances=SUPPRESS)
for sfere in range (0,numero_sfere):		
	mdb.models[Model].rootAssembly.features['Sfera-%s' % (sfere)].resume()	
mdb.models[Model].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY, 
    instances=(mdb.models[Model].rootAssembly.instances['Sfera-0'], 
    mdb.models[Model].rootAssembly.instances['bucata-%s-1' %(numero_sfere-1)]), 
    keepIntersections=ON, name='assieme-0', originalInstances=DELETE)	
for sfere in range (1,numero_sfere):	
	mdb.models[Model].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY, 
	  instances=(mdb.models[Model].rootAssembly.instances['Sfera-%s'% (sfere)], 
	  mdb.models[Model].rootAssembly.instances['assieme-%s-1' %(sfere-1)]), 
	  keepIntersections=ON, name='assieme-%s' %(sfere), originalInstances=DELETE)
del mdb.models[Model].parts['Matrice']	
# delete  
for sfere in range (0,numero_sfere):
	del mdb.models[Model].parts['sfera-%s' %(sfere)]
	del mdb.models[Model].parts['bucata-%s' %(sfere)]
del mdb.models[Model].rootAssembly.features['Matrice-1']
for sfere in range(0,numero_sfere-1):	
	del mdb.models[Model].parts['assieme-%s' %(sfere)]
	del mdb.models[Model].rootAssembly.features['bucata-%s-1' %(sfere)]
#Creazione materiali
mdb.models[Model].Material(name='Material-matrice')
mdb.models[Model].Material(name='Material-sfere')
mdb.models[Model].materials['Material-matrice'].Elastic(table=((E_matrice,NU_matrice), ))
mdb.models[Model].materials['Material-sfere'].Elastic(table=((E_particella, NU_particella), ))
mdb.models[Model].materials['Material-matrice'].Plastic(table=((291.5, 
    0.0), ))
mdb.models[Model].materials['Material-sfere'].Plastic(table=((3450, 
    0.0), ))
mdb.models['Model-1'].materials['Material-sfere'].Expansion(table=((4e-06, ), 
    ))
mdb.models['Model-1'].materials['Material-matrice'].Expansion(table=((2.34e-05, 
    ), ))	
#Definizione section
mdb.models[Model].HomogeneousSolidSection(material='Material-sfere', name=
    'section-sfere', thickness=None)
mdb.models[Model].HomogeneousSolidSection(material='Material-matrice', 
    name='section-matrice', thickness=None)	
#Set e section sfere 
mdb.models[Model].parts['assieme-%s' %(numero_sfere-1)].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    cells=mdb.models[Model].parts['assieme-%s' %(numero_sfere-1)].cells.findAt(((0,0,0),), )), sectionName='section-matrice', thicknessAssignment=
    FROM_SECTION)

mdb.models[Model].parts['assieme-%s' %(numero_sfere-1)].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    cells=mdb.models[Model].parts['assieme-%s' %(numero_sfere-1)].cells.getByBoundingBox(.1,.1,.1,9.9,9.9,9.9)), sectionName='section-sfere', thicknessAssignment=
    FROM_SECTION)
	
mdb.models[Model].rootAssembly.Set(cells=
    mdb.models[Model].rootAssembly.instances['assieme-%s-1' %(numero_sfere-1)].cells.getByBoundingBox(-1,-1,-1,11,11,11), name='ASET')

#DUMMY	
mdb.models[Model].rootAssembly.Set(name='DUMMY-1', referencePoints=(
    mdb.models[Model].rootAssembly.instances['DUMMY-1-1'].referencePoints[1], 
    ))
mdb.models[Model].rootAssembly.Set(name='DUMMY-2', referencePoints=(
    mdb.models[Model].rootAssembly.instances['DUMMY-2-1'].referencePoints[1], 
    ))
mdb.models[Model].rootAssembly.Set(name='DUMMY-3', referencePoints=(
    mdb.models[Model].rootAssembly.instances['DUMMY-3-1'].referencePoints[1], 
    ))	
#Mesh
mdb.models[Model].parts['assieme-%s' %(numero_sfere-1)].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size= numero_seeds)

mdb.models[Model].parts['assieme-%s' %(numero_sfere-1)].setMeshControls(elemShape=TET, 
    regions=mdb.models[Model].parts['assieme-%s' %(numero_sfere-1)].cells.getByBoundingBox(-1,-1,-1,11,11,11), technique=FREE)
mdb.models[Model].parts['assieme-%s' %(numero_sfere-1)].setElementType(elemTypes=(ElemType(
    elemCode=C3D20R, elemLibrary=STANDARD), ElemType(elemCode=C3D15, 
    elemLibrary=STANDARD), ElemType(elemCode=C3D10, elemLibrary=STANDARD)), 
    regions=(
    mdb.models[Model].parts['assieme-%s' %(numero_sfere-1)].cells.getByBoundingBox(-1,-1,-1,11,11,11), ))
mdb.models[Model].parts['assieme-%s' %(numero_sfere-1)].generateMesh()

mdb.models[Model].StaticStep(name='Step-1', previous='Initial')

mdb.models[Model].parts.changeKey(fromName='assieme-%s' %(numero_sfere-1), toName='Part-1')
mdb.models[Model].rootAssembly.features.changeKey(fromName='assieme-%s-1' %(numero_sfere-1), 
    toName='Part-1-1')
mdb.models[Model].StaticStep(name='Step-1', previous='Initial')
mdb.models[Model].parts['Part-1'].Set(name='SETDISP', nodes=
    mdb.models[Model].parts['Part-1'].nodes.getByBoundingSphere((0,5,5),.05)+\
	mdb.models[Model].parts['Part-1'].nodes.getByBoundingSphere((10,5,5),.05))

#Field Output
mdb.models[Model].fieldOutputRequests['F-Output-1'].setValues(frequency=
    LAST_INCREMENT, variables=('S', 'PEMAG', 'U'))	
#Loads
mdb.models[Model].ConcentratedForce(cf1=30000, createStepName='Step-1', 
    distributionType=UNIFORM, field='', localCsys=None, name='P100', region=
    mdb.models[Model].rootAssembly.sets['DUMMY-1'])
#-----------------------------------------------------------------------------
mdb.models[Model].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
    distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name='X'
    , region=mdb.models[Model].rootAssembly.sets['DUMMY-1'], u1=UNSET,u2=0.0
    , u3=0.0, ur1=UNSET, ur2=UNSET, ur3=UNSET)
mdb.models[Model].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
    distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name='Y'
    , region=mdb.models[Model].rootAssembly.sets['DUMMY-2'], u1=0.0, u2=
    UNSET, u3=0.0, ur1=UNSET, ur2=UNSET, ur3=UNSET)

mdb.models[Model].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
    distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name='Z'
    , region=mdb.models[Model].rootAssembly.sets['DUMMY-3'], u1=0.0, u2=0.0
    , u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
mdb.models[Model].steps['Step-1'].setValues(initialInc=0.1, minInc=0.001)	
mdb.models[Model].rootAssembly.regenerate()
mdb.models[Model].steps['Step-1'].setValues(initialInc=0.7, noStop=OFF, 
    timeIncrementationMethod=FIXED)


mdb.models['Model-1'].Temperature(createStepName='Initial', 
    crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, distributionType=
    UNIFORM, magnitudes=(100.0, ), name='Temp', region=
    mdb.models['Model-1'].rootAssembly.sets['ASET'])
mdb.models[Model].rootAssembly.regenerate()
#PBC
execfile('PBC_Adaptive.py')
mdb.models['Model-1'].rootAssembly.regenerate()
mdb.models['Model-1'].StaticStep('LMM-Placeholder', 'Initial')
mdb.models['Model-1'].loads['P100'].move('Step-1', 'LMM-Placeholder')
mdb.models['Model-1'].predefinedFields['Temp'].move('Initial', 
    'LMM-Placeholder')
mdb.models['Model-1'].predefinedFields['Temp'].move('LMM-Placeholder', 
    'LMM-Placeholder')
mdb.models['Model-1'].boundaryConditions['X'].move('Step-1', 'LMM-Placeholder')
mdb.models['Model-1'].boundaryConditions['Y'].move('Step-1', 'LMM-Placeholder')
mdb.models['Model-1'].boundaryConditions['Z'].move('Step-1', 'LMM-Placeholder')
mdb.models['Model-1'].steps['Step-1'].suppress()
mdb.models['Model-1'].StaticStep('LMM-P100', 'Initial')
mdb.models['Model-1'].loads['P100'].move('LMM-Placeholder', 'LMM-P100')
mdb.models['Model-1'].StaticStep('LMM-Temp', 'LMM-P100')
mdb.models['Model-1'].predefinedFields['Temp'].move('LMM-Placeholder', 
    'LMM-Temp')
mdb.models['Model-1'].StaticStep('LMM-Null', 'LMM-Temp')
mdb.models['Model-1'].StaticStep('LMM-Shakedown', 'LMM-Null')
mdb.models['Model-1'].steps['LMM-Shakedown'].setValues(initialInc=1.0, maxInc=
    1.0, maxNumInc=300, minInc=1.0, timePeriod=300)
mdb.models['Model-1'].boundaryConditions['X'].move('LMM-Placeholder', 
    'LMM-P100')
mdb.models['Model-1'].boundaryConditions['Y'].move('LMM-Placeholder', 
    'LMM-P100')
mdb.models['Model-1'].boundaryConditions['Z'].move('LMM-Placeholder', 
    'LMM-P100')
mdb.models['Model-1'].loads['P100'].deactivate('LMM-Temp')
mdb.models['Model-1'].loads['P100'].deactivate('LMM-Null')
mdb.models['Model-1'].predefinedFields['Temp'].resetToInitial(stepName=
    'LMM-Null')
mdb.models['Model-1'].loads['P100'].deactivate('LMM-Shakedown')
mdb.models['Model-1'].predefinedFields['Temp'].resetToInitial(stepName=
    'LMM-Shakedown')
mdb.models['Model-1'].loads['P100'].deactivate('LMM-Placeholder')
mdb.models['Model-1'].predefinedFields['Temp'].resetToInitial(stepName=
    'LMM-Placeholder')
del mdb.models['Model-1'].steps['LMM-Placeholder']
mdb.models['Model-1'].Material(name='Material-matrice-Original', objectToCopy=
    mdb.models['Model-1'].materials['Material-matrice'])
mdb.models['Model-1'].Material(name='Material-sfere-Original', objectToCopy=
    mdb.models['Model-1'].materials['Material-sfere'])
del mdb.models['Model-1'].materials['Material-matrice'].elastic
del mdb.models['Model-1'].materials['Material-matrice'].plastic
del mdb.models['Model-1'].materials['Material-matrice'].creep
mdb.models['Model-1'].materials['Material-matrice'].UserMaterial(
    mechanicalConstants=(68900.0, 0.3, 291.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
mdb.models['Model-1'].materials['Material-matrice'].Expansion(table=((2.34e-05, 
    ), ))
mdb.models['Model-1'].materials['Material-matrice'].Depvar(n=41)
del mdb.models['Model-1'].materials['Material-sfere'].elastic
del mdb.models['Model-1'].materials['Material-sfere'].plastic
del mdb.models['Model-1'].materials['Material-sfere'].creep
mdb.models['Model-1'].materials['Material-sfere'].UserMaterial(
    mechanicalConstants=(380000.0, 0.19, 3450.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
mdb.models['Model-1'].materials['Material-sfere'].Expansion(table=((4e-06, ), 
    ))
mdb.models['Model-1'].materials['Material-sfere'].Depvar(n=41)
mdb.models['Model-1'].FieldOutputRequest(createStepName='LMM-P100', frequency=1
    , name='LMM-Outputs', variables=('S', 'E', 'U', 'NT'))
mdb.models['Model-1'].fieldOutputRequests['LMM-Outputs'].setValuesInStep(
    stepName='LMM-Null', variables=('SDV', 'S', 'E', 'U', 'NT'))
mdb.models['Model-1'].fieldOutputRequests['LMM-Outputs'].setValuesInStep(
    stepName='LMM-Shakedown', variables=('SDV', ))
mdb.models['Model-1'].HistoryOutputRequest(createStepName='LMM-P100', 
    frequency=LAST_INCREMENT, name='LMM-H_output', variables=('ETOTAL', ))
mdb.models['Model-1'].keywordBlock.setValues(edited=False)
mdb.models['Model-1'].keywordBlock.synchVersions(storeNodesAndElements=False)
mdb.models['Model-1'].keywordBlock.insert(11928, '*NODE PRINT, FREQUENCY=0')
mdb.models['Model-1'].keywordBlock.insert(11929, '*EL PRINT, FREQUENCY=0')
mdb.models['Model-1'].keywordBlock.insert(11930, '*ENERGY FILE')
mdb.models['Model-1'].keywordBlock.insert(11931, 
    '*EL FILE, POSITION=INTEGRATION POINTS')
mdb.Job(model='Model-1', name='M1-LL', userSubroutine=
    'C:\\SIMULIA\\Abaqus\\LMM\\LMM_Shakedown_Multi_Process.obj')
mdb.jobs['M1-LL'].setValues(multiprocessingMode=THREADS, numCpus=7, numDomains=7)
mdb.jobs['M1-LL'].submit(consistencyChecking=OFF)
mdb.jobs['M1-LL'].waitForCompletion()