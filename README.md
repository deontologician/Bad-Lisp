Bad-Lisp
========

An implementation of lisp, given no real experience with lisp, from a half
remembered version of its overall concept

Mission Statement
-----------------

I've often read that lisp is an easy language to implement. And it makes
intuitive sense knowing what I know about the language. First, it's syntax is
extremely easy to parse, it's just a bunch of parentheses (Some say that lisp
has "no syntax". Sorry, this isn't true. Matching parentheses to arbitrary
depths requires a push-down automata to parse, which is equivalent to a context
free grammar. The grammar is extremely simple, but it is still a grammar.)
Anyways, so the grammar is simple and homogenous ("homoiconic") which
facilitates the second big part of lisp, which is the powerful macro
system. Macros in languages like the C preprocessor don't have quite the power
of lisp macros because they can't directly manipulate the syntax tree. In other
words, the explicit parens in lisp ensure that macros can work on the syntax
tree structure of a lisp program instead of unintelligently cutting and pasting
symbols at the lexical level like most macro languages. That doesn't mean lisp
macros ensure that the resulting program is semantically meaningful, but it does
mean it is syntactically correct. The third large conceptual aspect of lisp in
my mind is its dynamic nature. That means that not only do we need to implement
some sort of dynamic typing, but we also need to implement "eval" in the
language itself so that we can take advantage of the "code is data and data is
code" isomorphism.

So knowing these three high-level concepts behind lisp, can I implement a simple
lisp without the guiding hand of experience? It seems simple enough, but as we
all know the devil is in the details. Certainly, there are a hundred tutorials
out there on implementing simple lisps, and I'm guessing many of them make use
of important lessons learned after a half-century of lisp implementors tinkering
and improving and often completely rewriting the language from the ground up. I
will be making use of none of those lessons directly, although I have had some
training in programming language design and implementation, and in compiler
design.

Everything I Know About Lisp Going Into This
---------------------------------------------

I'd better lay on the line what I know currently about lisp (at the time of
beginning this project).
 * Lisp uses parens to make the syntax tree explicit
 * Lisp macros do replacement making use of the syntax tree
 * Lisp's basic structure is the S-expression, which is essentially a list
 * Lisp is a dynamic language with access to its own interpreter from within the
   code (eval)
 * We can implement a small number of basic control structures and data
   declarations and allow more complexity to be defined through macros
 * Lisp uses a prefix notation for everything. So (+ 3 2) instead of (3 + 2)
 * Lisp usually has a "quote" mechanism to prevent a string from being
   interpreted as code and instead evaluates to the unquoted string. At least, I
   think that's how it works.

That's pretty much it. I'd say I know enough to get myself into trouble
implementing a lisp interpreter. I don't even know really what the common
keywords are other than defmacro.

Design Choices
--------------

### Scoping

Lexical scoping. Definitely.

### Bad-Lisp Constructs

What's the minimum that I need for a lisp?

I need some way to create variables, set variables, and functions

```lisp
(var var-name initial-value) ; introduce and initialize a variable
(set var-name new-value)     ; set variable to a new value
(def function-name (arg-list) body) ; function definition
(function-name [args ...]) ; application
(lambda arg-list body)     ; anonymous function
```

Also, some way to loop and branch is important:

```lisp
(if condition then-branch else-branch)     ; if-then-else
(for initialize condition after-loop body) ; for loop
```
    
And, of course, some built in way to do IO:

```lisp
(read filename-or-stdin)
(write filename-or-stdout string-to-write)
```
    
Also, we need some simple arithmetic and boolean operators as well as string
operators:
 
```lisp
(3,000,000)     ; integer (commas are legal and ignored)
(true)  ; boolean
(false) ; boolean
('a')   ; character
("a string") ; short for ('a' ' ' 's' 't' 'r' 'i' 'n' 'g')
(`quoted) ; quoted value, evaluates to itself without the backtick
(+ x y [z ...]) ; addition (allows repetition since associative)
(- x y) ; subtraction (no repetition)
(* x y [z ...]) ; multiplication (allows repetition)
(^ x y) ; exponentiation
(/ x y) ; division
(< x y) ; less-than
(> x y) ; greater-than
(= x y) ; equality
(and clause-1 clause-2 [clause-3 ...]) ; logical AND
(or clause-1 clause-2 [clause-3 ...])  ; logical OR
```
    
Of course, we can't neglect the list, the fundamental data structure:

```lisp
()      ; empty list
(3 'a' x) ; list of integer, char, and variable
(hd list) ; get first element of a list
(tl list) ; get all elements but the first of a list
(ht 3 4 5 6) ; split a list by head and tail => (3 (4 5 6))
(cons 3 (2 4)) ; joins a head and tail => (3 2 4)
```

Now to macros... Hmm. Well, I guess these are really just like functions, except
they are replaced before evaluation instead of during it. This essentially means
macros are functions whose arguments are evaluated lazily, instead of eagerly
like regular functions arguments. At least that's how I see it naively. Let's
try that and see if it works.

```lisp
(defmacro macro-name (macro-args) body)
```

The strategy is, at runtime I'll run through and pick up all defmacro blocks,
and do macro replacement for all statements at the same level or lower in the
syntax tree, and the defmacro list will just be annihilated. So for example:

```lisp
(if (< 3 4)
  ((defmacro foo (x y) (= x y))
   (foo (+ 1 2) (- 3 4)))
  (foo 3 4)
)
```
    
This will be macro expanded to:

```lisp
(if (< 3 4)
  ((= (+ 1 2) (- 3 4)))
  (foo 3 4)
)
```
   
The foo function in the else branch won't be expanded with the macro since it
was not in a sibling branch of the syntax tree or below. So in other words,
macro definitions will be scoped just like function definitions are. In fact,
let's go crazy and just allow anonymous macros as well:

```lisp
((lambdamac (x) (x x x)) (+ 3 4))
=>
(((+ 3 4) (+ 3 4) (+ 3 4)))
```
