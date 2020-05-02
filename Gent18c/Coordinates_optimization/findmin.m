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
disp(index_min)
disp('Emax')
disp(-t)
figure
plot(1:length(state.Score),state.Score)
hold on
RVE_gen(state.Population(index_min,:),Vf)
end
function RVE_gen(coordinates,Vf)
N_part=(length(coordinates))/3;
r=(1000*Vf*3/(4*pi*N_part))^(1/3);

for i=1:N_part
    pos(i,1:3)=coordinates(1+3*(i-1):3+3*(i-1));
end

figure
axis([0 10 0 10 0 10 ])
        title('Cluster')
        xlabel('x') % x-axis label
        ylabel('y') % y-axis label
        zlabel('z')
        grid on
        
        hold on
        [x,y,z] = sphere(30);
        for i=1:N_part
        surf(x*r+pos(i,1), y*r+pos(i,2), z*r+pos(i,3)) 
        end
end