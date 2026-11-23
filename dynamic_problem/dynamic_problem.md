### Problema Dinâmico: Cobertura de Conjuntos (*Set Cover*) e Análise de Escalabilidade

Considere o problema de Cobertura de Conjuntos (*Set Cover*), onde dado um universo $U = \{1, 2, \dots, n\}$ com $|U| = n$ elementos e uma família $\mathcal{F} = \{S_1, S_2, \dots, S_m\}$ de subconjuntos de $U$ tal que $\bigcup_{S \in \mathcal{F}} S = U$, buscamos encontrar uma subcoleção $\mathcal{C}^* \subseteq \mathcal{F}$ que cubra todo o universo $U$ utilizando a menor quantidade possível de subconjuntos.

Diferente da versão estática (onde $U$ e $\mathcal{F}$ possuem tamanhos fixos e reduzidos), nesta formulação **dinâmica e experimental** avaliamos o comportamento assintótico e o custo computacional do algoritmo guloso à medida que o universo $U$ cresce.

---

#### Parâmetros do Experimento

1. **Tamanho do Universo ($|U| = n$):**
   * Variável no intervalo de $n = 10$ até $n = 1000$ ($10 \le |U| \le 1000$).
   * Para cada tamanho $n$, gera-se dinamicamente o conjunto $U = \{1, 2, \dots, n\}$.

2. **Tamanho da Família de Subconjuntos ($|\mathcal{F}| = m$):**
   * Constante e fixado em $m = 10$ subconjuntos ($\mathcal{F} = \{S_1, S_2, \dots, S_{10}\}$).
   * **Garantia de Cobertura Viável:** A geração aleatória dos subconjuntos $S_i \subseteq U$ deve garantir que todo elemento $u \in U$ pertença a pelo menos um subconjunto de $\mathcal{F}$ ($\bigcup_{i=1}^{10} S_i = U$), evitando instâncias sem solução.

3. **Métrica de Custo (Quantidade de Operações):**
   * Ao resolver o *Set Cover* para cada universo $U$ gerado, registra-se o **custo computacional** expresso pela quantidade de operações elementares empregadas pelo algoritmo para encontrar a cobertura.
   * **Contagem de Operações:**
     * *Operações de nível de elemento (interseção e diferença de conjuntos):* A cada iteração do laço guloso, o algoritmo avalia os $m = 10$ subconjuntos calculando a interseção $S_i \cap \text{descobertos}$ (cujo custo em operações elementares é proporcional aos elementos inspecionados, i.e., $\min(|S_i|, |\text{descobertos}|)$ ou $|S_i|$) e, após escolher o melhor subconjunto $S^*$, remove os elementos recém-cobertos ($\text{descobertos} \leftarrow \text{descobertos} \setminus S^*$).
     * *Iterações / Comparações de subconjuntos:* Número de avaliações de subconjuntos ($|\mathcal{F}|$ por passo guloso).

---

#### Objetivo

1. **Gerar e Resolver:** Para cada tamanho $n \in [10, 1000]$, construir o universo $U$ e a família $\mathcal{F}$ ($|\mathcal{F}| = 10$) e executar o algoritmo guloso de *Set Cover*.
2. **Registrar o Custo:** Armazenar o número total de operações realizadas para resolver cada instância de tamanho $n$.
3. **Visualizar a Escalabilidade (`matplotlib`):** Plotar um gráfico relacionando o tamanho do universo $|U|$ (eixo X, de $10$ a $1000$) com o custo em operações (eixo Y), permitindo observar na prática como o algoritmo escala (por exemplo, verificando se a curva de crescimento com $|\mathcal{F}| = 10$ constante comporta-se de forma **linear** $O(|U|)$ ou sublinear/logarítmica).

---

#### Análise Teórica Esperada vs. Prática

No algoritmo guloso de *Set Cover*:
* Em cada passo, percorremos os $m = |\mathcal{F}|$ subconjuntos para encontrar aquele que maximiza $|S_i \cap U_{\text{restante}}|$.
* Em Python, a interseção entre dois conjuntos `A & B` percorre os elementos do menor conjunto, realizando $O(\min(|A|, |B|))$ consultas de hash ($O(1)$ médio cada), ou $O(|U|)$ no pior caso por subconjunto.
* Como $|\mathcal{F}| = 10$ é **constante**, o número máximo de passos do laço `while` é limitado superiormente por $|\mathcal{F}| = 10$ (já que só existem 10 subconjuntos disponíveis para serem escolhidos!).
* Portanto, com $|\mathcal{F}| = 10$ fixo:
  * O número de **passos gulosos** (e de comparações entre subconjuntos) estabiliza rapidamente em um valor limitado por $10$ (crescimento quase constante / logarítmico até saturar em $\le 10$).
  * O número de **operações elementares sobre elementos** (consultas de pertinência na interseção `S & uncovered` e remoção `uncovered -= newly_covered`) cresce de forma **linear** em relação a $|U|$, isto é, $\Theta(|U|)$, pois a cada um dos $k \le 10$ passos as operações de conjunto processam frações de $|U|$.
