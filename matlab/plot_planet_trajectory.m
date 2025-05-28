function plot_planet_trajectory(ax1, ax2, planet_name, planet_traj, start_time, end_time, scale)
    % planet_traj is an N x 7 matrix: [t x y z vx vy vz]
    time_vals = planet_traj(:,1);
    valid_idx = (time_vals <= end_time) & (time_vals >= start_time);
    rs = planet_traj(valid_idx, 2:4);
    plot(ax1, rs(:,1), rs(:,2), 'DisplayName', planet_name);
    plot(ax2, rs(:,1), rs(:,3), 'DisplayName', planet_name);
    % scatter3(ax, rs(1,1), rs(1,2), rs(1,3), 36, 'g', 'filled');
    % scatter3(ax, rs(end,1), rs(end,2), rs(end,3), 36, 'r', 'filled');
    % scatter3(ax, 0, 0, 0, 100, 'y', 'filled', 'DisplayName', 'sun');
    if isvector(scale) && length(scale) == 6
        xlim(ax1, [scale(1), scale(2)]);
        ylim(ax1, [scale(3), scale(4)]);
        xlim(ax2, [scale(1), scale(2)]);
        ylim(ax2, [scale(5), scale(6)]);
    elseif scale ~= 0
        xlim(ax1, [-scale, scale]);
        ylim(ax1, [-scale, scale]);
        xlim(ax2, [-scale, scale]);
        ylim(ax2, [-scale, scale]);
    end
end