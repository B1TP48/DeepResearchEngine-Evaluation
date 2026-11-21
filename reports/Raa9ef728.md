# Explain PAC Learning Through Sample Guarantees

PAC learning describes when examples can support a reliable prediction rule: under stated assumptions, enough labeled examples let a learner produce a rule whose error on future examples is small with high probability. For a finite set of candidate rules in the **realizable** setting, a consistent learner has error at most \(\epsilon\) with probability at least \(1-\delta\) once it has at least \(\bigl(\ln|\mathcal H|+\ln(1/\delta)\bigr)/\epsilon\) examples ([Foundations of Machine Learning, Theorem 2.5](https://dlib.hust.edu.vn/bitstream/HUST/24963/1/OER000003225.pdf)). “Approximately correct” means the error is no more than \(\epsilon\); “probably” means this happens with probability at least \(1-\delta\) over the randomly drawn training sample ([Haussler, “Probably Approximately Correct Learning”](https://cdn.aaai.org/AAAI/1990/AAAI90-163.pdf)). The guarantee does not promise that every training sample succeeds or that predictions are right on every possible input ([Princeton lecture notes](https://www.cs.princeton.edu/courses/archive/spring16/cos511/lec2.pdf)). It assumes that examples are independently drawn from the same distribution, and that the target rule belongs to the candidate set ([Foundations of Machine Learning, §2.1](https://dlib.hust.edu.vn/bitstream/HUST/24963/1/OER000003225.pdf)). The proof shows how those assumptions, together with a finite number of candidate rules, limit the chance that a bad rule fits the examples by accident ([Foundations of Machine Learning, proof of Theorem 2.5](https://dlib.hust.edu.vn/bitstream/HUST/24963/1/OER000003225.pdf)).

## A learner learns from labeled draws, not isolated facts

A supervised-learning example pairs an input \(x\) with its correct label \(y\). A **hypothesis** \(h\) is a candidate rule for predicting labels, and a **hypothesis class** \(\mathcal H\) is the set of rules the learner is allowed to consider ([University of Toronto, “Supervised Learning”](https://www.teach.cs.toronto.edu/~csc311notes/supervised_learning/supervised.html)). In the realizable PAC setup, an unknown target rule \(c^*\) supplies the labels. The learner receives examples drawn independently from the same distribution \(\mathcal D\), meaning each draw follows the same chances and does not affect the others ([Cornell, “PAC Learning”](https://www.cs.cornell.edu/courses/cs6781/2020sp/lectures/03-pac1.pdf)):

\[
x_i\sim\mathcal D,\qquad y_i=c^*(x_i),\qquad
S=((x_1,y_1),\ldots,(x_m,y_m)),\qquad h=\mathcal A(S).
\]

Here \(x_i\) is an input, \(y_i\) its label, \(m\) the number of examples, \(S\) the training sample, and \(\mathcal A\) the learning algorithm that returns hypothesis \(h\) ([University of Toronto, “Supervised Learning”](https://www.teach.cs.toronto.edu/~csc311notes/supervised_learning/supervised.html); [Cornell, “PAC Learning”](https://www.cs.cornell.edu/courses/cs6781/2020sp/lectures/03-pac1.pdf)). The distribution \(\mathcal D\) says how likely different inputs are; inputs need not be equally likely.

A hypothesis’s **true error** is the chance that it disagrees with the target on a fresh input drawn from \(\mathcal D\):

\[
\operatorname{err}_{\mathcal D}(h)
=\Pr_{x\sim\mathcal D}[h(x)\ne c^*(x)].
\]

The notation \(x\sim\mathcal D\) means “draw \(x\) according to \(\mathcal D\),” and the event inside the probability is that the candidate and target give different labels ([Cornell, “PAC Learning”](https://www.cs.cornell.edu/courses/cs6781/2020sp/lectures/03-pac1.pdf); [CMU, “8803 Machine Learning Theory,” Lecture 2](https://www.cs.cmu.edu/~ninamf/ML10/lect0114.pdf)). For a discrete set of possible inputs, this can also be written as a weighted sum:

\[
\operatorname{err}_{\mathcal D}(h)
=\sum_{x\in\mathcal X}\mathcal D(x)\,
\mathbf 1\{h(x)\ne c^*(x)\}.
\]

Each input contributes its chance of being drawn, \(\mathcal D(x)\), if the hypothesis is wrong on it; the indicator \(\mathbf 1\{\cdot\}\) equals \(1\) when its condition is true and \(0\) otherwise. Adding those contributions gives the total chance of an error ([Cornell, “PAC Learning”](https://www.cs.cornell.edu/courses/cs6781/2020sp/lectures/03-pac1.pdf)).

The **empirical error** is the fraction of the observed examples that the hypothesis gets wrong:

\[
\operatorname{err}_{S}(h)
=\frac{1}{m}\sum_{i=1}^{m}\mathbf 1\{h(x_i)\ne y_i\}.
\]

Each indicator counts one mistake as \(1\) and a correct prediction as \(0\); summing counts the mistakes, and dividing by the number of examples \(m\) gives the fraction of mistakes in the sample ([Cornell, “PAC Learning”](https://www.cs.cornell.edu/courses/cs6781/2020sp/lectures/03-pac1.pdf)). A hypothesis is **consistent** with the sample when this empirical error is zero.

## PAC separates accuracy from confidence

The basic PAC success condition is

\[
\Pr_{S}\!\left[
\operatorname{err}_{\mathcal D}(\mathcal A(S))\le\epsilon
\right]\ge 1-\delta.
\]

Read the inside first: the hypothesis returned from sample \(S\) has true error at most \(\epsilon\). The outer probability describes how often that happens across randomly drawn training samples. Thus, \(\epsilon\) is the allowed error, while \(\delta\) is the allowed chance of failing the guarantee; the confidence level is \(1-\delta\) ([Cornell, “PAC Learning”](https://www.cs.cornell.edu/courses/cs6781/2020sp/lectures/03-pac1.pdf); [Haussler, “Probably Approximately Correct Learning”](https://cdn.aaai.org/AAAI/1990/AAAI90-163.pdf)). A smaller \(\epsilon\) demands more accuracy; a smaller \(\delta\) demands greater confidence.

The finite-class sample guarantee applies when the target rule is in \(\mathcal H\), examples are independently drawn from one fixed distribution and labeled by that target, and the learner returns a hypothesis consistent with its sample. Under those assumptions, it is sufficient that

\[
m\ge \frac{\ln|\mathcal H|+\ln(1/\delta)}{\epsilon}
\]

to ensure that the returned hypothesis has true error at most \(\epsilon\) with probability at least \(1-\delta\) ([Foundations of Machine Learning, Theorem 2.5](https://dlib.hust.edu.vn/bitstream/HUST/24963/1/OER000003225.pdf)). Here \(|\mathcal H|\) is the number of candidate rules, and \(\ln\) is the natural logarithm. “Sufficient” matters: the bound says this many examples guarantee the stated result under the assumptions, not that this is always the smallest sample that could work.

## A union bound turns hidden mistakes into a sample size

The proof first considers one bad hypothesis: a rule whose true error is greater than \(\epsilon\). Such a rule is wrong on more than an \(\epsilon\) fraction of the input distribution. For one random example, the chance it avoids that rule’s errors is \(1-\operatorname{err}_{\mathcal D}(h)\); independence means the chance that all \(m\) examples avoid its errors is the product of that chance across the draws:

\[
\Pr[h\text{ is consistent with }S]
=(1-\operatorname{err}_{\mathcal D}(h))^m
\le (1-\epsilon)^m
\le e^{-\epsilon m}.
\]

The last inequality uses \(1-t\le e^{-t}\) for \(t\ge0\), which gives a convenient exponential upper bound ([Foundations of Machine Learning, proof of Theorem 2.5](https://dlib.hust.edu.vn/bitstream/HUST/24963/1/OER000003225.pdf); [CMU, Introduction to Machine Learning, Recitation 13](https://www.cs.cmu.edu/~10315-s20/recitation/rec13_sol.pdf)). This is the chance that one fixed bad rule escapes detection, not yet the chance that any bad rule does.

There can be many bad rules, so the proof adds their individual survival probabilities. This is the **union bound**: the chance that at least one bad rule remains consistent is no more than the sum of the chances for each rule. It does not require those survival events to be independent ([Foundations of Machine Learning, proof of Theorem 2.5](https://dlib.hust.edu.vn/bitstream/HUST/24963/1/OER000003225.pdf)):

\[
\Pr[\text{some bad }h\text{ is consistent}]
\le |\mathcal H|e^{-\epsilon m}.
\]

The number of bad rules cannot exceed the total number \(|\mathcal H|\), which explains the class-size factor. To make the probability of failure no more than \(\delta\), require

\[
|\mathcal H|e^{-\epsilon m}\le\delta.
\]

Dividing by \(|\mathcal H|\) and taking natural logarithms gives
\(-\epsilon m\le\ln\delta-\ln|\mathcal H|\). Reversing the inequality when multiplying by \(-1\), then dividing by \(\epsilon>0\), yields

\[
m\ge\frac{\ln|\mathcal H|-\ln\delta}{\epsilon}
=\frac{\ln|\mathcal H|+\ln(1/\delta)}{\epsilon}
=\frac{1}{\epsilon}\ln\frac{|\mathcal H|}{\delta}.
\]

The logarithm appears because taking the logarithm solves the exponential inequality for \(m\); it makes the sample requirement grow logarithmically with the number of candidate rules ([Foundations of Machine Learning, proof and Theorem 2.5](https://dlib.hust.edu.vn/bitstream/HUST/24963/1/OER000003225.pdf); [Columbia lecture-note paper, Fact 3](https://www.cs.columbia.edu/~rocco/Public/hs6.pdf)). Finally, if no bad hypothesis is consistent, every consistent output—including the learner’s choice—has error at most \(\epsilon\). Rounding the threshold up gives a whole-number sample size.

## Sixteen candidate rules illustrate what the bound promises

Imagine objects described by two yes-or-no features, such as “striped” and “round.” The features produce four possible combinations; a rule assigns either “yes” or “no” to each combination. There are \(2^4=16\) such rules because each of the four combinations has two possible labels ([UC Berkeley lecture notes](https://people.eecs.berkeley.edu/~nika/courses/cs272/f25/02-consistency-pac.pdf)). If the target is one of those rules, the setting is realizable, and the learner returns any rule consistent with the training examples, the finite-class guarantee applies.

For an allowed error of \(0.10\) and confidence of \(0.95\), the failure probability is \(\delta=0.05\). Substituting \(|\mathcal H|=16\) into the bound gives

\[
m\ge\frac{\ln(16)+\ln(1/0.05)}{0.10}
=\frac{\ln(16)+\ln(20)}{0.10}
=\frac{\ln(320)}{0.10}
\approx57.683.
\]

Because the sample must contain a whole number of examples and meet or exceed the threshold, round up to **58 examples** ([UC Berkeley lecture notes](https://people.eecs.berkeley.edu/~nika/courses/cs272/f25/02-consistency-pac.pdf); [IISc lecture notes](https://ece.iisc.ac.in/~parimal/2022/ml/lecture-07.pdf)). At that sample size, the bound on failure is \(16e^{-0.10(58)}\approx0.04844\), so the bound implies success probability of at least about \(0.95156\) ([UC Berkeley lecture notes](https://people.eecs.berkeley.edu/~nika/courses/cs272/f25/02-consistency-pac.pdf)). This is a guarantee across possible training samples, not a verdict about the result from any one particular sample.

The same formula shows how the requested guarantee affects the sufficient sample size. Doubling the candidate rules to \(32\), while keeping the error and confidence targets fixed, gives \(\lceil\ln(640)/0.10\rceil=65\) examples; tightening the error target to \(0.05\) gives \(\lceil\ln(320)/0.05\rceil=116\); and raising confidence to \(0.99\), so \(\delta=0.01\), gives \(\lceil\ln(1600)/0.10\rceil=74\) ([UC Berkeley lecture notes](https://people.eecs.berkeley.edu/~nika/courses/cs272/f25/02-consistency-pac.pdf)). The class size enters through a logarithm, the error tolerance through its reciprocal, and the failure probability through \(\ln(1/\delta)\) ([UC Berkeley lecture notes](https://people.eecs.berkeley.edu/~nika/courses/cs272/f25/02-consistency-pac.pdf)). These are sufficient bounds, not claims that those sample sizes are necessary for this particular example.

## Noisy labels call for a different guarantee

The finite-class proof relies on **realizability**: the target rule belongs to \(\mathcal H\), so there is a rule that fits every correctly labeled example. If labels are noisy or no candidate rule matches perfectly, that assumption may fail, and the consistent-learner guarantee does not automatically apply ([Foundations of Machine Learning, Theorem 2.5](https://dlib.hust.edu.vn/bitstream/HUST/24963/1/OER000003225.pdf); [University of Utah, Lecture 3](https://users.cs.utah.edu/~bhaskara/courses/theoryml/scribes/lecture3.pdf)).

In the **agnostic** setting, the aim is instead to perform nearly as well as the best rule in the class. A standard guarantee is

\[
R_D(\hat h)\le \inf_{h\in\mathcal H}R_D(h)+\epsilon
\]

with probability at least \(1-\delta\), where \(\hat h\) is the learned rule and \(R_D\) denotes true error under the labeled-data distribution ([University of Utah, Lecture 3](https://users.cs.utah.edu/~bhaskara/courses/theoryml/scribes/lecture3.pdf)). For a finite class, a uniform-deviation result states that every rule’s true and observed errors differ by at most \(\alpha\) with probability at least \(1-\delta\), provided

\[
m\ge\frac{1}{2\alpha^2}\ln\frac{2|\mathcal H|}{\delta}.
\]

This is a separate concentration result for the agnostic setting, not the realizable survival bound ([Illinois CS 574, “Theorem for Finite Hypothesis Classes (Agnostic Case)”](https://courses.grainger.illinois.edu/cs574/fa2025/notes/main.pdf)). To see how it yields the excess-error guarantee, let \(h^*\) be the best rule in the class and let \(\hat h\) minimize observed error. On the event that every rule’s true and observed errors differ by at most \(\alpha\),

\[
R_D(\hat h)
\le \widehat R_S(\hat h)+\alpha
\le \widehat R_S(h^*)+\alpha
\le R_D(h^*)+2\alpha.
\]

The first and last steps use the uniform error bound; the middle step follows because \(\hat h\) minimizes observed error. Choosing \(\alpha=\epsilon/2\) makes the excess error at most \(\epsilon\), and substitution into the sample bound gives

\[
m\ge\frac{2}{\epsilon^2}\ln\frac{2|\mathcal H|}{\delta}.
\]

This standard agnostic ERM bound has a \(1/\epsilon^2\) dependence, unlike the realizable finite-class bound’s \(1/\epsilon\) dependence, because the settings and guarantees differ ([Illinois CS 574, finite-class theorems](https://courses.grainger.illinois.edu/cs574/fa2025/notes/main.pdf)).

## Conclusion

PAC guarantees turn “learn from examples” into a precise claim: the sample must be random in the specified way, the learner must meet the theorem’s conditions, and the guarantee concerns typical performance on future draws from the same distribution. The finite-class result is useful because its proof makes the tradeoffs visible, but its sample count alone does not establish that a suitable rule can be found efficiently ([IISc lecture notes](https://ece.iisc.ac.in/~parimal/2022/ml/lecture-07.pdf); [Columbia lecture notes](https://www.cs.columbia.edu/~aho/cs3261/Lectures/L22-Introduction_to_PAC_Learning.html)).

In practice, the central question is therefore not just “How many examples?” but “Which assumptions make this bound relevant?” If the target is outside the class, labels are noisy, or future examples come from a different distribution, the realizable guarantee does not certify performance in that changed setting ([University of Utah, Lecture 3](https://users.cs.utah.edu/~bhaskara/courses/theoryml/scribes/lecture3.pdf); [IISc lecture notes](https://ece.iisc.ac.in/~parimal/2022/ml/lecture-07.pdf)).
