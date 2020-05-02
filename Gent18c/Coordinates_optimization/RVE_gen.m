function RVE_gen(coordinates,Vf)
N_part=(length(coordinates))/3;
r=(1000*Vf*3/(4*pi*N_part))^(1/3);

for i=1:N_part
    pos(i,1:3)=coordinates(1+3*(i-1):3+3*(i-1));
end

figure
axis([0 10 0 10 0 10 ])
        title('4 Particles Vf 10%')
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