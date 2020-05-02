function [C,Ceq]=nonlcon_ott_semplice(x)
global r;
global delta;
global N_part

ii=1;
pos=zeros(N_part,3);
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

Ceq=[];

end