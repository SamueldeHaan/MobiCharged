
function y = unknown_poly_type(x1, x2, x3, x4)
    a = - 5;
    b = 5;
    f = x1^3 + x1*x2^2 - x2*x3*x4 + x3^2*x1*x4 + x4^2;
    r = a + (b-a).*rand(100,1);
    y = f + mean(r);
end
