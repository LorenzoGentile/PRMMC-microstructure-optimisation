#Inputs
Tol=0.02
Radius=0.1
Radius_in=0.021
Inc_down=0.01
Inc_up=0.001
myPart=mdb.models['Model-1'].parts['Part-1']
myInstances=mdb.models['Model-1'].rootAssembly.instances['Part-1-1']

#Vertices
myPart.Set(name='v-1', nodes=
	myPart.nodes.getByBoundingSphere((0,0,0),Radius))
myPart.Set(name='v-2', nodes=
	myPart.nodes.getByBoundingSphere((10,0,0),Radius))	
myPart.Set(name='v-3', nodes=
	myPart.nodes.getByBoundingSphere((0,10,0),Radius))	
myPart.Set(name='v-4', nodes=
	myPart.nodes.getByBoundingSphere((10,10,0),Radius))	
myPart.Set(name='v-5', nodes=
	myPart.nodes.getByBoundingSphere((0,0,10),Radius))	
myPart.Set(name='v-6', nodes=
	myPart.nodes.getByBoundingSphere((10,0,10),Radius))	
myPart.Set(name='v-7', nodes=
	myPart.nodes.getByBoundingSphere((0,10,10),Radius))		
myPart.Set(name='v-8', nodes=
	myPart.nodes.getByBoundingSphere((10,10,10),Radius))
#Equations on the Vertices	
for n in range (1,4):
	mdb.models['Model-1'].Equation(name='v-%s-12'%(n), terms=((1.0, 'Part-1-1.v-1', n), (-1.0, 'Part-1-1.v-2', 
		n), (1.0, 'DUMMY-1',n)))
	mdb.models['Model-1'].Equation(name='v-%s-24'%(n), terms=((1.0, 'Part-1-1.v-2', n), (-1.0, 'Part-1-1.v-4', 
		n), (1.0, 'DUMMY-2', n)))
	mdb.models['Model-1'].Equation(name='v-%s-43'%(n), terms=((-1.0, 'Part-1-1.v-4',n), (1.0, 
		'Part-1-1.v-3', n), (1.0, 'DUMMY-1', n)))
	mdb.models['Model-1'].Equation(name='v-%s-65'%(n), terms=((-1.0, 'Part-1-1.v-6', n), (1.0, 'Part-1-1.v-5', 
		n), (1.0, 'DUMMY-1', n)))
	mdb.models['Model-1'].Equation(name='v-%s-86'%(n), terms=((-1.0, 'Part-1-1.v-8', n), (1.0, 
		'Part-1-1.v-6', n), (1.0, 'DUMMY-2', n)))
	mdb.models['Model-1'].Equation(name='v-%s-78'%(n), terms=((1.0, 'Part-1-1.v-7', n), (-1.0, 
		'Part-1-1.v-8', n), (1.0, 'DUMMY-1', n)))
	mdb.models['Model-1'].Equation(name='v-%s-51'%(n), terms=((-1.0, 'Part-1-1.v-5', n), (1.0, 'Part-1-1.v-1', 
		n), (1.0, 'DUMMY-3', n)))

#Reference Sets			
myPart.Set(name='Edge-1', nodes=
	myPart.nodes. getByBoundingCylinder((Tol,0,0),(10-Tol,0,0),Tol))
myPart.Set(name='Edge-2', nodes=
	myPart.nodes.getByBoundingCylinder((0,Tol,0),(0,10-Tol,0),Tol))
myPart.Set(name='Edge-3', nodes=
	myPart.nodes.getByBoundingCylinder((0,0,Tol),(0,0,10-Tol),Tol))
#-------------------------------------------------------------------	
myPart.Set(name='Face-1', nodes=
	myPart.nodes.getByBoundingBox(Tol,Tol,-Tol,10-Tol,10-Tol,Tol))
myPart.Set(name='Face-2', nodes=
	myPart.nodes.getByBoundingBox(-Tol,Tol,Tol,Tol,10-Tol,10-Tol))
myPart.Set(name='Face-3', nodes=
	myPart.nodes.getByBoundingBox(Tol,-Tol,Tol,10-Tol,Tol,10-Tol))

