function [x_best,y_best]=MBH_LG(x0,y0)
global Vf

raggio=1;
Volume=1000;
N_part=length(x0)/3;
pos=zeros(N_part,3);
c=cumsum(1:N_part);
C=zeros(c(end),1);
r=(Volume*Vf*3/(4*pi*N_part))^(1/3);
delta=.1;
N_var=3*N_part;
LB(1,1:N_var)=r+delta;
UB(1,1:N_var)=10-(r+delta);
ub=UB(1);
lb=LB(1);
f_options = optimoptions('fmincon','Display','off') ;
f_options.StepTolerance = 1.0e-4;
f_options.MaxFunctionEvaluations = 10^12;
f_options.OptimalityTolerance =1e-4;
f_options.ConstraintTolerance = 1e-8;
f_options.MaxIterations = 40000;
x_evaluated=x0;
y_compare=y0;
x_best=x0;
y_best=y0;
for i=1:50
    [ott,ott_values,exitflag,~]=fmincon(@Overlap_sum_cons,x_evaluated,[],[],[],[],LB,UB,@nonlcon_ott_semplice,f_options);
    if ott_values<y_compare && exitflag~=-2
        
        for I=1:N_part
            pos(I,1:3)=ott(1+3*(I-1):3+3*(I-1));
        end
        II=1;
        
        for I=1:N_part-1
            for J=I+1:N_part
                dist_x=(pos(J,1)-pos(I,1)).^2;
                dist_y=(pos(J,2)-pos(I,2)).^2;
                dist_z=(pos(J,3)-pos(I,3)).^2;
                
                C(II,1)=-sqrt( dist_x+ dist_y + dist_z)+2*r+delta;
                II=II+1;
            end
        end
        
        if max(C)<=.05
            x_evaluated=ott;
            y_compare=ott_values;
            i=1;
        end
        
    else
        add=rand(1,length(x0));
        x_evaluated=x_evaluated+(add*raggio*2)-raggio;
        x_evaluated(x_evaluated>ub)=ub;
        x_evaluated(x_evaluated<lb)=lb;
        
    end
end
if y_compare<y0
    for I=1:N_part
        pos(I,1:3)=ott(1+3*(I-1):3+3*(I-1));
    end
    II=1;
    
    for I=1:N_part-1
        for J=I+1:N_part
            dist_x=(pos(J,1)-pos(I,1)).^2;
            dist_y=(pos(J,2)-pos(I,2)).^2;
            dist_z=(pos(J,3)-pos(I,3)).^2;
            
            C(II,1)=-sqrt( dist_x+ dist_y + dist_z)+2*r+delta;
            II=II+1;
        end
    end
    if max(C)<=.05
    y_best=y_compare;
    x_best= x_evaluated;
    end
end



