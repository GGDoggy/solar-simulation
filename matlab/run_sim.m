function [traj_history, vel_history, acc_history] = run_sim(spacecraft, fire_time, fire_delay, end_time, init_vel, acc_strategy, trajectory_data, dt, close_dt)
    acc_ptr = 0;
    apply_time = fire_delay;
    action = zeros(1,7);
    traj_history = [];
    vel_history = [];
    acc_history = [];
    have_acc = false;
    close = false;
    while spacecraft.time_index <= end_time
        time = spacecraft.time_index;
        if time == fire_time
            action(4) = 1;
            action(5:7) = init_vel;
        end
        if apply_time == 0
            acc_ptr = acc_ptr + 1;
            apply_time = acc_strategy{acc_ptr}{1};
            if isequal(acc_strategy{acc_ptr}{2}, 'wait')
                have_acc = false;
                close = false;
                action(1:3) = [0, 0, 0];
            elseif isequal(acc_strategy{acc_ptr}{2}, 'close')
                apply_time = 3600;
                spacecraft.close_counter = 0;
                close_targ = acc_strategy{acc_ptr}{3};
                close = true;
            elseif isequal(acc_strategy{acc_ptr}{3}, 'z')
                action(1:3) = [0, 0, acc_strategy{acc_ptr}{2}];
            else
                have_acc = true;
            end
        end
        if have_acc
            planet_name = acc_strategy{acc_ptr}{5};
            planet_map = trajectory_data.(planet_name);
            time_key = num2str(spacecraft.time_list(time));
            planet_state = planet_map(time_key);
            planet_pos = planet_state(2:4);
            disp_vec = planet_pos - spacecraft.pos;
            vel = spacecraft.vel;
            n_vel = vel / norm(vel);
            n_right = disp_vec - dot(disp_vec, n_vel) * n_vel;
            n_right = n_right / norm(n_right);
            n_3 = cross(n_vel, n_right);
            acc = cell2mat(acc_strategy{acc_ptr}(2:4));
            basis = [n_vel(:), n_right(:), n_3(:)];
            acc_xyz = inv(basis) * acc(:);
            action(1:3) = acc_xyz(:)';
        end
        if close
            spacecraft.step(action, close_dt, true, close_targ);
        else
            spacecraft.step(action, dt);
        end
        if time > fire_time
            traj_history = [traj_history; spacecraft.pos];
            vel_history = [vel_history; spacecraft.vel];
            acc_history = [acc_history; action(1:3)];
        end
        apply_time = apply_time - 1;
    end
end