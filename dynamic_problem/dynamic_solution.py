from __future__ import annotations

import json
import os
import random
import sys
import matplotlib.pyplot as plt
import numpy as np


def generate_instance(
    universe_size: int,
    num_subsets: int = 10,
    subset_prob: float = 0.35,
    rng: random.Random | None = None,
) -> tuple[set[int], dict[str, set[int]]]:
    """
    Gera dinamicamente um universo U = {1, ..., universe_size} e uma família F
    com `num_subsets` subconjuntos (fixado em 10 por padrão), garantindo que a
    união de todos os subconjuntos em F cubra 100% de U.
    """
    if rng is None:
        rng = random.Random()

    universe = set(range(1, universe_size + 1))
    subset_names = [f"S{i}" for i in range(1, num_subsets + 1)]
    subsets: dict[str, set[int]] = {name: set() for name in subset_names}

    # 1. Garantia de cobertura viável: todo elemento u in U é alocado a pelo menos um S_i
    for u in universe:
        chosen_subset = rng.choice(subset_names)
        subsets[chosen_subset].add(u)

    # 2. Popula os subconjuntos com elementos adicionais com probabilidade `subset_prob`
    #    para criar sobreposições realistas entre os conjuntos de F.
    k_sample = max(1, int(universe_size * subset_prob))
    universe_list = list(universe)
    for name in subset_names:
        extra_elements = rng.sample(universe_list, k=min(k_sample, universe_size))
        subsets[name].update(extra_elements)

    return universe, subsets


def greedy_set_cover_with_cost(
    universe: set[int],
    subsets: dict[str, set[int]],
) -> tuple[list[str], int, int]:
    """
    Resolve o Set Cover usando a heurística gulosa e contabiliza o custo
    (quantidade de operações elementares realizadas).

    Contagem de operações (`ops`):
      - Cópia inicial do universo: |U| operações.
      - Em cada passo do laço `while uncovered`:
          * Para cada subconjunto S em F:
            A interseção `S & uncovered` verifica pertinência para cada elemento
            do menor conjunto (ou percorre S), custando `min(|S|, |uncovered|)`
            operações de consulta hash + 1 operação de comparação do máximo.
          * Atualização `uncovered -= best_newly_covered`:
            Custa `|best_newly_covered|` operações de remoção.

    Retorna:
        - chosen: lista de nomes dos subconjuntos escolhidos.
        - total_ops: quantidade total de operações elementares (nível de elementos).
        - subset_evals: quantidade de avaliações de subconjuntos (passos * |F|).
    """
    uncovered = set(universe)
    total_ops = len(universe)  # custo de inicializar `uncovered`
    subset_evals = 0
    chosen: list[str] = []

    while uncovered:
        best_name = ""
        best_newly_covered: set[int] = set()

        for name, s in subsets.items():
            subset_evals += 1
            # Custo da interseção entre dois sets em Python: O(min(|s|, |uncovered|))
            total_ops += min(len(s), len(uncovered)) + 1
            candidate_covered = s & uncovered

            if len(candidate_covered) > len(best_newly_covered):
                best_name = name
                best_newly_covered = candidate_covered

        if not best_newly_covered:
            raise ValueError("Impossível cobrir o universo U com a família F fornecida.")

        chosen.append(best_name)
        # Custo da diferença de conjuntos (remoção dos elementos cobertos)
        total_ops += len(best_newly_covered)
        uncovered -= best_newly_covered

    return chosen, total_ops, subset_evals


def run_experiment(
    min_u: int = 10,
    max_u: int = 1000,
    num_subsets: int = 10,
    seed: int = 42,
) -> dict[str, list[int]]:
    """
    Executa o experimento variando |U| de `min_u` (10) até `max_u` (1000),
    mantendo |F| = 10 constante.
    """
    rng = random.Random(seed)
    sizes: list[int] = []
    element_ops: list[int] = []
    subset_evals_list: list[int] = []
    cover_sizes: list[int] = []

    for n in range(min_u, max_u + 1):
        universe, subsets = generate_instance(
            universe_size=n,
            num_subsets=num_subsets,
            subset_prob=0.35,
            rng=rng,
        )
        chosen, ops, evals = greedy_set_cover_with_cost(universe, subsets)

        sizes.append(n)
        element_ops.append(ops)
        subset_evals_list.append(evals)
        cover_sizes.append(len(chosen))

    return {
        "sizes": sizes,
        "element_ops": element_ops,
        "subset_evals": subset_evals_list,
        "cover_sizes": cover_sizes,
    }


