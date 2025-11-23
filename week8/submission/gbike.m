clear all;
close all;

alphaA = [3 4];
alphaB = [3 2];
move_cost = 10;
shift_cost = 2;
penalty_fee = 4;

decision_map = zeros(21, 21);
gamma_val = 0.9;

stable_flag = false;
iteration = 0;

while ~stable_flag
    value_grid = eval_policy(decision_map, alphaA, alphaB, move_cost, shift_cost, gamma_val, penalty_fee);
    [decision_map, stable_flag] = improve_policy(value_grid, decision_map, alphaA, alphaB, move_cost, shift_cost, gamma_val, penalty_fee);
    iteration = iteration + 1;
end

figure(1);
subplot(2, 1, 1); contour(decision_map, [-5:5]);
subplot(2, 1, 2); surf(value_grid);


function [new_pol, is_stable] = improve_policy(vtable, pol, aA, aB, rc, tc, g, pf)
[rows, cols] = size(pol);

vec = 0:cols-1;
Q1 = exp(-aA(1)) * (aA(1).^vec) ./ factorial(vec);
Q2 = exp(-aA(2)) * (aA(2).^vec) ./ factorial(vec);
Q3 = exp(-aB(1)) * (aB(1).^vec) ./ factorial(vec);
Q4 = exp(-aB(2)) * (aB(2).^vec) ./ factorial(vec);

is_stable = true;
prev = pol;

for x = 1:rows
    for y = 1:cols
        k1 = x-1; 
        k2 = y-1;

        lo = -min(min(k2, rows-1-k1), 5);
        hi = min(min(k1, cols-1-k2), 5);

        best_val = -inf;

        for act = lo:hi
            Rw = -max(0, abs(act) - 1) * tc;

            if k1 - act > 10
                Rw = Rw - pf;
            end
            if k2 + act > 10
                Rw = Rw - pf;
            end

            aggV = 0;
            nx = k1 - act; 
            ny = k2 + act;

            for a = 0:12
                for b = 0:14
                    lx = nx - min(a, nx);
                    ly = ny - min(b, ny);

                    for c = 0:12
                        for d = 0:9
                            fx = lx + min(c, 20 - lx);
                            fy = ly + min(d, 20 - ly);

                            prob = Q1(a+1) * Q2(b+1) * Q3(c+1) * Q4(d+1);

                            aggV = aggV + prob * vtable(fx+1, fy+1);

                            Rw = Rw + prob * (min(a, nx) + min(b, ny)) * rc;
                        end
                    end
                end
            end

            cur_val = Rw + g * aggV;

            if cur_val > best_val
                best_val = cur_val;
                pol(x, y) = act;
            end
        end
    end
end

if sum(sum(abs(prev - pol))) ~= 0
    is_stable = false;
end

new_pol = pol;
end


function V = eval_policy(pol, aA, aB, rc, tc, g, pf)
[rows, cols] = size(pol);

vec = 0:cols-1;
Q1 = exp(-aA(1)) * (aA(1).^vec) ./ factorial(vec);
Q2 = exp(-aA(2)) * (aA(2).^vec) ./ factorial(vec);
Q3 = exp(-aB(1)) * (aB(1).^vec) ./ factorial(vec);
Q4 = exp(-aB(2)) * (aB(2).^vec) ./ factorial(vec);

V = zeros(rows, cols);
gap = 10;
limit = 0.1;

while gap > limit
    prevV = V;

    for x = 1:rows
        for y = 1:cols
            k1 = x-1; 
            k2 = y-1;

            act = pol(x,y);

            nx = k1 - act;
            ny = k2 + act;

            Rw = -max(0, abs(act) - 1) * tc;

            if nx > 10
                Rw = Rw - pf;
            end
            if ny > 10
                Rw = Rw - pf;
            end

            aggV = 0;

            for a = 0:12
                for b = 0:14
                    lx = nx - min(a, nx);
                    ly = ny - min(b, ny);

                    for c = 0:12
                        for d = 0:9
                            fx = lx + min(c, 20 - lx);
                            fy = ly + min(d, 20 - ly);

                            prob = Q1(a+1) * Q2(b+1) * Q3(c+1) * Q4(d+1);

                            Rw = Rw + prob * (min(a, nx) + min(b, ny)) * rc;
                            aggV = aggV + prob * V(fx+1, fy+1);
                        end
                    end
                end
            end

            V(x,y) = Rw + g * aggV;
        end
    end

    gap = max(max(abs(prevV - V)));
end
end
