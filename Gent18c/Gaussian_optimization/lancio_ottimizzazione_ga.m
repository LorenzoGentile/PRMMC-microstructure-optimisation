
global N_part;
global Volume ;
global Vf;
global delta;
global N_analisi;
clear all;
list=[2,3,4,5,6,8];
volumes=[0.1,.15,.2];
for V=1:size(volumes,2)
    for N=1:size(list,2)
        N_analisi=1;
        delta=.1;
        Volume =1000;
        Vf=volumes(V); 
        N_part=list(N);
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
        filename=sprintf('WSpart%d-Vf%d.mat',N_part,Vf);
        save(filename,'FVAL','x','N_part','Vf')
    end
end