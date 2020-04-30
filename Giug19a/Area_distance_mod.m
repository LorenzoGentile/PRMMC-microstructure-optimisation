function [distbar,dist_x,sum_aree,minimi]=Area_distance_mod(x,y,z)
Vf=.1;
Volume=1000;
N_part=5;
r_0=(Volume*Vf*3/(4*pi*N_part))^(1/3);

r(1:length(y),1:N_part)=r_0;
bar=(sum(x))./N_part;
distbar=(sum(abs(x-bar),2))./N_part;
dist_x=zeros(length(x),1);
minimi(1:length(x),1)=100;
for i=1:N_part-1
    for j=i+1:N_part
        dist_x=dist_x+abs(x(:,i)-x(:,j));
     minimi=min(minimi,abs(x(:,i)-x(:,j)));

    end
end
% minimo=min(minimi,[],2);

for ii=1:(length(x))

     M_int(:,:,ii)=triu([zeros(1,N_part);area_intersect_circle_analytical(y(ii,:),z(ii,:),r(ii,:))]);
    
end


sum_aree(:,1)=sum(sum(M_int));
end