def plot_cost_curve(results: dict[str, list[int]], output_path: str) -> None:
    """
    Plota a curva de custo observada usando matplotlib para analisar como o
    algoritmo escala de |U| = 10 até |U| = 1000 com |F| = 10 fixo.
    """
    sizes = np.array(results["sizes"])
    ops = np.array(results["element_ops"])
    evals = np.array(results["subset_evals"])

    # Ajuste linear (mínimos quadrados) para demonstrar o comportamento O(|U|)
    slope, intercept = np.polyfit(sizes, ops, 1)
    linear_fit = slope * sizes + intercept
    r_squared = 1.0 - (np.sum((ops - linear_fit) ** 2) / np.sum((ops - np.mean(ops)) ** 2))

    # Ajuste logarítmico para comparação visual
    log_sizes = np.log(sizes)
    log_slope, log_intercept = np.polyfit(log_sizes, ops, 1)
    log_fit = log_slope * log_sizes + log_intercept

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.8), dpi=140)
    fig.suptitle(
        "Escalabilidade do Set Cover Guloso: |U| de 10 a 1000 (|F| = 10 constante)",
        fontsize=14,
        fontweight="bold",
        y=0.98,
    )

    # --- Gráfico 1: Custo em Operações Elementares vs |U| ---
    ax1.scatter(
        sizes,
        ops,
        s=10,
        alpha=0.35,
        color="#2563eb",
        label="Custo observado (operações por |U|)",
    )
    ax1.plot(
        sizes,
        linear_fit,
        color="#dc2626",
        linewidth=2.2,
        label=f"Tendência Linear O(|U|): y ≈ {slope:.1f}·|U| + {intercept:.0f} (R² = {r_squared:.4f})",
    )
    ax1.plot(
        sizes,
        log_fit,
        color="#16a34a",
        linestyle="--",
        linewidth=1.8,
        label="Referência Logarítmica O(log |U|)",
    )
    ax1.set_title("Custo Computacional (Operações de Conjunto vs. |U|)", fontsize=11, fontweight="bold")
    ax1.set_xlabel("Tamanho do Universo |U|", fontsize=10)
    ax1.set_ylabel("Quantidade de Operações Elementares", fontsize=10)
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="upper left", fontsize=9)

    # --- Gráfico 2: Avaliações de Subconjuntos (Passos Gulosos * |F|) vs |U| ---
    # Média móvel de 25 pontos para destacar a tendência
    window = 25
    evals_smooth = np.convolve(evals, np.ones(window) / window, mode="valid")
    sizes_smooth = sizes[window - 1 :]

    ax2.scatter(
        sizes,
        evals,
        s=10,
        alpha=0.25,
        color="#7c3aed",
        label="Avaliações de subconjuntos (|C*| × |F|)",
    )
    ax2.plot(
        sizes_smooth,
        evals_smooth,
        color="#4c1d95",
        linewidth=2.2,
        label=f"Média móvel ({window} instâncias)",
    )
    ax2.axhline(
        y=100,
        color="#dc2626",
        linestyle="--",
        linewidth=1.5,
        label="Teto teórico máximo (|F|² = 100 avaliações)",
    )
    ax2.set_title("Iterações sobre F (Limitadas por |F| = 10 fixo)", fontsize=11, fontweight="bold")
    ax2.set_xlabel("Tamanho do Universo |U|", fontsize=10)
    ax2.set_ylabel("Avaliações de Subconjuntos (Passos × |F|)", fontsize=10)
    ax2.set_ylim(0, 115)
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.legend(loc="lower right", fontsize=9)

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.savefig(output_path)
    print(f"\n[✔] Gráfico salvo com sucesso em: {output_path}")

    # Exibe a janela do gráfico caso não esteja em modo headless bloqueante
    if os.environ.get("MPLBACKEND", "").lower() != "agg":
        plt.show(block=False)
        plt.pause(0.1)
    plt.close(fig)


