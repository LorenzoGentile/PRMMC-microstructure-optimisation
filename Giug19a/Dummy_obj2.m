function [a]=Dummy_obj2(x)
a=1;
ii=1;
global N_part
global r
global delta
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
end