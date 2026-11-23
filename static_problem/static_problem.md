### Problema: Cobertura de Conjuntos (*Set Cover*)

Considere um conjunto universo $U = \{u_1, u_2, \dots, u_n\}$ composto por $n$ elementos distintos e uma família $\mathcal{F} = \{S_1, S_2, \dots, S_m\}$ de $m$ subconjuntos de $U$, tal que a união de todos os subconjuntos em $\mathcal{F}$ seja igual a $U$:

$$\bigcup_{S \in \mathcal{F}} S = U$$

Dizemos que um subconjunto $\mathcal{C} \subseteq \mathcal{F}$ **cobre** o universo $U$ se todo elemento de $U$ pertencer a pelo menos um subconjunto de $\mathcal{C}$, isto é:

$$\bigcup_{S \in \mathcal{C}} S = U$$

#### Objetivo

Encontrar uma subcoleção $\mathcal{C}^* \subseteq \mathcal{F}$ de **tamanho mínimo** $\vert{}\mathcal{C}^*\vert{}$ que cubra todos os elementos de $U$.

#### Entrada

* Um conjunto não vazio $U$ com $n$ elementos.
* Uma coleção $\mathcal{F}$ de $m$ subconjuntos $S_1, S_2, \dots, S_m \subseteq U$, assumindo que existe ao menos uma cobertura válida.

#### Saída

* Uma lista ou coleção $\mathcal{C} \subseteq \mathcal{F}$ de subconjuntos cuja união seja igual a $U$, buscando minimizar $\vert{}\mathcal{C}\vert{}$.

---

### Exemplo Ilustrativo

Dado o universo $U = \{1, 2, 3, 4, 5, 6\}$ e a coleção:

* $S_1 = \{1, 2, 3\}$
* $S_2 = \{2, 4\}$
* $S_3 = \{3, 4, 5\}$
* $S_4 = \{4, 5, 6\}$
* $S_5 = \{1, 6\}$

Uma cobertura válida de tamanho $2$ é $\mathcal{C}^* = \{S_1, S_4\}$, pois:

$$S_1 \cup S_4 = \{1, 2, 3\} \cup \{4, 5, 6\} = \{1, 2, 3, 4, 5, 6\} = U$$

(Observação: Na versão de decisão do problema — relevante no estudo de NP-completude da ementa —, dado adicionalmente um inteiro $k$, pergunta-se se existe uma cobertura $\mathcal{C} \subseteq \mathcal{F}$ com $\vert{}\mathcal{C}\vert{} \le k$.)

Se você quiser o enunciado adaptado para **grafos** (como *Vertex Cover* ou *Dominating Set*) ou no estilo de **atividade prática/prova** da disciplina, posso ajustar o formato.