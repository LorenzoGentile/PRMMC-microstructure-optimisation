function  findmin(state,Vf)
t=0;
index_min=0;
for i=1:length(state.Score)
   if abs (state.Score(i,1)==min(state.Score))
       t=state.Score(i,1);
       index_min=i;
   end
end

disp('Index_min')
disp(state.Population(index_min,:))
disp('Emax')
disp(-t)
figure
plot(1:length(state.Score),state.Score)
hold on
RVE_gen(state.Population(index_min,:),Vf)
end
