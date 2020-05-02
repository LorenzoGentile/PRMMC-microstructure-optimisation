import numpy as np
# PBC
numero_seeds=0.5
Radius=0.05
i0=np.arange(numero_seeds,10,numero_seeds)
Points=int((10/numero_seeds)-1)
	
#Vertices
mdb.models['Model-1'].parts['Part-1'].Set(name='v-1', nodes=
	mdb.models['Model-1'].parts['Part-1'].nodes.getByBoundingSphere((0,0,0),Radius))
mdb.models['Model-1'].parts['Part-1'].Set(name='v-2', nodes=
	mdb.models['Model-1'].parts['Part-1'].nodes.getByBoundingSphere((10,0,0),Radius))	
mdb.models['Model-1'].parts['Part-1'].Set(name='v-3', nodes=
	mdb.models['Model-1'].parts['Part-1'].nodes.getByBoundingSphere((0,10,0),Radius))	
mdb.models['Model-1'].parts['Part-1'].Set(name='v-4', nodes=
	mdb.models['Model-1'].parts['Part-1'].nodes.getByBoundingSphere((10,10,0),Radius))	
mdb.models['Model-1'].parts['Part-1'].Set(name='v-5', nodes=
	mdb.models['Model-1'].parts['Part-1'].nodes.getByBoundingSphere((0,0,10),Radius))	
mdb.models['Model-1'].parts['Part-1'].Set(name='v-6', nodes=
	mdb.models['Model-1'].parts['Part-1'].nodes.getByBoundingSphere((10,0,10),Radius))	
mdb.models['Model-1'].parts['Part-1'].Set(name='v-7', nodes=
	mdb.models['Model-1'].parts['Part-1'].nodes.getByBoundingSphere((0,10,10),Radius))		
mdb.models['Model-1'].parts['Part-1'].Set(name='v-8', nodes=
	mdb.models['Model-1'].parts['Part-1'].nodes.getByBoundingSphere((10,10,10),Radius))
	
	 
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

for i in range(0,Points):

	for ii in range(0,Points):
	# L e R
		mdb.models['Model-1'].parts['Part-1'].Set(name='l-%s-%s'%(i,ii), nodes=
			mdb.models['Model-1'].parts['Part-1'].nodes.getByBoundingSphere((0,i0[ii],i0[i]),Radius))
		mdb.models['Model-1'].parts['Part-1'].Set(name='r-%s-%s'%(i,ii), nodes=
			mdb.models['Model-1'].parts['Part-1'].nodes.getByBoundingSphere((10,i0[ii],i0[i]),Radius))
	# B	T 	
		mdb.models['Model-1'].parts['Part-1'].Set(name='b-%s-%s'%(i,ii), nodes=
			mdb.models['Model-1'].parts['Part-1'].nodes.getByBoundingSphere((i0[ii],i0[i],0),Radius))
		mdb.models['Model-1'].parts['Part-1'].Set(name='t-%s-%s'%(i,ii), nodes=
			mdb.models['Model-1'].parts['Part-1'].nodes.getByBoundingSphere((i0[ii],i0[i],10),Radius))	
	# F e R	
		mdb.models['Model-1'].parts['Part-1'].Set(name='f-%s-%s'%(i,ii), nodes=
			mdb.models['Model-1'].parts['Part-1'].nodes.getByBoundingSphere((i0[ii],0,i0[i]),Radius))
		mdb.models['Model-1'].parts['Part-1'].Set(name='re-%s-%s'%(i,ii), nodes=
			mdb.models['Model-1'].parts['Part-1'].nodes.getByBoundingSphere((i0[ii],10,i0[i]),Radius))	
		for n in range (1,4):	
			mdb.models['Model-1'].Equation(name='Yfaces-%s-%s-%s'%(n,i,ii), terms=((-1.0, 'Part-1-1.re-%s-%s'%(i,ii), n), (
				1.0, 'Part-1-1.f-%s-%s'%(i,ii), n), (1.0, 'DUMMY-2', n)))
			mdb.models['Model-1'].Equation(name='Zfaces-%s-%s-%s'%(n,i,ii), terms=((-1.0, 'Part-1-1.t-%s-%s'%(i,ii), n), (
				1.0, 'Part-1-1.b-%s-%s'%(i,ii), n), (1.0, 'DUMMY-3', n)))
			mdb.models['Model-1'].Equation(name='Xfaces-%s-%s-%s'%(n,i,ii), terms=((-1.0, 'Part-1-1.r-%s-%s'%(i,ii), n), (
				1.0, 'Part-1-1.l-%s-%s'%(i,ii), n), (1.0, 'DUMMY-1', n)))
		
			
	# Edges