#Edges 1-1,1-2,1-3,1-4 single node sets	
for i in range( 0,len(myInstances.sets['Edge-1'].nodes)):
	
	Radius=Radius_in
	flag=1		
	
	while flag==1:		
		myPart.Set(name='E-12-%s'% i, nodes=
			myPart.nodes.getByBoundingSphere((
			myInstances.sets['Edge-1'].nodes[i].coordinates),Radius))
		if len((myInstances.sets['E-12-%s'% i].nodes))>1 :
				del myPart.sets['E-12-%s'% i]
				Radius= Radius-Inc_down	
		elif len((myInstances.sets['E-12-%s'% i].nodes))==0 :
				del myPart.sets['E-12-%s'% i]
				Radius= Radius+Inc_up					
		else :
			flag=0			
	Radius=Radius_in
	flag=1		
	
	while flag==1:				
		myPart.Set(name='E-56-%s'% i , nodes=
			myPart.nodes.getByBoundingCylinder((		
			myInstances.sets['Edge-1'].nodes[i].coordinates[0],0,10-Tol),(		
			myInstances.sets['Edge-1'].nodes[i].coordinates[0],0,10+Tol),Radius))
		if len((myInstances.sets['E-56-%s'% i ].nodes))>1 :
				del myPart.sets['E-56-%s'% i ]
				Radius= Radius-Inc_down	
		elif len((myInstances.sets['E-56-%s'% i ].nodes))==0 :
				del myPart.sets['E-56-%s'% i ]
				Radius= Radius+Inc_up					
		else :
			flag=0				
		
	Radius=Radius_in
	flag=1		
	
	while flag==1:			
		myPart.Set(name='E-34-%s'% i , nodes=
			myPart.nodes.getByBoundingCylinder((		
			myInstances.sets['Edge-1'].nodes[i].coordinates[0],10-Tol,0),(		
			myInstances.sets['Edge-1'].nodes[i].coordinates[0],10+Tol,0),Radius))
		if len((myInstances.sets['E-34-%s'% i ].nodes))>1 :
				del myPart.sets['E-34-%s'% i ]
				Radius= Radius-Inc_down	
		elif len((myInstances.sets['E-34-%s'% i ].nodes))==0 :
				del myPart.sets['E-34-%s'% i ]
				Radius= Radius+Inc_up					
		else :
			flag=0
			flag=0				
	Radius=Radius_in
	flag=1		
	
	while flag==1:				
		myPart.Set(name='E-78-%s'% i , nodes=
			myPart.nodes.getByBoundingCylinder((		
			myInstances.sets['Edge-1'].nodes[i].coordinates[0],10,10-Tol),(		
			myInstances.sets['Edge-1'].nodes[i].coordinates[0],10,10+Tol),Radius))
		if len((myInstances.sets['E-78-%s'% i ].nodes))>1 :
				del myPart.sets['E-78-%s'% i ]
				Radius= Radius-Inc_down	
		elif len((myInstances.sets['E-78-%s'% i ].nodes))==0 :
				del myPart.sets['E-78-%s'% i ]
				Radius= Radius+Inc_up					
		else :
			flag=0
#Equations on the Edges 1-1,1-2,1-3,1-4
     # X
	for n in range (1,4): 
		mdb.models['Model-1'].Equation(name='X1-%s-%s'%(n,i), terms=((-1.0, 'Part-1-1.E-34-%s'%(i), n), (
		+1.0, 'Part-1-1.E-12-%s'%(i), n), (1.0, 'DUMMY-2', n)))
		mdb.models['Model-1'].Equation(name='X2-%s-%s'%(n,i), terms=((1.0, 'Part-1-1.E-56-%s'%(i), n), (
		-1.0, 'Part-1-1.E-78-%s'%(i), n), (1.0, 'DUMMY-2', n)))
		mdb.models['Model-1'].Equation(name='X3-%s-%s'%(n,i), terms=((1.0, 'Part-1-1.E-12-%s'%(i), n), (
		-1.0, 'Part-1-1.E-56-%s'%(i), n), (1.0, 'DUMMY-3', n)))
		
