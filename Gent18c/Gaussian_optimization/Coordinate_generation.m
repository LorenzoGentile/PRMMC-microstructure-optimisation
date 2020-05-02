
%% Random coordinates generations based on proper distribution charateristhics
function []=Coordinate_generation(N_part)



exitflag=0;
%% Definition

% Volume borders
x_min=0;
x_max=10;
y_min=0;
y_max=10;
z_min=0;
z_max=10;

% Calculation of sphere radius
Volume=(x_max-x_min)*(y_max-y_min)*(z_max-z_min);
Vf=.05;
N_part=50;
r=(Volume*Vf*3/(4*pi*N_part))^(1/3);
delta=0.1;
d=2*r+delta;
% Definition of Gaussians charateristics
mu_x=5;
mu_y=5;
mu_z=5;

sigma_x=.7;
sigma_y=3;
sigma_z=5;

% Vectors o coordinates Preallocation
x_coord=zeros(1,N_part);
y_coord=zeros(1,N_part);
z_coord=zeros(1,N_part);

% rng(1*N_part,'twister');
x_gauss = normrnd(mu_x,sigma_x,1,100);
% rng(2*N_part,'twister');
y_gauss = normrnd(mu_y,sigma_y,1,100);
% rng(3*N_part,'twister');
z_gauss = normrnd(mu_z,sigma_z,1,100);

%% Delimiting array

% The particles cannot be touch do volume edges
x_gauss=x_gauss(x_gauss>r+delta+x_min & x_gauss<-r-delta+x_max);
y_gauss=y_gauss(y_gauss>r+delta+y_min & y_gauss<-r-delta+y_max);
z_gauss=z_gauss(z_gauss>r+delta+z_min & z_gauss<-r-delta+z_max);

% The vectors have to be of the same size

dimension=min(length(x_gauss),length(y_gauss));
dimension=min(dimension,length(z_gauss));
x_gauss=x_gauss(1:dimension);
y_gauss=y_gauss(1:dimension);
z_gauss=z_gauss(1:dimension);

% Combine the coordinates to have an arra of points

ii=1;
pos=zeros(dimension^3,3);
for i=1:dimension
    for j=1:dimension
        for k=1:dimension
            pos(ii,1)=x_gauss(i);
            pos(ii,2)=y_gauss(j);
            pos(ii,3)=z_gauss(k);
            ii=ii+1;
        end
    end
end
dimension=length(pos);
posx = pos(:,1);
posy = pos(:,2);
posz = pos(:,3);
%     plot3(posx,posy,posz,'b+')

for i=1:N_part
    
    
    if dimension>=1
        pick=randi([1,dimension],1);
        x_coord(i)=posx(pick);
        y_coord(i)=posy(pick);
        z_coord(i)=posz(pick);
        
        dist_x=(posx-x_coord(i)).^2;
        dist_y=(posy-y_coord(i)).^2;
        dist_z=(posz-z_coord(i)).^2;
        
        distances=sqrt( dist_x+ dist_y + dist_z);
        distance = sort(distances);
        %                          plot(distance)
        indexx=find(distances<d);
        distances(indexx) = [];
        %             distances = distances(distances~=0);
        
        dist_x(indexx)=[];
        dist_y(indexx)=[];
        dist_z(indexx)=[];
        %             distances(indexx,:)=[];
        
        
        posx(indexx)=[];
        posy(indexx)=[];
        posz(indexx)=[];
        
        
        
    else
        
        exitflag=2;
        
        disp ('distribuzione non accettaabile')
        break
        
    end
    dimension=size(posx,1);
end









if exitflag==0
    for k=1:N_part-1
        if exitflag==1
            break
        end
        for i=k+1:N_part
            dist_x=(x_coord(k)-x_coord(i)).^2;
            dist_y=(y_coord(k)-y_coord(i)).^2;
            dist_z=(z_coord(k)-z_coord(i)).^2;
            
            
            exitflag=exitflag+((sqrt( dist_x+ dist_y + dist_z)))<d;
            if exitflag==1
                disp('qualcosa � andato storto')
                
                break
            end
            if exitflag==1
                break
            end
            
        end
    end
end

if exitflag==0
    
    dip =('ok')
    
    P(:,1)=x_coord;
    P(:,2)=y_coord;
    P(:,3)=z_coord;
    figure
    %plot3(P(:,1),P(:,2),P(:,3),'.','MarkerSize',10)
    axis([0 10 0 10 0 10 ])
    title('Cluster')
    xlabel('x') % x-axis label
    ylabel('y') % y-axis label
    ylabel('y')
    grid on
    
    hold on
    [x,y,z] = sphere(30);
    for i=1:N_part
        surf(x*r+x_coord(i), y*r+y_coord(i), z*r+z_coord(i)) % where (a,b,c) is center of the sphere
        
        hold on
    end
    if N_part==1
        B=-1;
        
    else
        n=1;
        for i=1:N_part-1
            for   j=i+1:N_part
                dist_x=(x_coord(j)-x_coord(i)).^2;
                dist_y=(x_coord(j)-y_coord(i)).^2;
                dist_z=(x_coord(j)-z_coord(i)).^2;
                
                B(n,1)=-sqrt( dist_x+ dist_y + dist_z)+d;
                n=n+1;
            end
        end
        
    end
    %trisurf(k,P(:,1),P(:,2),P(:,3),'Facecolor','blue','FaceAlpha',0.1)
    scala(1,1:N_part)=r;
%     Avvio_da_matlab(N_part,x_coord',y_coord',z_coord',scala);
end

