# Cobertura de Conjuntos (*Set Cover*) — Estudo Estático e Análise de Escalabilidade Dinâmica

Este repositório apresenta a formulação, implementação e análise empírica de escalabilidade para o problema clássico de **Cobertura de Conjuntos (*Set Cover*)**, desenvolvido no contexto da disciplina de **Projeto e Análise de Algoritmos (PAA)**.

O projeto divide-se em duas frentes complementares:
1. **Problema Base (Estático):** Resolução passo a passo sobre uma instância controlada para demonstrar o funcionamento da heurística gulosa (*Greedy Set Cover*).
2. **Problema Dinâmico (Escalabilidade):** Geração automatizada de $991$ instâncias crescentes ($|U|$ variando de $10$ até $1000$, com $|\mathcal{F}| = 10$ fixo), contabilizando o custo exato em operações elementares e avaliando na prática o comportamento assintótico do algoritmo.

---

## 1. Definição do Problema Base (*Set Cover*)

Dado um conjunto universo $U = \{u_1, u_2, \dots, u_n\}$ composto por $n$ elementos distintos e uma família $\mathcal{F} = \{S_1, S_2, \dots, S_m\}$ de $m$ subconjuntos de $U$ cuja união cobre todo o universo:

$$\bigcup_{S \in \mathcal{F}} S = U$$

O objetivo do problema de **Cobertura de Conjuntos** é encontrar uma subcoleção $\mathcal{C}^* \subseteq \mathcal{F}$ de **cardinalidade mínima** ($|\mathcal{C}^*|$) que cubra todos os elementos de $U$:

$$\bigcup_{S \in \mathcal{C}^*} S = U$$

> [!NOTE]
> **Complexidade Teórica:** A versão de decisão do *Set Cover* é um dos 21 problemas **NP-completos** clássicos de Karp (e a versão de otimização é **NP-difícil**). Por isso, para instâncias gerais ou crescentes, algoritmos exatos de força bruta ($O(2^{|\mathcal{F}|})$) tornam-se inviáveis para famílias grandes, motivando o uso do **Algoritmo Guloso de Aproximação**.

### Exemplo Estático ([`static_problem/`](./static_problem/))

Na instância estática base ($|U| = 6$, $|\mathcal{F}| = 5$):
* **Universo:** $U = \{1, 2, 3, 4, 5, 6\}$
* **Família $\mathcal{F}$:**
  * $S_1 = \{1, 2, 3\}$
  * $S_2 = \{2, 4\}$
  * $S_3 = \{3, 4, 5\}$
  * $S_4 = \{4, 5, 6\}$
  * $S_5 = \{1, 6\}$

O algoritmo guloso seleciona iterativamente o subconjunto que cobre a maior quantidade de elementos ainda descobertos:
1. **Passo 1:** Escolhe $S_1 = \{1, 2, 3\}$ (cobre $3$ novos elementos; restam $\{4, 5, 6\}$).
2. **Passo 2:** Escolhe $S_4 = \{4, 5, 6\}$ (cobre os $3$ elementos restantes; restam $\emptyset$).
* **Solução encontrada:** $\mathcal{C}^* = \{S_1, S_4\}$ com tamanho $|\mathcal{C}^*| = 2$.

---

## 2. Abordagem da Solução e Transição para o Problema Dinâmico

Para investigar **como o algoritmo guloso escala na prática**, estendemos o solucionador do problema base para um experimento dinâmico ([`dynamic_problem/`](./dynamic_problem/)).

### Como o Problema Dinâmico foi Construído

1. **Crescimento do Universo ($|U|$ de $10$ a $1000$):**
   * Para cada tamanho $n \in \{10, 11, 12, \dots, 1000\}$ (totalizando **$991$ instâncias**), gera-se dinamicamente o universo $U = \{1, 2, \dots, n\}$.
2. **Família $\mathcal{F}$ Constante ($|\mathcal{F}| = 10$):**
   * A quantidade de subconjuntos em $\mathcal{F} = \{S_1, S_2, \dots, S_{10}\}$ é mantida fixa em $10$.
   * **Garantia de Cobertura Viável:** Na geração aleatória (`seed = 42`), todo elemento $u \in U$ é inicialmente atribuído a pelo menos um subconjunto $S_i$ sorteado ao acaso (garantindo $\bigcup_{i=1}^{10} S_i = U$), e em seguida cada subconjunto recebe uma amostragem adicional de $35\%$ do universo (`subset_prob = 0.35`) para criar sobreposições realistas.
3. **Instrumentação de Custo (Contagem de Operações):**
   * Ao resolver o *Set Cover* para cada universo $U$, o algoritmo registra duas métricas de custo:
     * **Custo em Operações Elementares (`element_ops`):** Contabiliza a inicialização do conjunto de elementos descobertos ($|U|$), o custo real de cada interseção `S & uncovered` em Python — proporcional a $\min(|S|, |\text{uncovered}|) + 1$ consultas de hash por subconjunto avaliado — e o custo de remoção dos elementos cobertos `uncovered -= best_newly_covered` ($|\text{newly\_covered}|$).
     * **Avaliações de Subconjuntos (`subset_evals`):** Número total de inspeções realizadas sobre a família $\mathcal{F}$, dado por $|\mathcal{C}^*| \times |\mathcal{F}|$.

---

## 3. Resultados Experimentais e Curva de Escalabilidade