#Edges 2-1,2-2,2-3,2-4 single node sets	
for i in range( 0,len(myInstances.sets['Edge-2'].nodes)):
	Radius=Radius_in
	flag=1		
	
	while flag==1:				
		myPart.Set(name='E-13-%s'% i , nodes=
			myPart.nodes.getByBoundingSphere((
			myInstances.sets['Edge-2'].nodes[i].coordinates),Radius))
		if len((myInstances.sets['E-13-%s'% i ].nodes))>1 :
				del myPart.sets['E-13-%s'% i ]
				Radius= Radius-Inc_down	
		elif len((myInstances.sets['E-13-%s'% i ].nodes))==0 :
				del myPart.sets['E-13-%s'% i ]
				Radius= Radius+Inc_up					
		else :
			flag=0	
	Radius=Radius_in
	flag=1		
	
	while flag==1:				
		myPart.Set(name='E-24-%s'% i , nodes=
			myPart.nodes.getByBoundingCylinder((10-Tol	,	
			myInstances.sets['Edge-2'].nodes[i].coordinates[1],0),(10+Tol	,	
			myInstances.sets['Edge-2'].nodes[i].coordinates[1],0),Radius))
		if len((myInstances.sets['E-24-%s'% i ].nodes))>1 :
				del myPart.sets['E-24-%s'% i ]
				Radius= Radius-Inc_down	
		elif len((myInstances.sets['E-24-%s'% i ].nodes))==0 :
				del myPart.sets['E-24-%s'% i ]
				Radius= Radius+Inc_up					
		else :
			flag=0		
	Radius=Radius_in
	flag=1		
	
	while flag==1:				
		myPart.Set(name='E-57-%s'% i , nodes=
			myPart.nodes.getByBoundingCylinder((0,		
			myInstances.sets['Edge-2'].nodes[i].coordinates[1],10-Tol),(0,		
			myInstances.sets['Edge-2'].nodes[i].coordinates[1],10+Tol),Radius))
		if len((myInstances.sets['E-57-%s'% i ].nodes))>1 :
				del myPart.sets['E-57-%s'% i ]
				Radius= Radius-Inc_down	
		elif len((myInstances.sets['E-57-%s'% i ].nodes))==0 :
				del myPart.sets['E-57-%s'% i ]
				Radius= Radius+Inc_up					
		else :
			flag=0				
	Radius=Radius_in
	flag=1		
	
	while flag==1:				
		myPart.Set(name='E-68-%s'% i , nodes=
			myPart.nodes.getByBoundingCylinder((10,	
			myInstances.sets['Edge-2'].nodes[i].coordinates[1],10-Tol),(10,	
			myInstances.sets['Edge-2'].nodes[i].coordinates[1],10+Tol),Radius))
		if len((myInstances.sets['E-68-%s'% i ].nodes))>1 :
				del myPart.sets['E-68-%s'% i ]
				Radius= Radius-Inc_down	
		elif len((myInstances.sets['E-68-%s'% i ].nodes))==0 :
				del myPart.sets['E-68-%s'% i ]
				Radius= Radius+Inc_up					
		else :
			flag=0
#Equations on the Edges 2-1,2-2,2-3,2-4
     # Y
	for n in range (1,4):
		mdb.models['Model-1'].Equation(name='Y1-%s-%s'%(n,i), terms=((-1.0, 'Part-1-1.E-24-%s'%(i), n), (
		1.0, 'Part-1-1.E-13-%s'%(i), n), (1.0, 'DUMMY-1', n)))
		mdb.models['Model-1'].Equation(name='Y2-%s-%s'%(n,i), terms=((1.0, 'Part-1-1.E-57-%s'%(i), n), (
		-1.0, 'Part-1-1.E-68-%s'%(i), n), (1.0, 'DUMMY-1', n)))
		mdb.models['Model-1'].Equation(name='Y3-%s-%s'%(n,i), terms=((1.0, 'Part-1-1.E-13-%s'%(i), n), (
		-1.0, 'Part-1-1.E-57-%s'%(i), n), (1.0, 'DUMMY-3', n)))
		
