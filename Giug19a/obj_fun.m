function [sum_aree]=obj_fun(x)
global r;
global delta;
global N_part;
global UB
global LB
c=cumsum(1:N_part);
C=zeros(c(end),1);
pos=zeros(N_part,3);

ii=1;
r_0(1:N_part)=r;
for i=1:N_part
    Y(i)=x((i-1)*3+2);
    Z(i)=x((i-1)*3+3);
    
end
for i=1:N_part
    pos(i,1:3)=x(1+3*(i-1):3+3*(i-1));
end

for i=1:N_part-1
    for j=i+1:N_part
        dist_x=(pos(j,1)-pos(i,1)).^2;
        dist_y=(pos(j,2)-pos(i,2)).^2;
        dist_z=(pos(j,3)-pos(i,3)).^2;
        
        C(ii,1)=-sqrt( dist_x+ dist_y + dist_z)+2*r+delta;
        ii=ii+1;
    end
end

if max(C)<=0.05 && min(x)>=LB(1) && max(x)<=UB(1)

    
 M_int=triu([zeros(1,N_part);area_intersect_circle_analytical(Y,Z,r_0)]);
 sum_aree=-sum(sum(M_int));
else
   
    sum_aree=0;
end


end















