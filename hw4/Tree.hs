---------------------------------------------------------------------
--
-- CAS CS 320, Fall 2014
-- Assignment 4
-- Tree.hs
--
-- Mahir Gulrajani
-- Credits: Professor Lapets
--

data Tree =
    Leaf
  | Twig
  | Branch Tree Tree Tree
  deriving (Eq, Show);

-- twigs(Leaf)
-- returns 0
-- twigs(Twig)
-- returns 1
-- twigs(Branch Twig Leaf (Branch Twig Twig Leaf))
-- returns 3
-- twigs ( Branch (Branch Twig Twig Twig) (Branch Twig Twig (Branch Twig Twig (Branch Leaf Twig Leaf))) Twig )
-- returns 9
twigs :: Tree -> Integer
twigs ( Leaf ) = 0; -- Base case #1
twigs ( Twig ) = 1; -- Base case #1
twigs ( Branch t t1 t2 ) = twigs(t) + twigs(t1) + twigs(t2);

-- branches (Branch Leaf (Branch Twig Leaf Leaf) Leaf)
-- returns 2
-- branches (Branch Leaf (Branch Twig Leaf Leaf) (Branch Twig Twig (Branch Twig Twig Leaf)))
-- returns 4
branches :: Tree -> Integer
branches ( Leaf ) = 0;
branches ( Twig ) = 0;
branches ( Branch t t1 t2 ) = 1 + branches(t) + branches(t1) + branches(t2);

-- height (Branch (Branch Leaf Leaf Twig) (Branch Leaf Leaf Leaf) Leaf)
-- returns 3
-- height (Branch Leaf Leaf (Branch Twig Twig (Branch Twig Twig Twig)))
-- returns 4
-- height (Branch Twig Leaf (Branch Leaf Leaf (Branch Twig Twig (Branch Twig Twig Twig))))
-- returns 5
height :: Tree -> Integer
height ( Leaf ) = 0;
height ( Twig ) = 1;
height ( Branch t t1 t2 ) = 1 + maximum[height(t), height(t1), height(t2)];

-- perfect (Branch (Branch Leaf Leaf Leaf) Leaf Leaf)
-- returns False
-- perfect (Branch Twig Twig Twig)
-- returns False
-- perfect (Branch (Branch Leaf Leaf Leaf) (Branch Leaf Leaf Leaf) (Branch Leaf Leaf Leaf))
-- returns True
-- perfect (Branch (Branch Leaf Leaf Leaf) (Branch Leaf Leaf Leaf) (Branch Leaf Leaf Twig))
-- returns False
perfect :: Tree -> Bool
perfect ( Leaf ) = True;
perfect ( Twig ) = False;
perfect ( Branch t t1 t2 ) = if ((height(t) == height(t1)) && (height(t1) == height(t2))) then perfect(t) && perfect(t1) && perfect(t2) else False;

-- degenerate (Branch (Branch Twig Leaf Leaf) Twig Leaf)
-- returns True
-- degenerate (Branch (Branch Leaf Leaf Leaf) Leaf (Branch Leaf Leaf Leaf))
-- returns False
degenerate :: Tree -> Bool
degenerate ( Leaf ) = True;
degenerate ( Twig ) = True;
degenerate ( Branch Leaf Leaf Leaf ) = True;
degenerate ( Branch Twig Twig Twig ) = True;
degenerate ( Branch t Leaf Leaf ) = degenerate(t);
degenerate ( Branch t Leaf Twig ) = degenerate(t);
degenerate ( Branch t Twig Leaf ) = degenerate(t);
degenerate ( Branch t Twig Twig ) = degenerate(t);
degenerate ( Branch Leaf t Leaf ) = degenerate(t);
degenerate ( Branch Leaf t Twig ) = degenerate(t);
degenerate ( Branch Twig t Leaf ) = degenerate(t);
degenerate ( Branch Twig t Twig ) = degenerate(t);
degenerate ( Branch Leaf Leaf t ) = degenerate(t);
degenerate ( Branch Leaf Twig t ) = degenerate(t);
degenerate ( Branch Twig Leaf t ) = degenerate(t);
degenerate ( Branch Twig Twig t ) = degenerate(t);
degenerate ( Branch t t1 t2 ) = False; -- Cases where there are more than one branch child

-- infinite tree without Leaf/Twig nodes
infinite :: Tree
infinite = Branch infinite infinite infinite;

--eof