#Edges 3-1,3-2,3-3,3-4 single node sets				
for i in range( 0,len(myInstances.sets['Edge-3'].nodes)):
	Radius=Radius_in
	flag=1		
	
	while flag==1:				
		myPart.Set(name='E-15-%s'% i , nodes=
			myPart.nodes.getByBoundingSphere((
			myInstances.sets['Edge-3'].nodes[i].coordinates),Radius))
		if len((myInstances.sets['E-15-%s'% i ].nodes))>1 :
				del myPart.sets['E-15-%s'% i ]
				Radius= Radius-Inc_down	
		elif len((myInstances.sets['E-15-%s'% i ].nodes))==0 :
				del myPart.sets['E-15-%s'% i ]
				Radius= Radius+Inc_up					
		else :
			flag=0		
	Radius=Radius_in
	flag=1	
	while flag==1:				
			
		myPart.Set(name='E-26-%s'% i , nodes=
			myPart.nodes.getByBoundingCylinder((10-Tol,0,		
			myInstances.sets['Edge-3'].nodes[i].coordinates[2]),(10+Tol,0,		
			myInstances.sets['Edge-3'].nodes[i].coordinates[2]),Radius))
		if len((myInstances.sets['E-26-%s'% i ].nodes))>1 :
				del myPart.sets['E-26-%s'% i ]
				Radius= Radius-Inc_down	
		elif len((myInstances.sets['E-26-%s'% i ].nodes))==0 :
				del myPart.sets['E-26-%s'% i ]
				Radius= Radius+Inc_up					
		else :
			flag=0				
	Radius=Radius_in
	flag=1		
	
	while flag==1:				
		myPart.Set(name='E-37-%s'% i , nodes=
			myPart.nodes.getByBoundingCylinder((0,10-Tol,	
			myInstances.sets['Edge-3'].nodes[i].coordinates[2]),(0,10+Tol,	
			myInstances.sets['Edge-3'].nodes[i].coordinates[2]),Radius))
		if len((myInstances.sets['E-37-%s'% i ].nodes))>1 :
				del myPart.sets['E-37-%s'% i ]
				Radius= Radius-Inc_down	
		elif len((myInstances.sets['E-37-%s'% i ].nodes))==0 :
				del myPart.sets['E-37-%s'% i ]
				Radius= Radius+Inc_up					
		else :
			flag=0			
	Radius=Radius_in
	flag=1		
	
	while flag==1:				
		myPart.Set(name='E-48-%s'% i , nodes=
			myPart.nodes.getByBoundingCylinder((10,10-Tol,	
			myInstances.sets['Edge-3'].nodes[i].coordinates[2]),(10,10+Tol,	
			myInstances.sets['Edge-3'].nodes[i].coordinates[2]),Radius))	
		if len((myInstances.sets['E-48-%s'% i ].nodes))>1 :
				del myPart.sets['E-48-%s'% i ]
				Radius= Radius-Inc_down	
		elif len((myInstances.sets['E-48-%s'% i].nodes))==0 :
				del myPart.sets['E-48-%s'% i ]
				Radius= Radius+Inc_up					
		else :
			flag=0
#Equations on the Edges 3-1,3-2,3-3,3-4
	 # Z
	for n in range (1,4):
		mdb.models['Model-1'].Equation(name='Z1-%s-%s'%(n,i), terms=((-1.0, 'Part-1-1.E-26-%s'%(i), n), (
		1.0, 'Part-1-1.E-15-%s'%(i), n), (1.0, 'DUMMY-1', n)))
		mdb.models['Model-1'].Equation(name='Z2-%s-%s'%(n,i), terms=((1.0, 'Part-1-1.E-37-%s'%(i), n), (
		-1.0, 'Part-1-1.E-48-%s'%(i), n), (1.0, 'DUMMY-1', n)))
		mdb.models['Model-1'].Equation(name='Z3-%s-%s'%(n,i), terms=((1.0, 'Part-1-1.E-15-%s'%(i), n), (
		-1.0, 'Part-1-1.E-37-%s'%(i), n), (1.0, 'DUMMY-2', n)))	
		
#Faces 1-1,1-2	single node sets			
for i in range( 0,len(myInstances.sets['Face-1'].nodes)):
	Radius=Radius_in
	flag=1		
	
	while flag==1:			
		myPart.Set(name='b-%s'% i , nodes=
			myPart.nodes.getByBoundingSphere((
			myInstances.sets['Face-1'].nodes[i].coordinates),Radius))
		if len((myInstances.sets['b-%s'% i].nodes))>1 :
				del myPart.sets['b-%s'% i]
				Radius= Radius-Inc_down	
		elif len((myInstances.sets['b-%s'% i].nodes))==0 :
				del myPart.sets['b-%s'% i]
				Radius= Radius+Inc_up					
		else :
			flag=0	
	Radius=Radius_in			
	flag=1		
	
	while flag==1:		
		myPart.Set(name='t-%s'% i , nodes=
			myPart.nodes.getByBoundingCylinder((myInstances.sets['Face-1'].nodes[i].coordinates[0],		
			myInstances.sets['Face-1'].nodes[i].coordinates[1],10-Tol),(myInstances.sets['Face-1'].nodes[i].coordinates[0],		
			myInstances.sets['Face-1'].nodes[i].coordinates[1],10+Tol),Radius))
		if len((myInstances.sets['t-%s'% i ].nodes))>1 :
				del myPart.sets['t-%s'% i]
				Radius= Radius-Inc_down		
		elif len((myInstances.sets['t-%s'% i].nodes))==0 :
				del myPart.sets['t-%s'% i]
				Radius= Radius+Inc_up		
		else :
			flag=0	
