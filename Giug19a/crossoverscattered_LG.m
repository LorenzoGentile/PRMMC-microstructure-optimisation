function xoverKids  = crossoverscattered_LG(parents,options,GenomeLength,~,~,thisPopulation)
global N_part;
global Vf
Volume=1000;
f_options = optimoptions('fmincon','Display','off','ConstraintTolerance',1e-8) ;
pos=zeros(N_part,3);
r=(Volume*Vf*3/(4*pi*N_part))^(1/3);
delta=.1;
N_var=3*N_part;
LB(1,1:N_var)=r+delta;
UB(1,1:N_var)=10-(r+delta);
c=cumsum(1:N_part);
C=zeros(c(end),1);
xoverKids=crossoverscattered(parents,options,GenomeLength,[],[],thisPopulation);
for n=1:size(xoverKids,1)
    temp=xoverKids(n,:);
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
    
    if max(C)<=.05
        
        [a,~,exitflag_c,~]=fmincon(@Dummy_obj2,temp,[],[],[],[],LB,UB,@nonlcon_ott_semplice,f_options);
        %disp(output.constrviolation)
        if exitflag_c~=-2
            
            xoverKids(n,:)=a;
            
        end
        
    end
end