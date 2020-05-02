function [E]=Objective_function(x)
%% Definition
global delta;
global Vf;
global Volume;
global N_part
iteration=0;
exitflag=1;
x_min=0;
x_max=10;
y_min=0;
y_max=10;
z_min=0;
z_max=10;
while exitflag==1 && iteration<200
    
    
    r=(Volume*Vf*3/(4*pi*N_part))^(1/3);
    d=2*r+delta;
    % Definition of Gaussians charateristic
    mu_x(1:x(4))=linspace(10/(2*x(4)),10- 10/(2*x(4)),x(4));
    mu_y(1:x(5))=linspace(10/(2*x(5)),10- 10/(2*x(5)),x(5));
    mu_z(1:x(6))=linspace(10/(2*x(6)),10- 10/(2*x(6)),x(6));
    
    
    
    sigma_x=x(1)/10;
    sigma_y=x(2)/10;
    sigma_z=x(3)/10;
    
    % Vectors o coordinates Preallocation
    x_coord=zeros(1,N_part);
    y_coord=zeros(1,N_part);
    z_coord=zeros(1,N_part);
    x_gauss=zeros(round(100/x(4))*x(4),1);
    y_gauss=zeros(round(100/x(5))*x(5),1);
    z_gauss=zeros(round(100/x(6))*x(6),1);
    
    for i=1:x(4)
        % rng(1*N_part,'twister');
        x_gauss_temp= normrnd(mu_x(i),sigma_x,round(100/x(4)),1);
        x_gauss((i-1)*round(100/x(4))+1:i*round(100/x(4)))=x_gauss_temp;
    end
    for i=1:x(5)
        % rng(1*N_part,'twister');
        y_gauss_temp= normrnd(mu_y(i),sigma_y,round(100/x(5)),1);
        y_gauss((i-1)*round(100/x(5))+1:i*round(100/x(5)))=y_gauss_temp;
    end
    %rng(2*N_part,'twister');
    for i=1:x(6)
        % rng(1*N_part,'twister');
        z_gauss_temp= normrnd(mu_z(i),sigma_z,round(100/x(6)),1);
        z_gauss((i-1)*round(100/x(6))+1:i*round(100/x(6)))=z_gauss_temp;
    end
    
    dimension=min(length(x_gauss),length(y_gauss));
    dimension=min(dimension,length(z_gauss));
    x_gauss=x_gauss(1:dimension);
    y_gauss=y_gauss(1:dimension);
    z_gauss=z_gauss(1:dimension);
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
    
    %% Pick coordinations randomly
    for i=1:N_part
        
        
        if dimension>1
            
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
            
            
            exitflag=0;
        else
            exitflag=1;
            
            %  disp ('distribuzione non accettaabile')
            
            
        end
        dimension=size(posx,1);
        
    end
    iteration=iteration+1;
end

if iteration ==20
    E=-68900;
else
    
    
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
        surf(x*r+x_coord(i), y*r+y_coord(i), z*r+z_coord(i))
    end
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %% Start analisys with Abaqus
    
    mo='nogui';
    
    scala(1:N_part,1)=r;
    fid = fopen('DATI.py', 'w');
    
    fprintf(fid,' %d \n %f\n %f\n %f\n %f\n',N_part,x_coord,y_coord,z_coord,scala);
    fclose(fid);
    
    system(['abaqus cae ',mo,'=RVE_Load.py'])
    
    system(['abaqus cae ',mo,'=Read_disp.py'])
    
    fido = fopen('YM_calc.txt');
    E=(fscanf(fido,'%f'));
    E=-E*1e-4
    fclose(fido);
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    delete('abaqus.rpy','abaqus.rpy.1','PBCx.com','PBCx.sim','PBCx.odb','PBCx.dat','PBCx.prt','PBCx.inp','PBCx.msg','PBCx.sta');
    
end
end