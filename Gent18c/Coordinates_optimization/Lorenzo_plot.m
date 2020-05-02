function state = Lorenzo_plot(options,state,flag)
global Vf
global N_part

filename=sprintf('WSpart%d-Gen%i-Vf%d.mat',N_part,state.Generation,Vf);
% filename = 'WSpar3Vf10.mat';
save(filename)
end