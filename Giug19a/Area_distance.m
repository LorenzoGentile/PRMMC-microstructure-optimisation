function [sum_aree,dist_x]=Area_distance(x)
Vf=.2;
Volume=1000;
N_part=4;
r_0=(Volume*Vf*3/(4*pi*N_part))^(1/3);

r(1:length(x),1:N_part)=r_0;
for i=1:N_part
    Y(:,i)=x(:,(i-1)*3+2);
    Z(:,i)=x(:,(i-1)*3+3);
    
end

dist_x=zeros(length(x),1);
for i=1:N_part-1
    for j=i+1:N_part
        dist_x=dist_x+abs((x(:,(i-1)*3+1)-x(:,(j-1)*3+1)));
     
    end
end




for ii=1:(length(Z))

     M_int(:,:,ii)=triu([zeros(1,N_part);area_intersect_circle_analytical(Y(ii,:),Z(ii,:),r(ii,:))]);
    
end


sum_aree(:,1)=sum(sum(M_int));
end