function [XX]=creation_fun_lor(N_var,N_part,LB,UB,r,delta)
X = lhsdesign(N_var*10,N_var);
XX=(X(:,:).*(UB-LB)+LB);
for n=1:N_var*10
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
        
        a=fmincon(@Dummy_obj2,temp,[],[],[],[],LB,UB,@nonlcon_ott_semplice);
        
        XX(n,:)=a;
        
    end
end
end