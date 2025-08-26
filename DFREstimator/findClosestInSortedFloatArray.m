function result = findClosestInSortedFloatArray(arr, target)
    % arr must be sorted ascending
    % result will be a struct with fields: element, index
    
    n = length(arr);

    % Average step shortcut
    avgStep = (arr(n) - arr(1)) / (n - 1);

    % Initial guess
    idx = floor((target - arr(1)) / avgStep) + 1; % MATLAB is 1-based

    % Clamp to valid range
    if idx < 1
        idx = 1;
    elseif idx >= n
        idx = n-1;
    end

    % Local search: only check idx and idx+1
    diff0 = arr(idx) - target;
    diff1 = arr(idx+1) - target;

    if diff0*diff0 <= diff1*diff1
        result.index = idx;
        result.element = arr(idx);
    else
        result.index = idx + 1;
        result.element = arr(idx+1);
    end
    
end


