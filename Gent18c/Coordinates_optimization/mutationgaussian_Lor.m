function mutationChildren = mutationgaussian_Lor(parents,options,GenomeLength,FitnessFcn,state,thisScore,thisPopulation)
global delta;
global r;
global N_part;
global UB;
global LB;
STD_SUM=0;
sd=zeros(1,N_part*3); 
for i=1:N_part*3    
    sd(i)=std(state.Population(:,i));
    STD_SUM=STD_SUM+sd(i);
end    

mutationRate=1.5-(STD_SUM/300)^(.5);
mutationChildren= mutationuniform(parents,options,GenomeLength,FitnessFcn,state,thisScore,thisPopulation,mutationRate);
  for n=1:size(mutationChildren,1)
    temp=mutationChildren(n,:);
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
    
    if max(C)>=.05 || max(mutationChildren(n,:))>10-r || min(mutationChildren(n,:))<r
        
        a=fmincon(@Dummy_obj2,temp,[],[],[],[],LB,UB,@nonlcon_ott_semplice);
        
        mutationChildren(n,:)=a;
        
    end
  end
end
