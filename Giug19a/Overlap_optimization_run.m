clear all;
global delta;
global r;
global N_part;
global Volume;
global Vf;
global UB;
global LB;
% Calculation of sphere radius
list=[2,4,6,8,10];
volumes=[0.1,.14,.25];
for V=1:size(volumes,2)
    for N=1:size(list,2)      
        x_min=0;
        x_max=10;
        y_min=0;
        y_max=10;
        z_min=0;
        z_max=10;
       
        Vf=volumes(V);
        Volume=(x_max-x_min)*(y_max-y_min)*(z_max-z_min);
        
        N_part=list(N);
        r=(Volume*Vf*3/(4*pi*N_part))^(1/3);
        delta=.1;
        N_var=3*N_part;
        LB(1,1:N_var)=r+delta;
        UB(1,1:N_var)=10-(r+delta);
        
        iterazioni=0;
        index_min=1;
        minimo=0;
        X_ga=0;
        pop=min(N_var*10,300);
        latin=min(N_var*20,1000);
        %____________________________________________________________________________
        %____________________________________________________________________________
        
        
        % while diff<-0.001
        iterazioni=iterazioni+1;
        XX=Creation_fun_LG(N_var,N_part,LB,UB,r,delta,latin);
        
        options = optimoptions('fmincon','Display','off') ;
        
        options.StepTolerance = 1.0e-4;
        options.MaxFunctionEvaluations = 10^12;
        options.OptimalityTolerance =1e-4;
        options.ConstraintTolerance = 1e-8;
        options.MaxIterations = 40000;
        
        X=[];
        %____________________________________________________________________________
        %Multistart
        %___________________________________________________________________________
        for ii=1:length(XX)
            if ii==1
                if X_ga~=0
                    XX(1,:)=X_ga;
                end
            end
            x0=XX(ii,:);
            
            [x,fval] =fmincon(@obj_fun,x0,[],[],[],[],LB,UB,@nonlcon_ott_semplice,options);
            
            X(ii,:)=x;
            fvals(ii)=fval;
            disp(fval);
            disp(minimo);
            disp(ii);
            disp(length(XX))
            %____________________________________________________________________________
            %____________________________________________________________________________
            
            % if fval<minimo
            % minimo=fval;
            % index_min=ii;
            
            % if ii~=1
            % close(2)
            % end
            
            % RVE_gen(X(ii,:),Vf)
            % pause(0.001)
            % end
        end
        %____________________________________________________________________________
        %____________________________________________________________________________
        
        [Bests_values,Bests]=sort(fvals,'ascend');
        Bests=Bests(1:pop);
        Bests_values=Bests_values(1:pop);
        
        
        g_options =gaoptimset('Generations',...
            10000,'StallGenLimit',Inf,'TolFun',0,'TolCon',1e-5,...
            'NonlinConAlgorithm','penalty','InitialPopulation',X(Bests,:),'InitialScores',Bests_values,'OutputFcns',@Out_fun,'EliteCount',...
            floor(0.05*pop),'PopulationSize',length(Bests),'Display','iter','CrossoverFraction',0.8, ...
            'PlotFcn',{ @gaplotbestf,@gaplotchange});
        
        [X_ga,fval_ga]=ga(@obj_fun,N_var,[],[],[],[],LB,UB,@nonlcon_ott_semplice,g_options)
        
        
        diff=fval_ga-Bests_values(1)
        valori_finali(iterazioni,1)=fval_ga;
        valori_finali(iterazioni,2)=Bests_values(1)
        minimo=fval_ga;
     
        %____________________________________________________________________________
        % Young Modulus evaluation
        %___________________________________________________________________________
        
        
        E = 0;
        for g=1:N_part
            pos(g,1:3)=X_ga(1+3*(g-1):3+3*(g-1));
        end
        gg=1;
        for g=1:N_part-1
            for h=g+1:N_part
                dist_x=(pos(h,1)-pos(g,1)).^2;
                dist_y=(pos(h,2)-pos(g,2)).^2;
                dist_z=(pos(h,3)-pos(g,3)).^2;
                
                C(gg,1)=-sqrt( dist_x+ dist_y + dist_z)+2*r+delta;
                gg=gg+1;
            end
        end
         constraint=max(C);
         
%         Uncomment thisif Abaqus is available
%         
%         if max(C)<=0.01
%             E=Abaqus_run(X_ga)
%         else
#             E=0;
%         end
         filename=sprintf('WSpart%d-Vf%d.mat',N_part,Vf);
         
%         Uncomment thisif Abaqus is available

%         save(filename,'E','X_ga','constraint','fval_ga')
          save(filename,'E','X_ga','constraint','fval_ga')        
%         
    end
end
