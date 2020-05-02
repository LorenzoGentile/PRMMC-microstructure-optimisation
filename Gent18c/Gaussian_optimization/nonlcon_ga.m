
%% Random coordinates generations based on proper distribution charateristhics
function [C,Ceq]=nonlcon_ga(x)
global delta;
global Vf;
global Volume;
global N_part;
iterazione=1;
exitflag=0;
 x_min=0;
        x_max=10;
        y_min=0;
        y_max=10;
        z_min=0;
        z_max=10;
while iterazione <200 && exitflag==0
    
    %% Definition
    Ceq=[];
    exitflag=1;
    
    
    r=(Volume*Vf*3/(4*pi*N_part))^(1/3); 
    d=2*r+delta;
    % Definition of Gaussians charateristics
    sigma_x=x(1)/10;
    sigma_y=x(2)/10;
    sigma_z=x(3)/10;
    
    mu_x=5;
    mu_y=5;
    mu_z=5;
    
    % Vectors o coordinates Preallocation
    x_coord=zeros(1,N_part);
    y_coord=zeros(1,N_part);
    z_coord=zeros(1,N_part);
    
    
    x_gauss = normrnd(mu_x,sigma_x,1,100);
    
    y_gauss = normrnd(mu_y,sigma_y,1,100);
    
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
    
    XX=0;
    for i=1:N_part
        
        if  dimension>1
            
            pick=randi([1,dimension],1);
            x_coord(i)=posx(pick);
            y_coord(i)=posy(pick);
            z_coord(i)=posz(pick);
            
            dist_x=(posx-x_coord(i)).^2;
            dist_y=(posy-y_coord(i)).^2;
            dist_z=(posz-z_coord(i)).^2;
            
            distances=sqrt( dist_x+ dist_y + dist_z);
            distance = sort(distances);
            
            indexx=find(distances<d);
            distances(indexx) = [];
            
            
            dist_x(indexx)=[];
            dist_y(indexx)=[];
            dist_z(indexx)=[];
            
            
            
            posx(indexx)=[];
            posy(indexx)=[];
            posz(indexx)=[];
            
            
            
            exitflag=1;
        else
            if XX ==0
                iterazione=iterazione+1;
                XX=XX+1;
            end
            exitflag=0;
            if i==1
                x_coord(i)=0;
                y_coord(i)=0;
                z_coord(i)=0;
                
            else
                x_coord(i)=x_coord(i-1);
                y_coord(i)=y_coord(i-1);
                z_coord(i)=z_coord(i-1);
                
            end
        end
        dimension=size(posx,1);
    end
end
B=zeros(6000,1);
if N_part==1
    B(1,1)=-1;
    
else
    n=1;
    for i=1:N_part-1
        for   j=i+1:N_part
            dist_x=(x_coord(j)-x_coord(i)).^2;
            dist_y=(y_coord(j)-y_coord(i)).^2;
            dist_z=(z_coord(j)-z_coord(i)).^2;
            
            B(n,1)=-sqrt( dist_x+ dist_y + dist_z)+d;
            n=n+1;
        end
    end
    
end
C=B;
end

