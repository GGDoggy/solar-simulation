function ret = get_trajectory()
    % each as [N x 4] arrays (time, x, y, z)
    data = load('planet_trajectories.mat');
    planet_names = fieldnames(data);
    ret = struct();
    for i = 1:length(planet_names)
        planet = planet_names{i};
        ret.(planet) = gene_state_table(data.(planet));
    end
end