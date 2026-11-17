---
title: Linear Algebra Basics
source: "Pachamanova & Fabozzi, Portfolio Construction and Analytics, Appendix: Basic Linear Algebra Concepts (pp. 541–548)"
book: "[[Portfolio Construction and Analytics]]"
project: "[[P1 Portfolio Construction Engine]]"
tags:
  - linear-algebra
  - portfolio-construction
  - covariance
  - textbook-notes
---

# Linear Algebra Basics

> [!info] Source
> *Portfolio Construction and Analytics* (Pachamanova & Fabozzi), Appendix, pp. 541–548. The appendix is deliberately simplified: its goal is to make the book's notation readable, not to teach linear algebra in full.
>
> Callouts marked **In P1** connect each idea to my portfolio construction engine. Those are my additions, not the book's.

## Contents

- [[#A.1 Systems of equations]]
- [[#A.2 Vectors and matrices]]
- [[#A.3 Matrix algebra]]
- [[#A.4 Important definitions]]
- [[#Quick reference]]

---

## A.1 Systems of equations

A single equation $a \cdot x = b$ is solved by $x = b/a = a^{-1} b$.

The book's two-equation example:

$$
\begin{aligned}
3x_1 + 8x_2 &= 46 \\
10x_1 - 7x_2 &= -15
\end{aligned}
$$

Solving by substitution gives $x_1 = 2$, $x_2 = 5$.

**Why matrix notation:** stack the coefficients, constants and unknowns into arrays

$$
\mathbf{A} = \begin{bmatrix} 3 & 8 \\ 10 & -7 \end{bmatrix}, \quad
\mathbf{b} = \begin{bmatrix} 46 \\ -15 \end{bmatrix}, \quad
\mathbf{x} = \begin{bmatrix} x_1 \\ x_2 \end{bmatrix}
$$

and the whole system reads like the single-equation case:

$$
\mathbf{A}\mathbf{x} = \mathbf{b} \quad\Longrightarrow\quad \mathbf{x} = \mathbf{A}^{-1}\mathbf{b}
$$

> [!example] numpy
> ```python
> A = np.array([[3, 8], [10, -7]])
> b = np.array([46, -15])
> np.linalg.solve(A, b)   # array([2., 5.])
> ```
> Prefer `solve` to `inv(A) @ b`: it is faster and numerically more stable.

> [!tip] In P1
> Many portfolio problems reduce to $\mathbf{A}\mathbf{x} = \mathbf{b}$. The unconstrained minimum-variance portfolio solves $\boldsymbol\Sigma\,\mathbf{w} \propto \mathbf{1}$, i.e. $\mathbf{w} \propto \boldsymbol\Sigma^{-1}\mathbf{1}$, then rescales so the weights sum to 1.

---

## A.2 Vectors and matrices

| Term | Definition | Notation |
|---|---|---|
| **Matrix** | Array of dimension $N \times M$ ($N$ rows, $M$ columns) | Bold capital, $\mathbf{A}$ |
| **Vector** | Matrix with one column, $N \times 1$ (a point in $N$-dimensional space) | Bold lowercase, $\mathbf{b}$ |
| **Scalar** | A $1 \times 1$ array: a single number | Plain, $a$ |
| **Element** | Entry in row $i$, column $j$ | $a_{ij}$, e.g. $a_{12} = 8$ above |
| **Null matrix** | All zeros | $\mathbf{0}$ |
| **Identity matrix** | 1s on the diagonal, 0s elsewhere; $\mathbf{A}\mathbf{I} = \mathbf{A}$ | $\mathbf{I}$ |

**Geometry.** A vector is a directed arrow from the origin. The vector $[2\ 5]$ points from $(0,0)$ to $(2,5)$.

**Norm (length, magnitude).** The Euclidean distance from start to end:

$$
\|[2\ 5]\| = \sqrt{2^2 + 5^2} = 5.39
$$

**A matrix is an operator.** Multiplying a vector by a matrix transforms it: it can rescale or rotate it.

> [!tip] In P1
> - A portfolio is a weight vector $\mathbf{w}$ ($23 \times 1$ for my universe).
> - A week of returns is a vector $\mathbf{r}_t$; the full return history is a $T \times N$ matrix ($677 \times 23$ weekly).
> - The covariance matrix $\boldsymbol\Sigma$ is $23 \times 23$.

---

## A.3 Matrix algebra

### Equality
Same dimensions **and** same elements. A $3 \times 3$ zero matrix is not equal to a $2 \times 2$ zero matrix.

### Transpose
Swap rows and columns across the diagonal: an $N \times M$ matrix becomes $M \times N$. Written $\mathbf{A}^\top$ or $\mathbf{A}'$.

$$
\mathbf{A}' = \begin{bmatrix} 3 & 10 \\ 8 & -7 \end{bmatrix}, \qquad
\mathbf{b}' = [46\ \ {-15}]
$$

Transposing turns a column vector into a row vector and vice versa.

### Scalar multiplication
Multiply every element by the number: $5\mathbf{A} = \begin{bmatrix} 15 & 40 \\ 50 & -35 \end{bmatrix}$. $-\mathbf{A}$ means $(-1)\mathbf{A}$.

### Addition
Add matching elements. Both matrices must have the **same dimensions**.

### Matrix multiplication
The $(i,j)$ element of $\mathbf{P}\mathbf{Q}$ is row $i$ of $\mathbf{P}$ times column $j$ of $\mathbf{Q}$, multiplied element by element and summed:

$$
(\mathbf{P}\mathbf{Q})_{ij} = \sum_{k=1}^{M} p_{ik}\, q_{kj}
\qquad
\underbrace{\mathbf{P}}_{N\times M}\ \underbrace{\mathbf{Q}}_{M\times T} = \underbrace{\mathbf{P}\mathbf{Q}}_{N\times T}
$$

Check with the A.1 example:

$$
\mathbf{A}\mathbf{x} = \begin{bmatrix} 3\cdot2 + 8\cdot5 \\ 10\cdot2 - 7\cdot5 \end{bmatrix} = \begin{bmatrix} 46 \\ -15 \end{bmatrix} = \mathbf{b}
$$

Rules:
- Inner dimensions must match: columns of the first = rows of the second.
- A chain $N\times M \cdot M\times T \cdot T\times S$ gives $N \times S$.
- **Not commutative:** in general $\mathbf{P}\mathbf{Q} \neq \mathbf{Q}\mathbf{P}$.

### Hadamard product
Element-by-element multiplication of same-size matrices, written $\mathbf{A} \bullet \mathbf{B}$ (or $\odot$). The book stresses this is the special case, not the default.

> [!warning] numpy gotcha
> In numpy, `A * B` is the **Hadamard** product. Matrix multiplication is `A @ B`. Mixing them up is the most common bug in portfolio code.

### Inverse
$\mathbf{A}^{-1}$ is the matrix with $\mathbf{A}\mathbf{A}^{-1} = \mathbf{I}$, so $\mathbf{x} = \mathbf{A}^{-1}\mathbf{b}$.

- Computing it means solving a system of equations whose unknowns are the elements of $\mathbf{A}^{-1}$; software does this for you.
- **Not every matrix has an inverse.** One that does is **nonsingular**.
- Symmetric positive definite matrices (see A.4) are always invertible.

> [!tip] In P1
> Portfolio variance is a chain of multiplications:
> $$\sigma_p^2 = \mathbf{w}'\boldsymbol\Sigma\,\mathbf{w} \qquad (1\times N)(N\times N)(N\times 1) = 1\times 1$$
> In numpy: `w @ Sigma @ w`. Risk contributions use a Hadamard product: `w * (Sigma @ w) / sigma_p`.

---

## A.4 Important definitions

Covariance and correlation matrices are special: they are **symmetric** and, in theory, **positive definite**.

### Symmetric matrix
Elements below the diagonal mirror those above: $\mathbf{A} = \mathbf{A}'$. Covariance and correlation matrices are always symmetric, since $\text{Cov}(X,Y) = \text{Cov}(Y,X)$.

### Positive definite and positive semi-definite
The matrix version of a positive (or non-negative) number:

$$
\text{Positive definite: } \mathbf{z}'\mathbf{A}\mathbf{z} > 0 \qquad
\text{Positive semi-definite: } \mathbf{z}'\mathbf{A}\mathbf{z} \ge 0
$$

for every (non-zero) vector $\mathbf{z}$ of the right size.

> [!tip] In P1
> Put a portfolio $\mathbf{w}$ in place of $\mathbf{z}$ and $\mathbf{z}'\boldsymbol\Sigma\mathbf{z}$ is that portfolio's variance. **Positive definite means every portfolio has positive risk.** If $\boldsymbol\Sigma$ is only semi-definite, some combination of assets looks riskless, and an optimizer will pile into it. Shrinkage ([[Ledoit-Wolf]]) guarantees positive definiteness.

### Scalar (dot, inner) product

$$
\mathbf{u}\cdot\mathbf{v} = \|\mathbf{u}\|\,\|\mathbf{v}\|\cos\theta, \qquad \|\mathbf{u}\| = \sqrt{\mathbf{u}\cdot\mathbf{u}}
$$

where $\theta$ is the angle between the two vectors.

### Orthogonal and orthonormal vectors
- **Orthogonal:** at 90° to each other, so the dot product is 0 ($\cos 90^\circ = 0$).
- **Orthonormal:** orthogonal **and** each of length 1.
- The book notes orthogonality matters whenever we want to show two variables are uncorrelated or independent.

> [!tip] In P1
> For demeaned return series, correlation *is* $\cos\theta$ between the two return vectors. Uncorrelated assets are orthogonal vectors. Principal components are orthogonal by construction, which is why PC factor returns are uncorrelated.

### Orthogonal matrix
Rows and columns are orthonormal vectors:

$$
\mathbf{A}\mathbf{A}' = \mathbf{A}'\mathbf{A} = \mathbf{I} \quad\Longrightarrow\quad \mathbf{A}^{-1} = \mathbf{A}'
$$

An orthogonal matrix always has an inverse: its transpose.

### Eigenvectors and eigenvalues
An eigenvector $\mathbf{v}$ of a square matrix $\mathbf{A}$ satisfies

$$
\mathbf{A}\mathbf{v} = \lambda\mathbf{v}
$$

Multiplying by $\mathbf{A}$ normally stretches, shrinks and rotates a vector. An eigenvector is **not rotated**: it only changes length, or flips direction. The eigenvalue $\lambda$ says how:

| $\lambda$ | Effect on $\mathbf{v}$ |
|---|---|
| $\lambda > 1$ | Stretched |
| $0 < \lambda < 1$ | Shrunk |
| $\lambda = 1$ | Unchanged |
| $\lambda < 0$ | Direction reversed |

### Spectral decomposition (eigendecomposition)
If an $N \times N$ matrix has $N$ distinct eigenvectors,

$$
\mathbf{A} = \mathbf{V}\mathbf{D}\mathbf{V}^{-1}
$$

with $\mathbf{D}$ the diagonal matrix of eigenvalues and the columns of $\mathbf{V}$ the eigenvectors. It can always be done for square **symmetric** matrices, such as covariance and correlation matrices.

> [!note] Beyond the book: the symmetric case
> For a symmetric matrix the eigenvectors can be chosen orthonormal, so $\mathbf{V}$ is an orthogonal matrix and $\mathbf{V}^{-1} = \mathbf{V}'$:
> $$\boldsymbol\Sigma = \mathbf{V}\boldsymbol\Lambda\mathbf{V}'$$
> This ties A.4 together: symmetric → orthogonal eigenvectors; positive definite ⟺ **all eigenvalues > 0**.

> [!example] Worked example: two near-duplicate funds
> SJNK and HYG have a weekly correlation of about 0.97. For a $2\times2$ correlation matrix with correlation $\rho$:
> $$\mathbf{R} = \begin{bmatrix} 1 & \rho \\ \rho & 1 \end{bmatrix}, \quad \lambda_1 = 1+\rho,\ \mathbf{v}_1 = \tfrac{1}{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix}, \quad \lambda_2 = 1-\rho,\ \mathbf{v}_2 = \tfrac{1}{\sqrt2}\begin{bmatrix}1\\-1\end{bmatrix}$$
> With $\rho = 0.97$: $\lambda_1 = 1.97$ (own both, "high yield" risk) and $\lambda_2 = 0.03$ (long one, short the other).
> - The long-short portfolio $\mathbf{v}_2$ has variance $\mathbf{v}_2'\mathbf{R}\mathbf{v}_2 = 0.03$: it looks almost riskless.
> - Condition number $\lambda_1/\lambda_2 \approx 66$.
> - Inverting $\mathbf{R}$ divides by $\lambda_2$, so an optimizer would lever up that spread. This is exactly what [[Ledoit-Wolf]] shrinkage and [[Marchenko-Pastur]] diagnostics address.
>
> ```python
> R = np.array([[1, 0.97], [0.97, 1]])
> eigvals, V = np.linalg.eigh(R)   # eigh: for symmetric matrices, sorted ascending
> eigvals                          # array([0.03, 1.97])
> np.allclose(V @ np.diag(eigvals) @ V.T, R)   # True: R = V Λ V'
> ```

> [!tip] In P1
> - **[[Principal Components Analysis]]** is the eigendecomposition of the correlation matrix: eigenvectors are the factor loadings, eigenvalues the variance each factor explains. My universe: PC1 ≈ risk-on (52%), PC2 ≈ rates (19%), PC3 ≈ dollar (6%).
> - **Condition number** $= \lambda_{\max}/\lambda_{\min}$ measures how unstable $\boldsymbol\Sigma^{-1}$ is.
> - **Scaled-identity shrinkage** keeps $\mathbf{V}$ and moves each eigenvalue toward the average: $\hat\lambda_i = (1-\delta)\lambda_i + \delta\mu$.

---

## Quick reference

| Concept | Math | numpy |
|---|---|---|
| Matrix product | $\mathbf{A}\mathbf{B}$ | `A @ B` |
| Hadamard product | $\mathbf{A}\bullet\mathbf{B}$ | `A * B` |
| Transpose | $\mathbf{A}'$ | `A.T` |
| Inverse | $\mathbf{A}^{-1}$ | `np.linalg.inv(A)` |
| Solve $\mathbf{A}\mathbf{x}=\mathbf{b}$ | $\mathbf{x}=\mathbf{A}^{-1}\mathbf{b}$ | `np.linalg.solve(A, b)` |
| Norm | $\lVert\mathbf{v}\rVert$ | `np.linalg.norm(v)` |
| Dot product | $\mathbf{u}\cdot\mathbf{v}$ | `u @ v` |
| Eigendecomposition (symmetric) | $\mathbf{V}\boldsymbol\Lambda\mathbf{V}'$ | `np.linalg.eigh(A)` |
| Positive definite? | all $\lambda_i > 0$ | `np.all(np.linalg.eigvalsh(A) > 0)` |
| Condition number | $\lambda_{\max}/\lambda_{\min}$ | `np.linalg.cond(A)` |
| Portfolio variance | $\mathbf{w}'\boldsymbol\Sigma\mathbf{w}$ | `w @ Sigma @ w` |

## Related
- [[Covariance Estimation]]
- [[Ledoit-Wolf]]
- [[Marchenko-Pastur]]
- [[Principal Components Analysis]]
- Next in the book: §2.7 *Covariance and Correlation*, §4.4 *Principal Components Analysis*
