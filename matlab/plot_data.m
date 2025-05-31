clear all

load('spacecraft.mat', 'pos', 'vel', 'acc', 'time');
load('planet_trajectories.mat');
load('voyager2.mat');

start_time = time(1);
end_time = time(end);
time = time - start_time;
AU = 149597870.7;
pos = pos / AU;

N = length(time);
radi = zeros(N,1);
ang = zeros(N,1);
z = zeros(N,1);
v_r = zeros(N,1);
v_the = zeros(N,1);
v_z = zeros(N,1);
a_vel = zeros(N,1);
a_2 = zeros(N,1);
a_z = zeros(N,1);
ang_mom = zeros(N,1);
plot_x = zeros(N,1);
plot_y = zeros(N,1);

revo = 0;
last_ang = 0;
finpos = pos(end,:);
finpos(3) = 0;
finpos = finpos / norm(finpos);
to_plot = [finpos; cross(finpos, [0 0 1], 2); [0 0 1]]';

for i = 1:N
    pos_i = pos(i,:);
    vel_i = vel(i,:);
    acc_i = acc(i,:);
    
    n_z = [0; 0; 1];
    r = pos_i;
    r(3) = 0;
    r_norm = norm(r);
    n_r = r / r_norm;
    n_the = cross(n_z, n_r);
    
    rot = [n_r(:), n_the(:), n_z(:)]';
    vel_tran = rot * vel_i';
    
    v = vel_i;
    v(3) = 0;
    n_v = v / norm(v);
    n_2 = cross(n_z, n_v);
    
    rot2 = [n_v(:), n_2(:), n_z(:)]';
    acc_tran = rot2 * acc_i(:);
    
    raw_ang = atan(r(2) / r(1)) + revo * pi + pi/2;
    if raw_ang < last_ang
        raw_ang = raw_ang + pi;
        revo = revo + 1;
    end
    last_ang = raw_ang;

    plot_pos = to_plot * pos_i';
    plot_x(i) = plot_pos(1);
    plot_y(i) = plot_pos(2);
    
    radi(i) = r_norm;
    ang(i) = raw_ang;
    z(i) = pos_i(3);
    v_r(i) = vel_tran(1);
    v_the(i) = vel_tran(2);
    v_z(i) = vel_tran(3);
    a_vel(i) = acc_tran(1);
    a_2(i) = acc_tran(2);
    a_z(i) = acc_tran(3);
    ang_mom(i) = norm(cross(pos_i, vel_i)) * AU;
end

% Position vs. Time
figure;
stackedplot(time, [radi, ang, z], ...
    'DisplayLabels', {'Radial (AU)', 'Angular (rad)', 'Vertical (AU)'});
title('Position vs. Time');
xlabel('Time (h)');

% Velocity vs. Time
figure;
stackedplot(time, [v_r, v_the, v_z], ...
    'DisplayLabels', {'Radial (km/s)', 'Angular (km/s)', 'Vertical (km/s)'});
title('Velocity vs. Time');
xlabel('Time (h)');

% % Acceleration vs. Time
% figure;
% stackedplot(time, [a_vel, a_2, a_z], ...
%     'DisplayLabels', {'Forward (km/s^2)', 'Side (km/s^2)', 'Vertical (km/s^2)'});
% title('Acceleration vs. Time');
% xlabel('Time (h)');

% Angular Momentum vs. Time
figure;
plot(time, ang_mom);
title('Specific Angular Momentum vs. Time');
xlabel('Time (h)');
ylabel('Specific Angular Momentum (km^2/s)');

% vo2 = voyager2(1:end-7000, :);
% vo2(:, 2:4) = (to_plot * vo2(:, 2:4)')' / AU;
% earth(:, 2:4) = (to_plot * earth(:, 2:4)')' / AU;
% mars(:, 2:4) = (to_plot * mars(:, 2:4)')' / AU;
% jupiter(:, 2:4) = (to_plot * jupiter(:, 2:4)')' / AU;
% saturn(:, 2:4) = (to_plot * saturn(:, 2:4)')' / AU;
% uranus(:, 2:4) = (to_plot * uranus(:, 2:4)')' / AU;
% neptune(:, 2:4) = (to_plot * neptune(:, 2:4)')' / AU;

% % Trajectory Plot
% figure('Units', 'normalized', 'Position', [0.12 0.25 0.25 0.6]);
% scale = [-2e9 6e9 -3e9 5e9 -2e8 2e8] / AU;
% ax1 = subplot(6, 4, 1:16);
% hold on;
% grid on;
% ylabel('Y (AU)');
% legend("Location", "se");
% ax2 = subplot(6, 4, 17:24);
% ax2.Position(3) = ax1.Position(3);
% hold on;
% grid on;
% plot_trajectory(ax1, ax2, (to_plot * pos')', scale, "#FF0000");
% plot_planet_trajectory(ax1, ax2, "Voyager 2", vo2, start_time, end_time, scale, "#77AC30");
% plot_planet_trajectory(ax1, ax2, "Earth", earth, start_time, end_time, scale, "#0072BD");
% plot_planet_trajectory(ax1, ax2, "Mars", mars, start_time, end_time, scale, "#D95319");
% plot_planet_trajectory(ax1, ax2, "Jupiter", jupiter, start_time, end_time, scale, "#EDB120");
% plot_planet_trajectory(ax1, ax2, "Saturn", saturn, start_time, end_time, scale, "#A2142F");
% plot_planet_trajectory(ax1, ax2, "Uranus", uranus, start_time, end_time, scale, "#7E2F8E");
% plot_planet_trajectory(ax1, ax2, "Neptune", neptune, start_time, end_time, scale, "#4DBEEE");
% hold off;
% xlabel('X (AU)'); ylabel('Z (AU)');
% title(ax1, 'Spacecraft Trajectory');
% set(ax1,'xticklabel',[], 'xtick', -10:5:40);
% set(ax2, 'xtick', -10:5:40);