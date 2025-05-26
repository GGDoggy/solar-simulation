clear all

load('spacecraft.mat', 'pos', 'vel', 'acc', 'time');
load('planet_trajectories.mat');
load('voyager2.mat');

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

revo = 0;
last_ang = 0;

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
    
    rot = inv([n_r(:), n_the(:), n_z(:)]);
    vel_tran = rot * vel_i';
    
    v = vel_i;
    v(3) = 0;
    n_v = v / norm(v);
    n_2 = cross(n_z, n_v);
    
    rot2 = inv([n_v(:), n_2(:), n_z(:)]);
    acc_tran = rot2 * acc_i(:);
    
    raw_ang = atan(r(2) / r(1)) + revo * pi + pi/2;
    if raw_ang < last_ang
        raw_ang = raw_ang + pi;
        revo = revo + 1;
    end
    last_ang = raw_ang;
    
    radi(i) = r_norm;
    ang(i) = raw_ang;
    z(i) = pos_i(3);
    v_r(i) = vel_tran(1);
    v_the(i) = vel_tran(2);
    v_z(i) = vel_tran(3);
    a_vel(i) = acc_tran(1);
    a_2(i) = acc_tran(2);
    a_z(i) = acc_tran(3);
    ang_mom(i) = norm(cross(pos_i, vel_i));
end

% Position vs. Time
figure;
subplot(3,1,1); plot(time, radi); title('Radial Position');
subplot(3,1,2); plot(time, ang); title('Angular Position');
subplot(3,1,3); plot(time, z); title('Vertical Position'); xlabel('Time (s)');
sgtitle('Position vs. Time');

% Velocity vs. Time
figure;
subplot(3,1,1); plot(time, v_r); title('Radial Velocity');
subplot(3,1,2); plot(time, v_the); title('Tangential Velocity');
subplot(3,1,3); plot(time, v_z); title('Vertical Velocity'); xlabel('Time (s)');
sgtitle('Velocity vs. Time');

% Boost Acceleration vs. Time
figure;
subplot(3,1,1); plot(time, a_vel); title('Forward Acceleration');
subplot(3,1,2); plot(time, a_2); title('Side Acceleration');
subplot(3,1,3); plot(time, a_z); title('Vertical Acceleration'); xlabel('Time (s)');
sgtitle('Boost Acceleration vs. Time');

% Angular Momentum vs. Time
figure;
plot(time, ang_mom);
title('Angular Momentum vs. Time');

% Radial Position vs. Angular Position
figure;
plot(ang, radi);
title('Radial Position vs. Angular Position');

% 3D Trajectory Plot
figure;
ax = axes('NextPlot','add');
hold on;
plot_trajectory(ax, pos, 5e9);
plot_planet_trajectory(ax, "voyager 2", voyager2(1:end-7000, :), time(1), time(end), 5e9);
plot_planet_trajectory(ax, "earth", earth, time(1), time(end), 5e9);
plot_planet_trajectory(ax, "mars", mars, time(1), time(end), 5e9);
plot_planet_trajectory(ax, "jupiter", jupiter, time(1), time(end), 5e9);
plot_planet_trajectory(ax, "saturn", saturn, time(1), time(end), 5e9);
plot_planet_trajectory(ax, "uranus", uranus, time(1), time(end), 5e9);
plot_planet_trajectory(ax, "neptune", neptune, time(1), time(end), 5e9);
hold off;
xlabel('X'); ylabel('Y'); zlabel('Z');
title('Spacecraft Trajectory');
grid on;