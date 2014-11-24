---------------------------------------------------------------------
--
-- CAS CS 320, Fall 2014
-- Assignment 4
-- Term.hs
--
-- Mahir Gulrajani
-- Credits: Professor Lapets
--

data Term =
    Number Integer
  | Abs Term
  | Plus Term Term
  | Mult Term Term

-- evaluate (Plus (Number 1) (Number 2))
-- returns 3
-- evaluate (Mult (Number 4) (Abs (Plus (Number (-1)) (Number (-2)))))
-- return 12
evaluate :: Term -> Integer
evaluate (Number i) = i;
evaluate (Abs t) = abs(evaluate(t));
evaluate (Plus t t1) = evaluate(t) + evaluate(t1);
evaluate (Mult t t1) = evaluate(t) * evaluate(t1);

--eof