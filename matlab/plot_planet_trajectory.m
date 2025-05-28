function plot_planet_trajectory(ax1, ax2, planet_name, planet_traj, start_time, end_time, scale)
    % planet_traj is an N x 7 matrix: [t x y z vx vy vz]
    time_vals = planet_traj(:,1);
    valid_idx = (time_vals <= end_time) & (time_vals >= start_time);
    rs = planet_traj(valid_idx, 2:4);
    plot3(ax, rs(:,1), rs(:,2), rs(:,3), 'DisplayName', planet_name);
    % scatter3(ax, rs(1,1), rs(1,2), rs(1,3), 36, 'g', 'filled');
    % scatter3(ax, rs(end,1), rs(end,2), rs(end,3), 36, 'r', 'filled');
    scatter3(ax, 0, 0, 0, 100, 'y', 'filled', 'DisplayName', 'sun');
    if isvector(scale) && length(scale) == 6
        xlim([scale(1), scale(2)]);
        ylim([scale(3), scale(4)]);
        zlim([scale(5), scale(6)]);
    elseif scale ~= 0
        xlim([-scale, scale]);
        ylim([-scale, scale]);
        zlim([-scale, scale]);
    end
end