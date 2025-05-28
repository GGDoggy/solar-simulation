% Load trajectory data
trajectory_data = get_trajectory();
scale = 4e9;
dt = 3600;
close_dt = 1;
init_fire_delay = 242616;
init_run_time = 175200;
change_rate = 10000;
start_time_map = trajectory_data.earth;
keys_list = keys(start_time_map);
first_key = keys_list{1};
start_time = 2433283;

% Initialize conditions
cond = Conditions(init_fire_delay, init_run_time, trajectory_data, change_rate, start_time, scale, dt, close_dt);

% Create figure and axes
fig = figure('Name', 'Solar Sim');
ax = axes('Parent', fig);
hold(ax, 'on');
view(ax, 3);

% Initial plot
[traj_history, vel_history, acc_history, times] = cond.sim(ax);

pos = traj_history;
vel = vel_history;
acc = acc_history;
time = times;
plot_trajectory(ax, traj_history, 1e9);
save("spacecraft.mat", "pos", "vel", "acc", "time");

% % Add buttons
% uicontrol('Style', 'pushbutton', 'String', 'Add DL', ...
%     'Units', 'normalized', 'Position', [0.7 0.09 0.1 0.06], ...
%     'Callback', @(src, event) cond.add_fire_delay(ax));
% uicontrol('Style', 'pushbutton', 'String', 'Sub DL', ...
%     'Units', 'normalized', 'Position', [0.81 0.09 0.1 0.06], ...
%     'Callback', @(src, event) cond.sub_fire_delay(ax));
% uicontrol('Style', 'pushbutton', 'String', 'Add RT', ...
%     'Units', 'normalized', 'Position', [0.7 0.01 0.1 0.06], ...
%     'Callback', @(src, event) cond.add_run_time(ax));
% uicontrol('Style', 'pushbutton', 'String', 'Sub RT', ...
%     'Units', 'normalized', 'Position', [0.81 0.01 0.1 0.06], ...
%     'Callback', @(src, event) cond.sub_run_time(ax));
% uicontrol('Style', 'pushbutton', 'String', 'acc', ...
%     'Units', 'normalized', 'Position', [0.81 0.17 0.1 0.06], ...
%     'Callback', @(src, event) cond.update_acc(ax));