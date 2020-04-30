function [sum_aree]=area_vectorized(x)
global N_part;
global r;

r_0(1:length(x),1:N_part)=r;

for i=1:N_part
    Y(:,i)=x(:,(i-1)*3+2);
    Z(:,i)=x(:,(i-1)*3+3);

end

for ii=1:(length(Z))

     M_int(:,:,ii)=triu([zeros(1,N_part);area_intersect_circle_analytical(Y(ii,:),Z(ii,:),r(ii,:))]);
    
end


sum_aree(:,1)=sum(sum(M_int));
end