# X
	mdb.models['Model-1'].parts['Part-1'].Set(name='E-12-%s'%(i), nodes=
		mdb.models['Model-1'].parts['Part-1'].nodes.getByBoundingSphere((i0[i],0,0),Radius)) 
	mdb.models['Model-1'].parts['Part-1'].Set(name='E-56-%s'%(i), nodes=
		mdb.models['Model-1'].parts['Part-1'].nodes.getByBoundingSphere((i0[i],0,10),Radius))
	mdb.models['Model-1'].parts['Part-1'].Set(name='E-34-%s'%(i), nodes=
		mdb.models['Model-1'].parts['Part-1'].nodes.getByBoundingSphere((i0[i],10,0),Radius))		
	mdb.models['Model-1'].parts['Part-1'].Set(name='E-78-%s'%(i), nodes=
		mdb.models['Model-1'].parts['Part-1'].nodes.getByBoundingSphere((i0[i],10,10),Radius))
	
# Y	
	mdb.models['Model-1'].parts['Part-1'].Set(name='E-13-%s'%(i), nodes=
		mdb.models['Model-1'].parts['Part-1'].nodes.getByBoundingSphere((0,i0[i],0),Radius))
	mdb.models['Model-1'].parts['Part-1'].Set(name='E-57-%s'%(i), nodes=
		mdb.models['Model-1'].parts['Part-1'].nodes.getByBoundingSphere((0,i0[i],10),Radius))
	mdb.models['Model-1'].parts['Part-1'].Set(name='E-24-%s'%(i), nodes=
		mdb.models['Model-1'].parts['Part-1'].nodes.getByBoundingSphere((10,i0[i],0),Radius))
	mdb.models['Model-1'].parts['Part-1'].Set(name='E-68-%s'%(i), nodes=
		mdb.models['Model-1'].parts['Part-1'].nodes.getByBoundingSphere((10,i0[i],10),Radius))
# Z
	mdb.models['Model-1'].parts['Part-1'].Set(name='E-15-%s'%(i), nodes=
		mdb.models['Model-1'].parts['Part-1'].nodes.getByBoundingSphere((0,0,i0[i]),Radius))
	mdb.models['Model-1'].parts['Part-1'].Set(name='E-26-%s'%(i), nodes=
		mdb.models['Model-1'].parts['Part-1'].nodes.getByBoundingSphere((10,0,i0[i]),Radius))
	mdb.models['Model-1'].parts['Part-1'].Set(name='E-37-%s'%(i), nodes=
		mdb.models['Model-1'].parts['Part-1'].nodes.getByBoundingSphere((0,10,i0[i]),Radius))
	mdb.models['Model-1'].parts['Part-1'].Set(name='E-48-%s'%(i), nodes=
		mdb.models['Model-1'].parts['Part-1'].nodes.getByBoundingSphere((10,10,i0[i]),Radius))
	

	
	for n in range (1,4):	
	
	# X
		mdb.models['Model-1'].Equation(name='X1-%s-%s'%(n,i), terms=((-1.0, 'Part-1-1.E-34-%s'%(i), n), (
		+1.0, 'Part-1-1.E-12-%s'%(i), n), (1.0, 'DUMMY-2', n)))
		
		
		mdb.models['Model-1'].Equation(name='X2-%s-%s'%(n,i), terms=((1.0, 'Part-1-1.E-56-%s'%(i), n), (
		-1.0, 'Part-1-1.E-78-%s'%(i), n), (1.0, 'DUMMY-2', n)))


		mdb.models['Model-1'].Equation(name='X3-%s-%s'%(n,i), terms=((1.0, 'Part-1-1.E-12-%s'%(i), n), (
		-1.0, 'Part-1-1.E-56-%s'%(i), n), (1.0, 'DUMMY-3', n)))
		 
	# Y
		mdb.models['Model-1'].Equation(name='Y1-%s-%s'%(n,i), terms=((-1.0, 'Part-1-1.E-24-%s'%(i), n), (
		1.0, 'Part-1-1.E-13-%s'%(i), n), (1.0, 'DUMMY-1', n)))

		 
		mdb.models['Model-1'].Equation(name='Y2-%s-%s'%(n,i), terms=((1.0, 'Part-1-1.E-57-%s'%(i), n), (
		-1.0, 'Part-1-1.E-68-%s'%(i), n), (1.0, 'DUMMY-1', n)))
		
		
		mdb.models['Model-1'].Equation(name='Y3-%s-%s'%(n,i), terms=((1.0, 'Part-1-1.E-13-%s'%(i), n), (
		-1.0, 'Part-1-1.E-57-%s'%(i), n), (1.0, 'DUMMY-3', n)))
		
	# Z
		mdb.models['Model-1'].Equation(name='Z1-%s-%s'%(n,i), terms=((-1.0, 'Part-1-1.E-26-%s'%(i), n), (
		1.0, 'Part-1-1.E-15-%s'%(i), n), (1.0, 'DUMMY-1', n)))
		
		
		mdb.models['Model-1'].Equation(name='Z2-%s-%s'%(n,i), terms=((1.0, 'Part-1-1.E-37-%s'%(i), n), (
		-1.0, 'Part-1-1.E-48-%s'%(i), n), (1.0, 'DUMMY-1', n)))

		
		mdb.models['Model-1'].Equation(name='Z3-%s-%s'%(n,i), terms=((1.0, 'Part-1-1.E-15-%s'%(i), n), (
		-1.0, 'Part-1-1.E-37-%s'%(i), n), (1.0, 'DUMMY-2', n)))
	