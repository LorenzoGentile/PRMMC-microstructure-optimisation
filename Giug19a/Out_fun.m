function [state,g_options,optchanged] = Out_fun(~,state,~)
global Vf;

f_options = optimoptions('fmincon','Display','off') ;
f_options.StepTolerance = 1.0e-4;
f_options.MaxFunctionEvaluations = 10^12;
f_options.OptimalityTolerance =1e-4;
f_options.ConstraintTolerance = 1e-8;
f_options.MaxIterations = 40000;

if state.Generation~=0
    if mod(state.Generation,300)==0
        
        [sorted,index]=sort(state.Score,'ascend');
        
        
        RVE_gen(state.Population(index(1,1),:),Vf);
        [ott,ott_values]=MBH_LG(state.Population(index(1,1),:),state.Score(index(1,1)));
        % [ott,ott_values,exitflag_out,output]=fmincon(@Overlap_sum_cons,state.Population(index(1,1),:),[],[],[],[],LB,UB,[],f_options);
        % disp(output.constrviolation)
        % pause(0.1)
        clearvars f_options
        if ott_values<sorted(1,1)
            state.Score(index(end,1),1)=ott_values;
            state.Population(index(end,1),:)=ott;
            if state.Generation~=0
                state.Best(end)=ott_values;
            end
            
        end
    end
end


if  state.Generation>1004
    
    if -state.Best(state.Generation)-(-state.Best(state.Generation-1000))<0.05
        g_options=gaoptimset('CrossoverFraction',0.2);
        optchanged='true';
    else
        g_options =gaoptimset('Vectorized','off');
        optchanged='false';
    end
else
    g_options =gaoptimset('Vectorized','off');
    optchanged='false';
    
    
end
%% interrupt
if state.Generation>1500
    if -state.Best(state.Generation)-(-state.Best(state.Generation-1000))<0.005
        state.StopFlag =1;
    end
end

end