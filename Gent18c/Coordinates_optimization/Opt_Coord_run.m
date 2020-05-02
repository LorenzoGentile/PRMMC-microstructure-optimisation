clear all;
list=[2,3,4,5,6,8];
volumes=[0.1,.15,.2];
for V=1:size(volumes,2)
    for N=1:size(list,2)
        
        global delta;
        global r;
        global N_part;
        global Volume;
        global Vf;
        global UB;
        global LB;
        % Calculation of sphere radius
        x_min=0;
        x_max=10;
        y_min=0;
        y_max=10;
        z_min=0;
        z_max=10;
        Vf=volumes(V); 
        N_part=list(N);
        Volume=(x_max-x_min)*(y_max-y_min)*(z_max-z_min);
        latin=10;
        r=(Volume*Vf*3/(4*pi*N_part))^(1/3);
        delta=.2;
        N_var=3*N_part;
        LB(1,1:N_var)=r+delta;
        UB(1,1:N_var)=10-(r+delta);
        %% Latin hypercube
        XX=Creation_fun_LG(N_var,N_part,LB,UB,r,delta,latin);
        
        
        g_options =gaoptimset('MutationFcn',@mutationgaussian_Lor,'CrossoverFcn',@crossoverscattered_Lor,'NonlinConAlgorithm','penalty',...
            'InitialPopulation',XX,'EliteCount',5,'TolFun',1e-3,'TolCon',1e-4,'PopulationSize',latin*N_var,'PlotFcn', {@gaplotchange,@Lorenzo_plot,@gaplotbestf,@gaplotscorediversity,@gaplotselection},...
            'Generations',10,'StallGenLimit',5,'Display','iter');
        
        
        
        [x,fval,exitflag,output,population,scores]=ga(@Obj_Fun_Coord,N_var,[],[],[],[],LB,UB,@nonlcon_ott_semplice,g_options);
        filename=sprintf('WSpart%d-Vf%d.mat',N_part,Vf);
        save(filename,'fval','x','N_part','Vf')
    end
end