#Equations on the Faces 1-1,1-2
	for n in range (1,4):
		mdb.models['Model-1'].Equation(name='Zfaces-%s-%s'%(i,n), terms=((-1.0, 'Part-1-1.t-%s'%i, n), (
		1.0, 'Part-1-1.b-%s'%i, n), (1.0, 'DUMMY-3', n)))
		
#Faces 2-1,2-2	single node sets
for i in range( 0,len(myInstances.sets['Face-2'].nodes)):
	Radius=Radius_in
	flag=1		
	while flag==1:	
	
		myPart.Set(name='l-%s'% i , nodes=
			myPart.nodes.getByBoundingSphere((
			myInstances.sets['Face-2'].nodes[i].coordinates),Radius))
		if len((myInstances.sets['l-%s'% i ].nodes))>1 :
				del myPart.sets['l-%s'% i]
				Radius= Radius-Inc_down		
		elif len((myInstances.sets['l-%s'% i].nodes))==0 :
				del myPart.sets['l-%s'% i]
				Radius= Radius+Inc_up
		else :
			flag=0		
	Radius=Radius_in			
	flag=1		
	
	while flag==1:		
		myPart.Set(name='r-%s'% i , nodes=
			myPart.nodes.getByBoundingCylinder((10-Tol,	myInstances.sets['Face-2'].nodes[i].coordinates[1],
			myInstances.sets['Face-2'].nodes[i].coordinates[2]	),(10+Tol,myInstances.sets['Face-2'].nodes[i].coordinates[1],
			myInstances.sets['Face-2'].nodes[i].coordinates[2]	),Radius))
		if len((myInstances.sets['r-%s'% i ].nodes))>1 :
				del myPart.sets['r-%s'% i]
				Radius= Radius-Inc_down		
		elif len((myInstances.sets['r-%s'% i].nodes))==0 :
				del myPart.sets['r-%s'% i]
				Radius= Radius+Inc_up		
		else :
			flag=0		
#Equations on the Faces 2-1,2-2	
	for n in range (1,4):		
		mdb.models['Model-1'].Equation(name='Xfaces-%s-%s'%(i,n), terms=((-1.0, 'Part-1-1.r-%s'%i, n), (
		1.0, 'Part-1-1.l-%s'%i, n), (1.0, 'DUMMY-1', n)))
		
#Faces 3-1,3-2	single node sets
for i in range( 0,len(myInstances.sets['Face-3'].nodes)):
	Radius=Radius_in
	flag=1	
	
	while flag==1:		
		myPart.Set(name='f-%s'% i , nodes=
			myPart.nodes.getByBoundingSphere((
			myInstances.sets['Face-3'].nodes[i].coordinates),Radius))
		if len((myInstances.sets['f-%s'% i  ].nodes))>1 :
				del myPart.sets['f-%s'% i]
				Radius= Radius-Inc_down		
		elif len((myInstances.sets['f-%s'% i].nodes))==0 :
				del myPart.sets['f-%s'% i]
				Radius= Radius+Inc_up
		else :
			flag=0	
	Radius=Radius_in					
	flag=1		
	
	while flag==1:		
		myPart.Set(name='re-%s'% i , nodes=
			myPart.nodes.getByBoundingCylinder((myInstances.sets['Face-3'].nodes[i].coordinates[0],10-Tol,		
			myInstances.sets['Face-3'].nodes[i].coordinates[2]),(myInstances.sets['Face-3'].nodes[i].coordinates[0],10+Tol,		
			myInstances.sets['Face-3'].nodes[i].coordinates[2]),Radius))
		if len((myInstances.sets['re-%s'% i ].nodes))>1 :
				del myPart.sets['re-%s'% i]
				Radius= Radius-Inc_down
		elif len((myInstances.sets['re-%s'% i].nodes))==0 :
				del myPart.sets['re-%s'% i]
				Radius= Radius+Inc_up
		else :
			flag=0
#Equations on the Faces 3-1,3-2	
	for n in range (1,4):		
		mdb.models['Model-1'].Equation(name='Yfaces-%s-%s'%(i,n), terms=((-1.0, 'Part-1-1.re-%s'%i, n), (
		1.0, 'Part-1-1.f-%s'%i, n), (1.0, 'DUMMY-2', n)))			