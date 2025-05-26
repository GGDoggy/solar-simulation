simulation_main();

function simulation_main()
    % Constants
    G = 6.6743e-20;
    M_SUN = 1.9884e30;
    GM_SUN = G * M_SUN;

    planet_name = {'earth','mars','jupiter','saturn','uranus','neptune'};
    planet_GM = struct( ...
        'mars', 6.4185e23 * G, ...
        'jupiter', 1.8982e27 * G, ...
        'saturn', 5.6832e26 * G, ...
        'uranus', 8.6811e25 * G, ...
        'neptune', 1.0241e26 * G, ...
        'earth', 5.9722e24 * G ...
    );
    planet_radius = struct( ...
        'mars', 3376.2, ...
        'jupiter', 66854, ...
        'saturn', 58232, ...
        'uranus', 25362, ...
        'neptune', 24622, ...
        'earth', 6371, ...
        'sun', 5e7 ...
    );

    % Load trajectories
    trajectories = get_trajectory();

    % Initial state
    start_time = 2433283;
    dt = 3600;
    state = [start_time, trajectories.earth(num2str(start_time)), 0]; % [time, x, y, z, vx, vy, vz, fired]
    spacecraft = Spacecraft(state, trajectories, planet_GM, planet_radius, GM_SUN);

    traj = zeros(1000, 3);
    tic;
    for i = 1:1000
        spacecraft = spacecraft.step([0 0 0 1], dt);
        traj(i, :) = spacecraft.pos;
    end

    % Plotting
    figure;
    ax = axes('NextPlot','add');
    hold on;
    plot_trajectory(ax, traj, 1e9);
    plot_planet_trajectory(ax, trajectories, planet_name, start_time, start_time+1000/3600, 1e9);
    legend;
    hold off;
end