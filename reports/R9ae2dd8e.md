# PAC Learning Guarantees Accuracy From Examples

There is no single named “PAC theorem” in machine learning. Probably Approximately Correct (PAC) is a framework, or model, introduced by Leslie Valiant in 1984 ([ACM DL](https://dl.acm.org/doi/10.1145/1968.1972); [Servedio](https://dl.acm.org/doi/10.1145/3749740.3749754)); what exists at theorem level is a family of sample-complexity results and a characterisation standardly called the Fundamental Theorem of PAC Learning ([Blumer et al.](https://dl.acm.org/doi/10.1145/76359.76371); [Weizmann Institute notes](https://www.wisdom.weizmann.ac.il/~ethanf/teaching/ItSLT_15/lectures/lec4-no_anim.pdf)). The framework asks how many labelled examples a learner needs before its output rule can be trusted on new examples from the same unknown source. Its guarantee is deliberately double: roughly correct, with true error at most ε, and probably so, with failure chance at most δ. That double hedge is why PAC is useful and why it is often misread: it is a worst-case, distribution-free promise, not a prediction for one dataset ([Wikipedia](http://en.wikipedia.org/api/rest_v1/page/pdf/Probably_approximately_correct_learning); [Sharif lecture notes](https://sharif.edu/~beigy/courses/14002/40718/Lect-3.pdf)). The practical cost of that strength is visible in modern machine learning, where capacity bounds are often loose or vacuous for deep networks ([Zhang et al., CACM](https://dl.acm.org/doi/fullHtml/10.1145/3446776); [MIT 6.7960](https://ocw.mit.edu/courses/6-7960-deep-learning-fall-2024/mit6_7960f24_lec06_captions.vtt)).

## PAC is a framework whose guarantee has two dials

Four objects have to be kept apart. The instance space \(X\) is the set of all possible examples; the unknown distribution \(D\) says how examples occur; the unknown labelling rule \(f\) (or target concept \(c\)) says how labels are assigned; and the hypothesis class \(H\) is the pool of candidate rules the learner is allowed to return ([Shalev-Shwartz & Ben-David, Ch. 3](https://www.cambridge.org/core/books/abs/understanding-machine-learning/formal-learning-model/94E1E4D2AC86897DF9B330977FF016B0); [Wikipedia](http://en.wikipedia.org/api/rest_v1/page/pdf/Probably_approximately_correct_learning)). In the realizable case, \(f\) is assumed to lie in \(H\); in the agnostic case labels may be noisy or \(f\) may lie outside \(H\), so the learner can only aim to be close to the best rule in \(H\) ([Sharif lecture notes](https://sharif.edu/~beigy/courses/14002/40718/Lect-3.pdf)). The true error of a rule \(h\) is the probability it mislabels a fresh example, \(R(h)=\Pr_{(x,y)\sim D}[h(x)\ne y]\); the training error is the fraction it gets wrong on the \(m\) examples seen, \(\hat R(h)=\frac1m\sum_{i=1}^m \mathbf{1}[h(x_i)\ne y_i]\) ([Sharif lecture notes](https://sharif.edu/~beigy/courses/14002/40718/Lect-3.pdf)). The i.i.d. requirement—each example drawn independently from the same distribution—is what makes training error an average of independent yes/no outcomes ([Princeton COS 511](https://www.cs.princeton.edu/courses/archive/spring13/cos511/scribe_notes/0212.pdf); [Sharif lecture notes](https://sharif.edu/~beigy/courses/14002/40718/Lect-3.pdf)).

ε is the accuracy parameter: the largest true error tolerated. δ is the confidence parameter: the largest probability of failing to meet that accuracy. The standard guarantee is

\[
\Pr_{S\sim D^m}\bigl[\,R(h_S)\le \varepsilon\,\bigr]\ge 1-\delta,
\]

where \(h_S\) is the rule returned after seeing sample \(S\) ([Shalev-Shwartz & Ben-David, Ch. 3](https://www.cambridge.org/core/books/abs/understanding-machine-learning/formal-learning-model/94E1E4D2AC86897DF9B330977FF016B0); [Princeton COS 511](https://www.cs.princeton.edu/courses/archive/spring13/cos511/scribe_notes/0212.pdf)). Read it as a statement about the training procedure: if the procedure were repeated on many independent samples, at least \(1-\delta\) of the returned rules would have true error at most ε. One lecture source states the requirement as error below ε with probability at least δ ([Razi University slides](https://en.razi.ac.ir/documents/10184/41979/Learning+Theory.pdf)); standard lecture and textbook statements use probability at least \(1-\delta\) ([UMass Boston slides](https://www.cs.umb.edu/~ding/classes/310_F23/slides/10_PAC.pdf); [Princeton COS 511](https://www.cs.princeton.edu/courses/archive/spring13/cos511/scribe_notes/0212.pdf)). This article follows \(1-\delta\) because δ is defined as the confidence parameter—how likely the classifier is to meet the accuracy requirement—so small δ must mean small failure, not small success; the “at least δ” form would make 99% failure acceptable when δ=0.01. Sources also differ on whether ε and δ may equal 0—the textbook writes \((0,1)\), while the Princeton notes write \(>0\)—a boundary detail that does not change the sample-size algebra ([Shalev-Shwartz & Ben-David, Ch. 3](https://www.cambridge.org/core/books/abs/understanding-machine-learning/formal-learning-model/94E1E4D2AC86897DF9B330977FF016B0); [Princeton COS 511](https://www.cs.princeton.edu/courses/archive/spring13/cos511/scribe_notes/0212.pdf)).

In the agnostic setting the target is not absolute error but excess error:

\[
\Pr_{S\sim D^m}\Bigl[\,R(h_S)\le \min_{h'\in H}R(h')+\varepsilon\,\Bigr]\ge 1-\delta.
\]

If the realizable assumption holds, agnostic PAC learning gives the same guarantee as PAC learning; if it fails, no learner can guarantee arbitrarily small error ([Sharif lecture notes](https://sharif.edu/~beigy/courses/14002/40718/Lect-3.pdf)).

## Finite classes turn the guarantee into a sample-size formula

For a finite class, the guarantee becomes arithmetic. The two tools are a concentration bound for one rule and a union bound over rules. For events \(A_1,\ldots,A_N\), the union bound is

\[
\Pr(A_1\cup\cdots\cup A_N)\le \sum_{i=1}^N \Pr(A_i).
\]

It follows from \(P(A\cup B)=P(A)+P(B)-P(A\cap B)\le P(A)+P(B)\), extended by induction; it does not require the events to be independent ([UCL slides](http://www0.cs.ucl.ac.uk/staff/M.Herbster/SL/13-5-class.pdf)).

For a fixed rule \(h\), each training example contributes a 0 or 1 mistake. Hoeffding’s inequality says the average of \(m\) independent bounded outcomes is unlikely to sit far from its expectation:

\[
\Pr\bigl[|\hat R(h)-R(h)|>\varepsilon\bigr]\le 2e^{-2m\varepsilon^2}.
\]

The intuition is coin flipping: if a coin has bias \(\mu\), the fraction of heads in \(m\) flips is probably close to \(\mu\), and the chance of a gap decays exponentially in \(m\) ([Sharif lecture notes](https://sharif.edu/~beigy/courses/14002/40718/Lect-3.pdf); [UCL slides](http://www0.cs.ucl.ac.uk/staff/M.Herbster/SL/13-5-class.pdf); [Mohri slides](https://cs.nyu.edu/~mohri/mls/ml_learning_with_finite_hypothesis_sets.pdf)). Applying the union bound over all \(|H|\) rules gives

\[
\Pr\bigl[\exists h\in H:\ |\hat R(h)-R(h)|>\varepsilon\bigr]\le 2|H|e^{-2m\varepsilon^2}.
\]

This is uniform convergence: the same ε holds for every rule at once, which is what allows the learner to choose a rule after seeing data ([Mohri slides](https://cs.nyu.edu/~mohri/mls/ml_learning_with_finite_hypothesis_sets.pdf); [UCL slides](http://www0.cs.ucl.ac.uk/staff/M.Herbster/SL/13-5-class.pdf)).

To get an excess-error guarantee, use the same bound at scale \(\varepsilon/2\):

\[
\Pr\bigl[\exists h:\ |\hat R(h)-R(h)|\ge \varepsilon/2\bigr]\le 2|H|e^{-m\varepsilon^2/2}.
\]

Set the right side equal to δ and solve:

\[
2|H|e^{-m\varepsilon^2/2}\le\delta
\quad\Longrightarrow\quad
-m\varepsilon^2/2\le \ln\frac{\delta}{2|H|}
\quad\Longrightarrow\quad
m\ge \frac{2}{\varepsilon^2}\ln\frac{2|H|}{\delta}
=\frac{2}{\varepsilon^2}\left(\ln|H|+\ln\frac{2}{\delta}\right).
\]

The algebra uses only \(\ln(ab)=\ln a+\ln b\) and \(-\ln(a/b)=\ln(b/a)\) ([Cornell CS 6781](https://www.cs.cornell.edu/courses/cs6781/2020sp/lectures/08-agnostic-bounds.pdf)). Let \(h^\star\) minimise true error and let \(h_{\rm ERM}\) minimise training error. If \(R(h_{\rm ERM})>R(h^\star)+\varepsilon\), uniform convergence gives

\[
\hat R(h_{\rm ERM})>R(h_{\rm ERM})-\varepsilon/2>R(h^\star)+\varepsilon/2>\hat R(h^\star),
\]

so \(h_{\rm ERM}\) could not have had the smallest training error. Therefore \(R(h_{\rm ERM})\le R(h^\star)+\varepsilon\) with probability at least \(1-\delta\) ([Cornell CS 6781](https://www.cs.cornell.edu/courses/cs6781/2020sp/lectures/08-agnostic-bounds.pdf)). Constants differ by proof route: Cornell’s excess-error version has \(2/\varepsilon^2(\ln|C|+\ln(2/\delta))\), while CMU’s uniform-gap version has \(1/(2\varepsilon^2)(\ln|H|+\ln(2/\delta))\)—a factor of four, because they promise different things ([Cornell CS 6781](https://www.cs.cornell.edu/courses/cs6781/2020sp/lectures/08-agnostic-bounds.pdf); [CMU 10-601](https://www.cs.cmu.edu/~10601-f20/lectures/10601_Fa20_Lecture_16_Learning_Theory.pdf)). The evidence does not single out an optimal constant; the numerical factors are artifacts of the union-bound bookkeeping.

The realizable case is cheaper. If a rule has true error greater than ε, the chance it agrees with one random example is less than \(1-\varepsilon\); because examples are independent, the chance it agrees with all \(m\) is less than \((1-\varepsilon)^m\). There are at most \(|H|\) such rules, so the union bound gives

\[
\Pr(\text{some bad rule is consistent})\le |H|(1-\varepsilon)^m\le |H|e^{-\varepsilon m},
\]

using \(1-x\le e^{-x}\). Set this to δ:

\[
|H|e^{-\varepsilon m}\le\delta
\quad\Longrightarrow\quad
\ln|H|-\varepsilon m\le\ln\delta
\quad\Longrightarrow\quad
m\ge \frac{\ln|H|+\ln(1/\delta)}{\varepsilon}.
\]

([Utah CS notes](https://users.cs.utah.edu/~zhe/teach/archived/2024f/pdf/5-learning-theory-framework.pdf); [UCSB Math CS 120](https://web.math.ucsb.edu/~atzberg/pmwiki_intranet/uploads/Teaching2018FallMachineLearningMATHCS120/ml_lecture_PAC_Learning_Atzberger.pdf); [CMU 10-601](https://www.cs.cmu.edu/~10601-f20/lectures/10601_Fa20_Lecture_16_Learning_Theory.pdf)). This standard derivation does not actually use Hoeffding; a Hoeffding-only route gives the weaker \(m\ge\frac{1}{2\varepsilon^2}(\ln|H|+\ln(1/\delta))\) ([UCL slides](http://www0.cs.ucl.ac.uk/staff/M.Herbster/SL/13-5-class.pdf)). Changing the logarithm base only rescales the bound.

| Setting | Enough examples in one standard form | What is promised | Source |
|---|---|---|---|
| Finite \(H\), realizable | \(m\ge \frac{\ln|H|+\ln(1/\delta)}{\varepsilon}\) | every rule with zero training error has true error at most ε | ([CMU 10-601](https://www.cs.cmu.edu/~10601-f20/lectures/10601_Fa20_Lecture_16_Learning_Theory.pdf); [UCSB](https://web.math.ucsb.edu/~atzberg/pmwiki_intranet/uploads/Teaching2018FallMachineLearningMATHCS120/ml_lecture_PAC_Learning_Atzberger.pdf)) |
| Finite \(H\), agnostic, uniform gap | \(m\ge \frac{1}{2\varepsilon^2}\left(\ln|H|+\ln\frac{2}{\delta}\right)\) | for every \(h\), \(|\hat R(h)-R(h)|\le\varepsilon\) | ([CMU 10-601](https://www.cs.cmu.edu/~10601-f20/lectures/10601_Fa20_Lecture_16_Learning_Theory.pdf)) |
| Finite \(H\), agnostic, excess error | \(m\ge \frac{2}{\varepsilon^2}\left(\ln|H|+\ln\frac{2}{\delta}\right)\) | ERM is within ε of the best rule in \(H\) | ([Cornell CS 6781](https://www.cs.cornell.edu/courses/cs6781/2020sp/lectures/08-agnostic-bounds.pdf)) |

For concreteness, take the class of conjunctions over six Boolean variables. There are \(3^6=729\) such conjunctions, because each variable can appear positive, negative, or not at all. With ε=0.1 and δ=0.05 the realizable formula gives \(m\ge(1/0.1)(\ln729+\ln20)\approx95.9\), about 96 examples ([USC CSCI-567](https://www-scf.usc.edu/~csci567/15-16-learning-theory.pdf)). At ε=δ=0.01 the same class needs about 1120 examples ([IISc](https://ece.iisc.ac.in/~parimal/2018/ml/lecture-08.pdf)), and ten variables need about 1560 ([Illinois State](https://www.itk.ilstu.edu//faculty/mecalif/ITK385/Spring2010/slides/385_2010_02_08.pdf)). The pattern is the lesson: \(m\) grows only logarithmically in \(|H|\) but linearly in \(1/\varepsilon\), so cutting ε in half roughly doubles the data, while squaring the number of candidate rules adds only a constant. One widely reused CMU slide labels 116 as the answer for \(3^{10}\) at ε=0.1 and δ=0.01, but substituting \(3^{10}\) into the printed formula gives about 156; the discrepancy is arithmetic, not a different theorem ([CMU 10-601 slides](http://www.cs.cmu.edu/~mgormley/courses/10601-f22//slides/lecture16-pac-ink-b.pdf)).

## VC dimension replaces class size when the class is infinite

For an infinite class, \(|H|\) is infinite and the finite union bound is useless ([Berkeley CS 272](https://people.eecs.berkeley.edu/~nika/courses/cs272/f25/03-pac.pdf); [Mohri slides](https://cs.nyu.edu/~mohri/mls/ml_learning_with_finite_hypothesis_sets.pdf)). The replacement is a combinatorial measure of richness. A set \(S\) is shattered by \(H\) if \(H\) can label \(S\) in every possible way. The VC dimension \(d={\rm VCdim}(H)\) is the size of the largest shattered set; if arbitrarily large sets can be shattered, \(d=\infty\) ([CMU 10-601 slides](http://www.cs.cmu.edu/%7etom/10601_fall2012/slides/PAC-learning1-10-11-2012_ANN.pdf); [UIUC ML Theory](http://mjt.web.engr.illinois.edu/courses/mlt-f18/lec22-handout.pdf)).

The growth function counts how many labelings \(H\) can produce on \(m\) points:

\[
\Pi_H(m)=\max_{S\subset X,\ |S|=m}\bigl|\{h|_S:h\in H\}\bigr|.
\]

It equals \(2^m\) for \(m\le d\), and Sauer’s lemma bounds it for \(m>d\):

\[
\Pi_H(m)\le\sum_{i=0}^{d}\binom{m}{i}\le\left(\frac{em}{d}\right)^d.
\]

([Oxford CLT notes](http://www.cs.ox.ac.uk/people/varun.kanade/teaching/CLT-MT2022/lectures/CLT.pdf); [Princeton COS 511](https://www.cs.princeton.edu/courses/archive/spring19/cos511/scribe_notes/0225.pdf); [MLSS Tübingen](http://mlss.tuebingen.mpg.de/2017/speaker_slides/Shai3.pdf)). The second inequality is the beginner-friendly part. Start from the binomial sum and multiply and divide by \((m/d)^d\):

\[
\sum_{i=0}^d\binom{m}{i}
=\left(\frac{m}{d}\right)^d\sum_{i=0}^d\binom{m}{i}\left(\frac{d}{m}\right)^d
\le\left(\frac{m}{d}\right)^d\sum_{i=0}^d\binom{m}{i}\left(\frac{d}{m}\right)^i
\le\left(\frac{m}{d}\right)^d\left(1+\frac{d}{m}\right)^m
\le\left(\frac{m}{d}\right)^d e^d
=\left(\frac{em}{d}\right)^d.
\]

The first inequality uses \(d/m\le1\) and \(i\le d\); the second is the binomial theorem; the third uses \(1+x\le e^x\) ([Oxford CLT notes](http://www.cs.ox.ac.uk/people/varun.kanade/teaching/CLT-MT2022/lectures/CLT.pdf)). Sauer’s lemma itself is proved by induction on \(m\) and \(d\): split the labelings of a set \(S\) into those that extend in only one way and those that extend in both ways after removing a point; the second family has VC dimension at most \(d-1\), which gives the binomial recursion \(\Phi(m,d)=\Phi(m-1,d)+\Phi(m-1,d-1)\) ([Oxford CLT notes](http://www.cs.ox.ac.uk/people/varun.kanade/teaching/CLT-MT2022/lectures/CLT.pdf); [Princeton COS 511](https://www.cs.princeton.edu/courses/archive/spring19/cos511/scribe_notes/0225.pdf)). Sources state slightly different boundary conditions for Sauer’s inequality—\(m\ge d\), \(n>d\), or \(m\ge d+2\)—but the difference is a boundary case ([Oxford CLT notes](http://www.cs.ox.ac.uk/people/varun.kanade/teaching/CLT-MT2022/lectures/CLT.pdf); [Loria notes](https://mlweb.loria.fr/book/en/SauerShelah.html); [Chicago REU paper](http://math.uchicago.edu/~may/REU2025/REUPapers/Wang,Luoqian.pdf)).

| Class | VC dimension | Beginner reason |
|---|---|---|
| Intervals on a line | 2 | Any 2 points can be labelled four ways; with 3, labelling the middle point negative and the outer two positive is impossible ([Oxford CLT notes](http://www.cs.ox.ac.uk/people/varun.kanade/teaching/CLT-MT2022/lectures/CLT.pdf)) |
| Axis-aligned rectangles in the plane | 4 | 4 extreme points can be shattered; any 5 points include a non-extreme point that can be labelled against the extremes ([Oxford CLT notes](http://www.cs.ox.ac.uk/people/varun.kanade/teaching/CLT-MT2022/lectures/CLT.pdf); [Princeton COS 511](https://www.cs.princeton.edu/courses/archive/spring19/cos511/scribe_notes/0225.pdf)) |
| Half-spaces in \(\mathbb{R}^n\) | \(n+1\) | 3 in the plane, and no 4; general form \(n+1\) ([Oxford CLT notes](http://www.cs.ox.ac.uk/people/varun.kanade/teaching/CLT-MT2022/lectures/CLT.pdf); [UIUC ML Theory](http://mjt.web.engr.illinois.edu/courses/mlt-f18/lec22-handout.pdf)) |
| Finite \(H\) | at most \(\log_2|H|\) | For thresholds on \(k\) points, \(|H|=k\) while VC dimension is 1 ([Shalev-Shwartz & Ben-David, p. 72](https://issuhub.com/view/index/1331?pageIndex=72)) |
| One-parameter \(\sin\) class | \(\infty\) | Parameter count is not VC dimension ([Shalev-Shwartz & Ben-David, p. 72](https://issuhub.com/view/index/1331?pageIndex=72)) |

For binary classification with 0–1 loss, the Fundamental Theorem of PAC Learning says the following are equivalent: \(H\) has uniform convergence; any ERM rule is a successful agnostic PAC learner; \(H\) is agnostically PAC learnable; \(H\) is PAC learnable; any ERM rule is a successful PAC learner; and \(H\) has finite VC dimension ([Shalev-Shwartz & Ben-David, p. 72](https://issuhub.com/view/index/1331?pageIndex=72); [MLSS Tübingen](http://mlss.tuebingen.mpg.de/2017/speaker_slides/Shai3.pdf)). In short, a class is learnable exactly when its VC dimension is finite, and the naive rule—pick any rule with near-zero training error—already succeeds ([Shalev-Shwartz & Ben-David, p. 72](https://issuhub.com/view/index/1331?pageIndex=72)). Finite VC dimension implies learnability through uniform convergence; learnability implies finite VC dimension through a no-free-lunch argument on a shattered set. If \({\rm VCdim}(H)=\infty\), there is a shattered set of size \(2m\); labels on half the points then carry no information about the other half, so no algorithm can succeed for ε<1/8 and δ<1/7 ([Weizmann Institute notes](https://www.wisdom.weizmann.ac.il/~ethanf/teaching/ItSLT_16/lectures/lec4_no_anim.pdf); [IIT Kharagpur](http://cse.iitkgp.ac.in/~pabitra/course/aml/Lec9-FTP.pdf)).

The quantitative version gives, for \(d={\rm VCdim}(H)<\infty\),

\[
m=O\!\left(\frac{d+\ln(1/\delta)}{\varepsilon^2}\right)
\]

for agnostic learning by ERM, and

\[
m=O\!\left(\frac{d\log(1/\varepsilon)+\ln(1/\delta)}{\varepsilon}\right)
\]

for realizable learning by a consistent rule ([MLSS Tübingen](http://mlss.tuebingen.mpg.de/2017/speaker_slides/Shai3.pdf); [Weizmann Institute notes](https://www.wisdom.weizmann.ac.il/~ethanf/teaching/ItSLT_15/lectures/lec4-no_anim.pdf); [Oxford CLT notes](http://www.cs.ox.ac.uk/people/varun.kanade/teaching/CLT-MT2022/lectures/CLT.pdf)). Sources differ on whether a \(\log(1/\varepsilon)\) factor appears: one textbook-style statement writes \(C(d+\ln(1/\delta))/\varepsilon\), while Oxford writes \((1/\varepsilon)(\ln(1/\delta)+d\log(1/\varepsilon))\) ([MLSS Tübingen](http://mlss.tuebingen.mpg.de/2017/speaker_slides/Shai3.pdf); [Oxford CLT notes](http://www.cs.ox.ac.uk/people/varun.kanade/teaching/CLT-MT2022/lectures/CLT.pdf)). The agnostic rate is tight in its dependence on \(d\) and \(1/\delta\): any PAC algorithm needs \(\Omega((d+\ln(1/\delta))/\varepsilon^2)\) ([Weizmann Institute notes](https://www.wisdom.weizmann.ac.il/~ethanf/teaching/ItSLT_16/lectures/lec4_no_anim.pdf)). Some agnostic upper bounds carry an extra \(\ln(1/\varepsilon)\), which a chaining proof removes, leaving \(O((d+\ln(1/\delta))/\varepsilon^2)\) ([Cornell CS 6781](https://www.cs.cornell.edu/courses/cs6781/2020sp/lectures/08-agnostic-bounds.pdf)). The realizable case improves \(1/\varepsilon^2\) to \(1/\varepsilon\) because a bad rule survives only if it is consistent with all \(m\) examples, an event of probability at most \((1-\varepsilon)^m\le e^{-\varepsilon m}\) rather than \(e^{-m\varepsilon^2}\) ([Oxford CLT notes](http://www.cs.ox.ac.uk/people/varun.kanade/teaching/CLT-MT2022/lectures/CLT.pdf)).

The standard sketch has four moves: fix one rule and use Hoeffding; union over the effective number of rules on a doubled sample, at most \(\Pi_H(2m)\); replace \(\Pi_H(2m)\) by Sauer’s bound \((2em/d)^d\); and solve a bound of the form

\[
2\left(\frac{2em}{d}\right)^d e^{-m\varepsilon^2/2}\le\delta
\]

for \(m\), which gives the displayed \(O((d+\ln(1/\delta))/\varepsilon^2)\) up to constants ([Oxford CLT notes](http://www.cs.ox.ac.uk/people/varun.kanade/teaching/CLT-MT2022/lectures/CLT.pdf); [CMU 10-601](https://www.cs.cmu.edu/~10601-f20/lectures/10601_Fa20_Lecture_16_Learning_Theory.pdf); [Cornell CS 6781](https://www.cs.cornell.edu/courses/cs6781/2020sp/lectures/08-agnostic-bounds.pdf)). The quantitative theorem leaves its absolute constants unspecified; the sources give no numerical values for them ([MLSS Tübingen](http://mlss.tuebingen.mpg.de/2017/speaker_slides/Shai3.pdf); [Shalev-Shwartz & Ben-David, p. 72](https://issuhub.com/view/index/1331?pageIndex=72)). The theorem is distribution-free: it must hold for every distribution, which is what makes it a worst-case guarantee and what makes it fail to describe practice outside that setting; a 2025 analysis says the distribution-free model is overly adversarial and that the traditional theorem fails beyond it ([PMLR 2025](https://proceedings.mlr.press/v272/hopkins25a.html)). The theorem as stated covers binary classification with 0–1 loss; regression needs a different capacity notion such as fat shattering ([Weizmann Institute notes](https://www.wisdom.weizmann.ac.il/~ethanf/teaching/ItSLT_16/lectures/lec4_no_anim.pdf)).

## Beginners should read PAC as a worst-case promise, not a prediction

The clearest beginner analogy is an urn. An urn has an unknown fraction \(\mu\) of red marbles; you draw \(m\) marbles independently and see fraction \(\nu\) red. It is possible to draw mostly green from a mostly red urn, but it is probable that \(\nu\) is close to \(\mu\). Hoeffding makes that precise: \(\Pr(|\nu-\mu|>\varepsilon)\le2e^{-2m\varepsilon^2}\), valid for all \(m\) and ε and independent of \(\mu\) ([Caltech, Learning from Data](https://work.caltech.edu/slides/slides02.pdf)). In learning, a marble is an example, red means “the rule got it wrong,” \(\mu\) is true error, and \(\nu\) is training error.

The analogy breaks at one crucial point: the rule was chosen after seeing the data, so its bin was not fixed in advance. Teachers patch this with “multiple bins,” one per hypothesis, and the union bound adds a factor of \(|H|\); the Caltech slides stop the reader with “h is fixed” before introducing that patch ([Caltech, Learning from Data](https://work.caltech.edu/slides/slides02.pdf)). The patch is deliberately crude: it ignores dependence between hypotheses that behave similarly, so it can be wildly pessimistic ([Caltech, Learning from Data](https://work.caltech.edu/slides/slides02.pdf); [argmin.net](https://www.argmin.net/p/three-paths-to-generalization)). The resulting imbalance is the whole PAC trade-off: failure probability falls exponentially with \(m\) but rises only linearly with the number of candidate rules, which is why adding hypotheses is cheaper than adding accuracy ([argmin.net](https://www.argmin.net/p/three-paths-to-generalization)).

Several misreadings are worth naming. PAC does not mean “always correct”: error up to ε is allowed. It does not mean “guaranteed on this run”: failure probability δ remains. The probability is over the random draw of the sample, not over hypotheses, datasets, or parameters, and it is not a statement about one returned rule ([Shalev-Shwartz & Ben-David, Ch. 3](https://www.cambridge.org/core/books/abs/understanding-machine-learning/formal-learning-model/94E1E4D2AC86897DF9B330977FF016B0)). The bound is worst-case over distributions, so it is not a prediction of error on one dataset, and its constants are typically loose ([AAAI-90](https://aaaipress.org/Papers/AAAI/1990/AAAI90-163.pdf); [Illinois State](https://www.itk.ilstu.edu//faculty/mecalif/ITK385/Spring2010/slides/385_2010_02_08.pdf)). A loose bound does not prove a class is unlearnable; it may just be a loose bound ([Sharif lecture notes](https://sharif.edu/~beigy/courses/14002/40718/Lect-3.pdf)). The realizable assumption—that a perfect rule sits inside \(H\)—often fails because labels are noisy or the truth lies outside \(H\) ([Sharif lecture notes](https://sharif.edu/~beigy/courses/14002/40718/Lect-3.pdf)). PAC also does not prove that simpler hypotheses are better: a philosophy critique argues that data-compression suffices for PAC learning, but so does drawing from any sufficiently small set of rules, and PAC assigns no prior probabilities ([ILLC, “Probably Approximately Confusing”](https://archive.illc.uva.nl/HPI/Draft_Learning.pdf)). PAC-Bayes is a separate, algorithm-dependent family; its prior and posterior need not follow Bayes’ theorem, so a PAC-Bayes bound should not be read as a Bayesian posterior probability that a model is correct ([SDU research portal](https://portal.findresearcher.sdu.dk/en/publications/pac-bayesian-analysis)).

The practical limits are not subtle. A course calculation with ε=0.1, δ=0.1 and VC dimension 3 gives a classical bound of about 29,300 examples, while a rule of thumb says about \(10\cdot d\), or 30, often enough ([NTU slides](https://www.csie.ntu.edu.tw/~htlin/mooc/doc/07_present.pdf)). A deep-learning lecture calls the VC bound “extremely loose” and “vacuous,” reporting bounds like “less than 10 billion percent,” and explains the mismatch: gradient descent does not pick a random hypothesis from the class ([MIT 6.7960](https://ocw.mit.edu/courses/6-7960-deep-learning-fall-2024/mit6_7960f24_lec06_captions.vtt)). Zhang et al. show that state-of-the-art networks can fit random labels and that simple depth-two networks already have perfect finite-sample expressivity once parameters exceed data points, so traditional complexity theories fail to explain why large networks generalize ([Zhang et al., CACM](https://dl.acm.org/doi/fullHtml/10.1145/3446776)). Earlier assessments reached the same verdict more mildly: VC bounds offer “a limited guide” with “important practical shortcomings” ([IEEE](https://ieeexplore.ieee.org/document/374184/authors#authors)), and the basic PAC theory “is not good for predicting learning curves” while its assumptions of well-defined targets and noise-free data are “unrealistic in practice” ([UCSC report](https://tr.soe.ucsc.edu/sites/default/files/technical-reports/UCSC-CRL-90-16.pdf)). The same report defends the other side: no amount of experimentation or distribution-specific theory replaces the security of a distribution-independent bound ([UCSC report](https://tr.soe.ucsc.edu/sites/default/files/technical-reports/UCSC-CRL-90-16.pdf)). The bound is sufficient, not necessary, and can grossly overestimate the data needed ([Illinois State](https://www.itk.ilstu.edu//faculty/mecalif/ITK385/Spring2010/slides/385_2010_02_08.pdf)); the constants in VC bounds are not tight, although the bounds often keep the right shape for ranking sources ([Technion paper](https://www.ee.technion.ac.il/people/koby/publications/crammer08a.pdf)); and an early “myths” report warns against treating computational learning theory as “a solid basis on which the algorithm designer can perform his duties,” calling it at best “a rough guide” ([NASA report](https://ntrs.nasa.gov/api/citations/19920016854/downloads/19920016854.pdf)). Most capacity bounds are far too loose to tell a specific problem how many examples it needs, and they are vacuous for deep networks ([BlueRingsLabs](https://github.com/BlueRingsLabs/no-shortcuts/blob/main/part-3-classical-ml/16-learning-problem/16.3-learning-theory.md)).

## Conclusion

PAC is best understood as a framework for asking how sample size buys accuracy and confidence, not as a single theorem. For finite classes, the arithmetic is explicit: realizable learning needs about \((\ln|H|+\ln(1/\delta))/\varepsilon\) examples, while agnostic learning pays a \(1/\varepsilon^2\) rate and a union-bound penalty for every candidate rule. For infinite classes, VC dimension replaces \(\ln|H|\), and the Fundamental Theorem makes finite VC dimension the exact dividing line for distribution-free binary learnability.

The practical lesson is two-sided. The bounds are worst-case and often numerically useless, especially for deep networks, and they do not justify Occam’s razor or a Bayesian posterior reading. But they are the rare guarantees that hold across all distributions, which is why they remain the reference point for what “learning from examples” can mean. Beginners should take the shape of the trade-offs seriously and the constants lightly.
