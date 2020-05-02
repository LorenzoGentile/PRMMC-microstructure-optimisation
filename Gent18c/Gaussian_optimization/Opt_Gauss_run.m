global N_part;
global Volume ;
global Vf;
global delta;
global N_analisi;
N_analisi=1;
Vf=.1;
delta=.1;
Volume =1000;
N_part=10;
pop=60;
intcon=1;
LB=[0,0,0,1,1,1];          %3*standard deviation 3*number of gaussians 
UB=[30,30,30,6,6,6];
X = lhsdesign(pop,N_var);
XX=(X(:,:).*(UB-LB)+LB);
XX=round(XX);
g_options =gaoptimset('NonlinConAlgorithm','penalty','InitialPopulation',XX,'EliteCount',5,'TolCon',1e-4,'PopulationSize',...
pop,'PlotFcn', {@Lorenzo_plot,@gaplotchange,@gaplotbestf,@gaplotscorediversity,@gaplotselection},'Generations',20,'Display','iter');

[x,FVAL]=ga(@Objective_function,N_var,[],[],[],[],LB,UB,@nonlcon_ga,[1,2,3,4,5,6],g_options);
