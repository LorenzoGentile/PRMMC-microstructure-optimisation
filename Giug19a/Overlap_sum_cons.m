function [output]=Overlap_sum_cons(x)
global r;
global N_part;
global delta;
r_0(1,1:N_part)=r;
for i=1:N_part
    Y(i)=x((i-1)*3+2);
    Z(i)=x((i-1)*3+3);
    
end
M_int=triu([zeros(1,N_part);area_intersect_circle_analytical(Y,Z,r_0)]);
sum_area=-sum(sum(M_int));
for i=1:N_part
    pos(i,1:3)=x(1+3*(i-1):3+3*(i-1));
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
    
    if max(C)<=0
    output=sum_area;
else
    output=0;
end
end