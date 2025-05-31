function plot_trajectory(ax1, ax2, trajectory, scale, color)
    drop_ratio = 0;
    start_plot = floor(size(trajectory,1) * drop_ratio) + 1;
    plot(ax1, trajectory(start_plot:end-1,1), trajectory(start_plot:end-1,2), 'DisplayName', 'Our Spacecraft', 'Color', color);
    plot(ax2, trajectory(start_plot:end-1,1), trajectory(start_plot:end-1,3), 'DisplayName', 'Our Spacecraft', 'Color', color);
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
    % scatter3(ax, trajectory(1,1), trajectory(1,2), trajectory(1,3), 36, 'orange', 'filled');
    % scatter3(ax, trajectory(end,1), trajectory(end,2), trajectory(end,3), 36, 'red', 'filled');
end