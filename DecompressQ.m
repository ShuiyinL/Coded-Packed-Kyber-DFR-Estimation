function y = DecompressQ(x,q,d)
if 2^d<q
    y=round(q/2^d*x);
      
else
    y=x;
end
end