def print_summary(results: dict[str, list[int]]) -> None:
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")

    sizes = results["sizes"]
    ops = results["element_ops"]
    evals = results["subset_evals"]
    covers = results["cover_sizes"]

    slope, intercept = np.polyfit(sizes, ops, 1)
    r_squared = 1.0 - (
        np.sum((np.array(ops) - (slope * np.array(sizes) + intercept)) ** 2)
        / np.sum((np.array(ops) - np.mean(ops)) ** 2)
    )

    line = "─" * 74
    print(f"\n╭{line}╮")
    print(f"│{'EXPERIMENTO DINÂMICO — SET COVER (|U| = 10..1000, |F| = 10)':^74}│")
    print(f"╰{line}╯")

    print("\n1. AMOSTRA DE RESULTADOS POR TAMANHO DE |U|:")
    print(f"   {'|U|':>6} │ {'|F|':>4} │ {'|C*| (Passos)':>14} │ {'Avaliações de F':>16} │ {'Custo (Operações)':>18}")
    print(f"   {'─'*6}─┼─{'─'*4}─┼─{'─'*14}─┼─{'─'*16}─┼─{'─'*18}")

    sample_points = [10, 50, 100, 250, 500, 750, 1000]
    for target in sample_points:
        idx = target - sizes[0]
        print(
            f"   {sizes[idx]:>6} │ {10:>4} │ {covers[idx]:>14} │ {evals[idx]:>16} │ {ops[idx]:>18,}"
        )

    print("\n2. ANÁLISE DE ESCALABILIDADE NA PRÁTICA:")
    print(f"   • Equação de Tendência Linear : Custo(|U|) ≈ {slope:.2f} · |U| + {intercept:.1f}")
    print(f"   • Coeficiente de Determinação : R² = {r_squared:.4f} (forte aderência linear)")
    print(
        "   • Conclusão Prática           : Com |F| = 10 fixo, a quantidade de passos gulosos\n"
        "     satura rapidamente (limitada ao teto de 10 subconjuntos), enquanto o custo total\n"
        "     de operações sobre os elementos cresce de forma LINEAR O(|U|)."
    )


def save_results_json(
    results: dict[str, list[int]],
    output_path: str,
    min_u: int,
    max_u: int,
    num_subsets: int,
    seed: int,
) -> None:
    """
    Exporta os parâmetros do experimento, o resumo estatístico e os dados
    por tamanho de |U| em formato JSON.
    """
    sizes = np.array(results["sizes"])
    ops = np.array(results["element_ops"])

    slope, intercept = np.polyfit(sizes, ops, 1)
    linear_fit = slope * sizes + intercept
    r_squared = float(
        1.0 - (np.sum((ops - linear_fit) ** 2) / np.sum((ops - np.mean(ops)) ** 2))
    )

    payload = {
        "experiment": {
            "min_u": min_u,
            "max_u": max_u,
            "num_subsets": num_subsets,
            "subset_prob": 0.35,
            "seed": seed,
            "total_instances": len(results["sizes"]),
        },
        "summary": {
            "linear_fit_slope": round(float(slope), 4),
            "linear_fit_intercept": round(float(intercept), 4),
            "r_squared": round(r_squared, 6),
            "min_element_ops": int(min(results["element_ops"])),
            "max_element_ops": int(max(results["element_ops"])),
            "avg_cover_size": round(float(np.mean(results["cover_sizes"])), 4),
        },
        "results": [
            {
                "universe_size": u_size,
                "num_subsets": num_subsets,
                "cover_size": c_size,
                "subset_evals": evals,
                "element_ops": e_ops,
            }
            for u_size, c_size, evals, e_ops in zip(
                results["sizes"],
                results["cover_sizes"],
                results["subset_evals"],
                results["element_ops"],
            )
        ],
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"[✔] Resultados salvos em JSON em: {output_path}")


def main() -> None:
    os.environ.setdefault("MPLBACKEND", "Agg")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_plot = os.path.join(script_dir, "cost_curve.png")
    output_json = os.path.join(script_dir, "results.json")

    min_u, max_u, num_subsets, seed = 10, 1000, 10, 42
    results = run_experiment(min_u=min_u, max_u=max_u, num_subsets=num_subsets, seed=seed)
    print_summary(results)
    save_results_json(results, output_json, min_u, max_u, num_subsets, seed)
    plot_cost_curve(results, output_plot)


if __name__ == "__main__":
    main()
