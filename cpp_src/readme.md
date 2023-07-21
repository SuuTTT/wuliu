# network flow implementation


## prompts

```prompt-cpp-imp
'problem definition (en)'
\begin{prob}
\textbf{Optimize Logistics Distribution}

Consider a logistics distribution scenario with $m$ orders, $n$ warehouses, and $l$ types of goods with dimension "lg". The task is to find a distribution plan that maximizes the overall satisfaction while minimizing the maximum transportation time.

The input data are:

\begin{itemize}
\item $X_{m \times n \times l}$: A three-dimensional matrix indicating the unit transportation time (in hours/lg) for each type of good from each warehouse to each order. 
\item $Y_{m \times l}$: A matrix showing the demand for each type of good (in lg) for each order.
\item $Z_{n \times l}$: A matrix giving the stock of each type of good (in lg) in each warehouse.
\item $O_{m}$: A matrix denoting the priority of each order (dimensionless).
\item $W_{n}$: A matrix representing the priority of each warehouse (dimensionless).
\end{itemize}

The output should be:

\begin{itemize}
\item $A_{m \times n \times l}$: A three-dimensional matrix indicating the transportation quantity of each type of good (in lg) from each warehouse to each order.
\item $B_{m \times n \times l}$: A three-dimensional matrix indicating the transportation time (in hours) of each type of good from each warehouse to each order.
\item $B_{m \times n \times l} = A_{m \times n \times l} \circ X_{m \times n \times l}$
\end{itemize}

The objective is to maximize the following objective function:

\[
\text{Maximize } Z = \alpha \cdot k \cdot \left( \sum_{i=1}^{m} O_i \cdot \left( \sum_{l=1}^{L} \frac{\sum_{j=1}^{n} a_{ijl} \cdot W_j}{y_{il}} \right) \right) - \beta \cdot \left( \max_{i=1}^{m} \sum_{j=1}^{n} \sum_{l=1}^{L} b_{ijl} \right)
\]

subject to $\alpha + \beta = 1$. Here, $k$ is a constant with units of time that balances total satisfaction (first term) and maximum transportation time (second term).

The constraints are:

\begin{itemize}
\item $0 \leq \sum_{i=1}^{m} a_{ijl} \leq z_{jl}$, for all $j$ and $l$
\item $0 \leq \sum_{j=1}^{n} a_{ijl} \leq y_{il}$, for all $i$ and $l$
\end{itemize}

\end{prob}

---
solve the above problem using network flow algorithm in c++.
requirement:
1. first tell me what files to be created.
2. you need to consider extensibility, define class for the entities
3. you will be prompted to write complete code for the entities in later conversations.

```

```prompt
```

```prompt

```prompt

"2.3 总体要求-研究内容“
---
请将上面的文档 转换成让GPT生产代码的prompt
```

