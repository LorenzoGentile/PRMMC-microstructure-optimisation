function [E]=Abaqus_run(x)
global r;
global delta;
global N_part;
for i=1:N_part
    X(i)=x((i-1)*3+1);
    Y(i)=x((i-1)*3+2);
    Z(i)=x((i-1)*3+3);
    
end
ii=1;
for i=1:N_part
    pos(i,1:3)=x(1+3*(i-1):3+3*(i-1));
end

for i=1:N_part-1
    for j=i+1:N_part
        dist_x=(pos(j,1)-pos(i,1)).^2;
        dist_y=(pos(j,2)-pos(i,2)).^2;
        dist_z=(pos(j,3)-pos(i,3)).^2;
        
        C(ii,1)=-sqrt( dist_x+ dist_y + dist_z)+2*r+delta;
        ii=ii+1;
    end
end

if max(C)<=0.05
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    %% Start analisys with Abaqus
    
    mo='nogui';
    
    scala(1:N_part,1)=r;
    fid = fopen('DATI.py', 'w');
    
    fprintf(fid,' %d \n %f\n %f\n %f\n %f\n',N_part,X,Y,Z,scala);
    fclose(fid);
    
    exit=1;
    it=0;
    while exit==1 && it<4
        exit=system(['abaqus cae ',mo,'=RVE_Load.py']);
        it=it+1;
        if exit==1
            pause(30);
        end
    end
    if exit==0
        system(['abaqus Viewer ',mo,'=Read_DISP.py']);
        
        fido = fopen('YM_calc.txt');
        E=fscanf(fido,'%f');
        fclose(fido);
        E=-E/1e4;
        pause(0.1)
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        delete('abaqus.rpy','abaqus.rpy.1','PBCx.com','PBCx.sim','PBCx.odb','PBCx.dat','PBCx.prt','PBCx.inp','PBCx.msg','PBCx.sta');
        
    else
        
        E=-6.89;
    end
else
   
    E=-6.89;
end


end















