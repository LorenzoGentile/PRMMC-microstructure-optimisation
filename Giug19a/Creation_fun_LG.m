function [XX]=Creation_fun_LG(N_var,N_part,LB,UB,r,delta,latin)
X = lhsdesign(latin,N_var);
XX=(X(:,:).*(UB-LB)+LB);
for n=1:latin
    temp=XX(n,:);
    for i=1:N_part
        pos(i,1:3)=temp(1+3*(i-1):3+3*(i-1));
    end
    ii=1;
    for i=1:N_part-1
        for j=i+1:N_part
            dist_x=(pos(j,1)-pos(i,1)).^2;
            dist_y=(pos(j,2)-pos(i,2)).^2;
            dist_z=(pos(j,3)-pos(i,3)).^2;
            
            C(ii,1)=-sqrt( dist_x+ dist_y + dist_z)+2*r+delta;
            ii=ii+1;
        end
    end
    
    if max(C)>=.05
    options = optimoptions('fmincon','Display','off') ;
    
    options.StepTolerance = 1.0e-4;
    options.MaxFunctionEvaluations = 10^12;
    options.OptimalityTolerance =1e-4;
    options.ConstraintTolerance = 1e-8;
    options.MaxIterations = 40000;
        a=fmincon(@Dummy_obj2,temp,[],[],[],[],LB,UB,@nonlcon_ott_semplice,options);
        
        XX(n,:)=a;
        
    end
end
end