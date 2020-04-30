function [sum_area]=Overlap_sum(x)
global r;
global N_part;
r_0(1,1:N_part)=r;
for i=1:N_part
    Y(i)=x((i-1)*3+2);
    Z(i)=x((i-1)*3+3);
    
end
 M_int=triu([zeros(1,N_part);area_intersect_circle_analytical(Y,Z,r_0)]);
 sum_area=-sum(sum(M_int));
end