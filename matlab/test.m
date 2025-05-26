% trajectories = get_trajectory();
planets = {'earth','mars','jupiter','saturn','uranus','neptune'};
start_time = 2435283;
end_time = 2463283; % Adjust as needed
scale = 5e9;

% figure;
ax = axes('NextPlot','add');
% hold on;
% plot_planet_trajectory(ax, trajectories, planets, start_time, end_time, scale);
% hold off;
% legend;

planet_names = fieldnames(trajectories);
for i = 1:numel(planet_names)
    planet = planet_names{i};
    planet_map = trajectories.(planet);
    keys_list = keys(planet_map);
    planet_traj = cell2mat(values(planet_map, keys_list))';
    planet_traj = reshape(planet_traj, 7, [])';
    plot_planet_trajectory(ax, planet, planet_traj, start_time, end_time, scale);
end