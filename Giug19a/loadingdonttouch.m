clear all
delta=.1;
list=linspace(2,20,19);
volumes=linspace(0.1,0.25,16);
for V=1:16
    for N=1:19
        
        Vf=volumes(V);
        N_part=list(N);
        
        r=(1000*Vf*3/(4*pi*N_part))^(1/3);
        % filename=sprintf('WSpart%d-Vf%d.mat',N_part,Vf);
        a=exist (sprintf('WSpart%d-Vf%d.mat',N_part,Vf));
        if a==2
            filename=sprintf('WSpart%d-Vf%d.mat',N_part,Vf);
            load(filename)
            for i=1:N_part
                pos(i,1:3)=X_ga(1+3*(i-1):3+3*(i-1));
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
            c=max(C);
            destination=(sprintf('X_ottimi-Vf%%%d.dat',Vf*100));
            destination_2=(sprintf('E_ottimi-Vf%%%d.dat',Vf*100));
            fileID = fopen(destination,'a');
            fileID_2 = fopen(destination_2,'a');
            %fprintf(fileID, '\n \n \t \t\t \t part%d-Vf%d.mat',N_part,Vf);
            fprintf(fileID_2,'\n%.4f\t%.4f\t %d%%\t%d\t',-E,c,Vf*100,N_part);
            fprintf(fileID,'\n ');
            fprintf(fileID,'%.4d\t\t%.4d ',X_ga);
            fclose(fileID);
            fclose(fileID_2);
            RVE_gen(X_ga,Vf)
        end
    end
end

function RVE_gen(coordinates,Vf)
N_part=(length(coordinates))/3;
r=(1000*Vf*3/(4*pi*N_part))^(1/3);

for i=1:N_part
    pos(i,1:3)=coordinates(1+3*(i-1):3+3*(i-1));
end

figure(1)
axis([0 10 0 10 0 10 ])
titolo=sprintf('%d Particles Vf %d%%',N_part,Vf*100);
title(titolo)
xlabel('x') % x-axis label
ylabel('y') % y-axis label
zlabel('z')
grid on

hold on
[x,y,z] = sphere(30);
for i=1:N_part
    surf(x*r+pos(i,1), y*r+pos(i,2), z*r+pos(i,3))
end
print('-bestfit',titolo,'-dpdf')
close (figure(1))
end