O gráfico abaixo (gerado por [`dynamic_problem/dynamic_solution.py`](./dynamic_problem/dynamic_solution.py) e consolidado em [`dynamic_problem/results.json`](./dynamic_problem/results.json)) ilustra a curva de custo observada para $|U| \in [10, 1000]$:

![Curva de Custo e Escalabilidade do Set Cover Guloso](./dynamic_problem/cost_curve.png)

### Síntese Estatística ([`results.json`](./dynamic_problem/results.json))

| Métrica do Experimento | Valor Observado |
| :--- | :--- |
| **Faixa do Universo ($\|U\|$)** | $10$ até $1000$ ($991$ instâncias avaliadas) |
| **Tamanho da Família ($\|\mathcal{F}\|$)** | $10$ subconjuntos (constante) |
| **Equação de Tendência Linear** | $\text{Custo}(\|U\|) \approx 17{,}0543 \cdot \|U\| - 166{,}7178$ |
| **Coeficiente de Determinação ($R^2$)** | **$0{,}999084$** ($99{,}91\%$ de aderência linear) |
| **Custo Mínimo / Máximo (Operações)** | $146$ ops ($\|U\| = 10$) / $17.096$ ops (pico próximo a $\|U\| = 1000$) |
| **Tamanho Médio da Cobertura ($\|\mathcal{C}^*\|$)** | $8{,}30$ subconjuntos |

### Amostra da Evolução do Custo por Tamanho de $|U|$

| Tamanho do Universo ($\|U\|$) | Família ($\|\mathcal{F}\|$) | Passos Gulosos ($\|\mathcal{C}^*\|$) | Avaliações de $\mathcal{F}$ (`subset_evals`) | Custo Total (`element_ops`) |
| ---: | ---: | ---: | ---: | ---: |
| **10** | 10 | 3 | 30 | 146 |
| **50** | 10 | 6 | 60 | 753 |
| **100** | 10 | 6 | 60 | 1.566 |
| **250** | 10 | 8 | 80 | 4.076 |
| **500** | 10 | 9 | 90 | 8.378 |
| **750** | 10 | 9 | 90 | 12.372 |
| **1000** | 10 | 9 | 90 | 16.732 |

### Interpretação Prática: Linear vs. Logarítmico

A análise conjunta dos dois painéis do gráfico revela duas perspectivas fundamentais do algoritmo quando $|\mathcal{F}| = 10$ é mantido constante:

1. **Custo em Operações sobre Elementos é Estritamente Linear — $\Theta(|U|)$ (Painel Esquerdo):**
   * O ajuste por mínimos quadrados apresenta $R^2 = 0{,}9991$ com inclinação de $\approx 17{,}05$ operações por elemento adicional em $U$.
   * Embora a referência logarítmica $O(\log |U|)$ (linha tracejada verde) seja mostrada para comparação, o custo real de processamento escala **linearmente** com $|U|$. Isso ocorre porque cada operação de interseção `S & uncovered` e diferença `uncovered -= best` precisa percorrer conjuntos cujo tamanho é uma fração direta de $|U|$.

2. **Quantidade de Iterações / Avaliações de $\mathcal{F}$ Cresce Logaritmicamente até Saturar (Painel Direito):**
   * Para universos pequenos ($|U|$ entre $10$ e $250$), o número de passos gulosos necessários para cobrir $U$ cresce rapidamente em formato sublinear/logarítmico (passando de $3$ passos / $30$ avaliações para $8$ passos / $80$ avaliações).
   * Como $|\mathcal{F}| = 10$ é constante, o número de passos gulosos possui um **teto teórico rígido** de no máximo $10$ escolhas ($100$ avaliações de subconjuntos, linha tracejada vermelha). A partir de $|U| \approx 400$, a média móvel estabiliza entre $85$ e $95$ avaliações, explicando por que o fator multiplicativo sobre $|U|$ torna-se constante e resulta na reta linear observada no painel esquerdo.

---

## 4. Estrutura do Repositório

```text
setcover/
├── README.md                           # Documentação principal e análise dos resultados
├── requirements.txt                    # Dependências Python (matplotlib, numpy)
├── static_problem/
│   ├── static_problem.md               # Definição formal e exemplo ilustrativo estático
│   └── static_solution.py              # Implementação gulosa com exibição passo a passo no console
└── dynamic_problem/
    ├── dynamic_problem.md              # Especificação do experimento dinâmico (|U| = 10..1000, |F| = 10)
    ├── dynamic_solution.py             # Gerador de instâncias, medição de custo, exportação JSON e plotagem
    ├── results.json                    # Dados completos das 991 instâncias e regressão linear
    └── cost_curve.png                  # Gráfico comparativo da curva de custo e iterações
```

---

## 5. Como Executar

### Pré-requisitos

Crie e ative um ambiente virtual Python e instale as dependências listadas em [`requirements.txt`](./requirements.txt):

```bash
python -m venv .venv

# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 1. Executar a Solução Estática (Problema Base)

```bash
python static_problem/static_solution.py
```

### 2. Executar o Experimento Dinâmico ($|U| = 10 \dots 1000$)

```bash
python dynamic_problem/dynamic_solution.py
```

A execução irá:
* Gerar e resolver as $991$ instâncias ($|U| = 10$ a $1000$, $|\mathcal{F}| = 10$);
* Exibir a tabela resumida e a equação de regressão no terminal;
* Atualizar o arquivo [`dynamic_problem/results.json`](./dynamic_problem/results.json) e o gráfico [`dynamic_problem/cost_curve.png`](./dynamic_problem/cost_curve.png).
