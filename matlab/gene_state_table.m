% may be useless
function ret = gene_state_table(states)
    % states: [N x 4] array, first column is time
    ret = containers.Map('KeyType','char','ValueType','any');
    for i = 1:size(states,1)
        t = states(i,1);
        add = states(i,:);
        ret(num2str(t)) = add;
    end
end