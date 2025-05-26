classdef Conditions < handle
    properties
        fire_delay
        fire_time
        run_time
        end_time
        trajectory_data
        init_vel
        acc_strategy
        first
        change_rate
        start_time
        scale
        dt
        close_dt
        spacecraft
    end
    methods
        function obj = Conditions(fire_delay, run_time, trajectory_data, change_rate, start_time, scale, dt, close_dt)
            obj.start_time = start_time;
            obj.fire_delay = fire_delay;
            obj.fire_time = fire_delay + 1;
            obj.run_time = run_time;
            obj.end_time = obj.fire_time + run_time;
            obj.trajectory_data = trajectory_data;
            obj.init_vel = zeros(1,3);
            obj.get_acc();
            obj.first = true;
            obj.change_rate = change_rate;
            obj.scale = scale;
            obj.dt = dt;
            obj.close_dt = close_dt;
        end
        
        function add_fire_delay(obj, ax)
            obj.fire_delay = obj.fire_delay + obj.change_rate;
            obj.fire_time = obj.fire_time + obj.change_rate;
            obj.end_time = obj.end_time + obj.change_rate;
            obj.first = false;
            obj.sim(ax);
        end
        
        function sub_fire_delay(obj, ax)
            obj.fire_delay = obj.fire_delay - obj.change_rate;
            obj.fire_time = obj.fire_time - obj.change_rate;
            obj.end_time = obj.end_time - obj.change_rate;
            obj.first = false;
            obj.sim(ax);
        end
        
        function add_run_time(obj, ax)
            obj.run_time = obj.run_time + obj.change_rate;
            obj.end_time = obj.end_time + obj.change_rate;
            obj.first = false;
            obj.sim(ax);
        end
        
        function sub_run_time(obj, ax)
            obj.run_time = obj.run_time - obj.change_rate;
            obj.end_time = obj.end_time - obj.change_rate;
            obj.first = false;
            obj.sim(ax);
        end
        
        function update_acc(obj, ax)
            obj.get_acc();
            obj.first = false;
            obj.sim(ax);
        end
        
        function get_acc(obj)
            s = fileread('acc_strg.json');
            obj.acc_strategy = jsondecode(s);
        end
        
        function [traj_history, vel_history, acc_history] = sim(obj, ax)
            temp = obj.trajectory_data.earth;
            key = num2str(obj.start_time);
            obj.spacecraft = Spacecraft([temp(key), 0], obj.trajectory_data);
            [traj_history, vel_history, acc_history] = run_sim(obj.spacecraft, obj.fire_time, obj.fire_delay, obj.end_time, obj.init_vel, obj.acc_strategy, obj.trajectory_data, obj.dt, obj.close_dt);
            disp([obj.fire_delay, obj.run_time]);
            if ~obj.first
                xlim = get(ax, 'XLim');
                ylim = get(ax, 'YLim');
                zlim = get(ax, 'ZLim');
            end
            cla(ax);
            plot_trajectory(ax, traj_history, obj.scale);
            planet_names = fieldnames(obj.trajectory_data);
            for i = 1:numel(planet_names)
                planet = planet_names{i};
                planet_map = obj.trajectory_data.(planet);
                keys_list = keys(planet_map);
                planet_traj = cell2mat(values(planet_map, keys_list))';
                planet_traj = reshape(planet_traj, 7, [])';
                plot_planet_trajectory(ax, planet, planet_traj, obj.spacecraft.time_list(obj.fire_time), obj.spacecraft.time_list(obj.end_time), obj.scale);
            end
            if ~obj.first
                set(ax, 'XLim', xlim);
                set(ax, 'YLim', ylim);
                set(ax, 'ZLim', zlim);
            end
        end
    end
end