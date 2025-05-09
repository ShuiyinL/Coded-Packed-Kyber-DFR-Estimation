function y = CompressQ(x,q,d)
if 2^d < q
    y=round(2^d/q*x);
    %y=mod(round(2^d/q*x),2^d);
else
    y=mod(x,q);
end

end

