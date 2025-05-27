classdef Spacecraft < handle
    properties
        time
        pos
        vel
        fired
        planet_trajectories
        planets
        too_close
        distance
        time_list
        time_index
        acc
        close_counter
        planet_GM
        planet_radius
        GM_SUN
    end
    methods
        function obj = Spacecraft(state, planet_trajectories)
            obj.time = state(1);
            obj.pos = state(2:4);
            obj.vel = state(5:7);
            obj.fired = state(8);
            obj.planet_trajectories = planet_trajectories;
            obj.planets = fieldnames(planet_trajectories);
            obj.too_close = false;
            obj.distance = struct();
            obj.time_list = str2double(keys(planet_trajectories.(obj.planets{1})));
            obj.time_index = find(obj.time_list == obj.time, 1);
            obj.acc = [0 0 0];
            obj.close_counter = 0;
            G = 6.6743e-20;
            obj.planet_GM = struct( ...
                            'earth', 5.9722e24 * G, ...
                            'mars', 6.4185e23 * G, ...
                            'jupiter', 1.8982e27 * G, ...
                            'saturn', 5.6832e26 * G, ...
                            'uranus', 8.6811e25 * G, ...
                            'neptune', 1.0241e26 * G ...
                            );
            obj.GM_SUN = 1.9884e30 * G;
            obj.planet_radius = struct( ...
                            'earth', 6371, ...
                            'mars', 3376.2, ...
                            'jupiter', 66854, ...
                            'saturn', 58232, ...
                            'uranus', 25362, ...
                            'neptune', 24622, ...
                            'sun', 5e7 ...
                            );
        end

        function obj = update_acc(obj, action_acc)
            norm_pos = norm(obj.pos);
            if norm_pos < obj.planet_radius.sun
                disp(['too close to sun with distance ', num2str(norm_pos)]);
                obj.too_close = true;
                obj.acc = -obj.GM_SUN / (obj.planet_radius.sun^2 * norm_pos) * obj.pos + action_acc;
            else
                obj.acc = -obj.GM_SUN / (norm_pos^3) * obj.pos + action_acc;
            end
            for i = 1:length(obj.planets)
                planet = obj.planets{i};
                pos = obj.planet_trajectories.(planet)(num2str(obj.time));
                r = pos(1:3) - obj.pos;
                r_norm = norm(r);
                obj.distance.(planet) = r_norm;
                if r_norm < obj.planet_radius.(planet)
                    disp(['too close to ', planet, ' with distance ', num2str(r_norm)]);
                    obj.too_close = true;
                    obj.acc = obj.acc + obj.planet_GM.(planet) / (obj.planet_radius.(planet)^2 * r_norm) * r;
                else
                    obj.acc = obj.acc + obj.planet_GM.(planet) / (r_norm^3) * r;
                end
            end
        end

        function obj = step(obj, action, dt)
            obj.time_index = obj.time_index + 1;
            obj.time = obj.time_list(obj.time_index);
            if obj.fired == 0
                if action(4) > 0
                    obj.fired = 1;
                    state = obj.planet_trajectories.earth(num2str(obj.time));
                    obj.pos = state(2:4);
                    obj.vel = state(5:7) + [0 0 0];
                    obj.pos = obj.pos + 8e4 * obj.pos / norm(obj.pos);
                else
                    state = obj.planet_trajectories.earth(num2str(obj.time));
                    obj.pos = state(2:4);
                    obj.vel = state(5:7);
                    return
                end
            end
            acc = action(1:3) * 5.6e-6;
            obj = obj.update_acc(acc);
            obj.vel = obj.vel + obj.acc * dt / 2;
            obj.pos = obj.pos + obj.vel * dt;
            obj = obj.update_acc(acc);
            obj.vel = obj.vel + obj.acc * dt / 2;
        end
    end
end