from __future__ import annotations

import sys


def greedy_set_cover(
    universe: set[int],
    subsets: dict[str, set[int]],
) -> tuple[list[str], list[dict]]:
    """
    Resolve o problema de Cobertura de Conjuntos (Set Cover) usando a heurística gulosa.
    A cada passo, escolhe o subconjunto que cobre a maior quantidade de elementos ainda não cobertos.

    Complexidade: O(|U| * |F| * min(|U|, |F|)) — polinomial e escalável para n = 1000+.

    Retorna:
        - chosen: lista com os nomes dos subconjuntos escolhidos (na ordem de escolha).
        - history: lista de dicionários registrando cada passo (útil para exibição/debug).
    """
    uncovered = set(universe)
    chosen: list[str] = []
    history: list[dict] = []

    while uncovered:
        # Seleciona o subconjunto que cobre o maior número de elementos restantes
        best_name, best_set = max(
            subsets.items(),
            key=lambda item: len(item[1] & uncovered),
        )
        newly_covered = best_set & uncovered

        if not newly_covered:
            raise ValueError(
                f"Impossível cobrir todo o universo. Elementos sem cobertura: {sorted(uncovered)}"
            )

        chosen.append(best_name)
        uncovered -= newly_covered

        history.append(
            {
                "step": len(chosen),
                "chosen_name": best_name,
                "chosen_set": best_set,
                "newly_covered": newly_covered,
                "remaining": set(uncovered),
            }
        )

    return chosen, history


# ---------------------------------------------------------------------------
# Apresentação no Console (UX/UI Simples - KIS)
# ---------------------------------------------------------------------------

class Style:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"


def fmt_set(s: set[int]) -> str:
    return "{" + ", ".join(map(str, sorted(s))) + "}" if s else "∅"


def render_solution(
    universe: set[int],
    subsets: dict[str, set[int]],
    chosen: list[str],
    history: list[dict],
) -> None:
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")

    line = "─" * 62

    print(f"\n{Style.BOLD}{Style.CYAN}╭{line}╮{Style.RESET}")
    print(f"{Style.BOLD}{Style.CYAN}│{'COBERTURA DE CONJUNTOS (SET COVER) — SOLUÇÃO ESTÁTICA':^62}│{Style.RESET}")
    print(f"{Style.BOLD}{Style.CYAN}╰{line}╯{Style.RESET}")

    # 1. Entrada
    print(f"\n{Style.BOLD}1. ENTRADA (ESTÁTICA){Style.RESET}")
    print(f"   {Style.BOLD}Universo U{Style.RESET} (|U| = {len(universe)}): {Style.BLUE}{fmt_set(universe)}{Style.RESET}")
    print(f"   {Style.BOLD}Família  F{Style.RESET} (|F| = {len(subsets)}):")
    for name, s in subsets.items():
        print(f"     • {Style.BOLD}{name:<3}{Style.RESET} = {fmt_set(s)}")

    # 2. Passo a passo da execução
    print(f"\n{Style.BOLD}2. EXECUÇÃO DO ALGORITMO (GULOSO){Style.RESET}")
    for step_info in history:
        step = step_info["step"]
        name = step_info["chosen_name"]
        s = step_info["chosen_set"]
        gained = step_info["newly_covered"]
        rem = step_info["remaining"]

        print(
            f"   {Style.YELLOW}[Passo {step}]{Style.RESET} "
            f"Escolhido {Style.BOLD}{name}{Style.RESET} = {fmt_set(s)}"
        )
        print(
            f"            ├─ Novos cobertos (+{len(gained)}) : {Style.GREEN}{fmt_set(gained)}{Style.RESET}"
        )
        print(
            f"            ╰─ Restantes      ({len(rem)})  : {Style.DIM}{fmt_set(rem)}{Style.RESET}"
        )

    # 3. Resultado e verificação
    union_covered = set().union(*(subsets[name] for name in chosen))
    is_valid = union_covered == universe
    status_badge = (
        f"{Style.GREEN}✔ VÁLIDA (U coberto){Style.RESET}"
        if is_valid
        else "\033[91m✘ INVÁLIDA\033[0m"
    )

    print(f"\n{Style.BOLD}3. RESULTADO FINAL{Style.RESET}")
    print(f"   {Style.DIM}{line}{Style.RESET}")
    print(f"   • Subcoleção C* : {Style.BOLD}{Style.GREEN}{'{ ' + ', '.join(chosen) + ' }'}{Style.RESET}")
    print(f"   • Tamanho |C*|  : {Style.BOLD}{len(chosen)}{Style.RESET} subconjunto(s)")
    for name in chosen:
        print(f"       - {name} = {fmt_set(subsets[name])}")
    print(f"   • União         : {fmt_set(union_covered)}")
    print(f"   • Verificação   : {status_badge}")
    print(f"   {Style.DIM}{line}{Style.RESET}\n")


def main() -> None:
    # Instância estática definida em static_problem.md
    U: set[int] = {1, 2, 3, 4, 5, 6}
    F: dict[str, set[int]] = {
        "S1": {1, 2, 3},
        "S2": {2, 4},
        "S3": {3, 4, 5},
        "S4": {4, 5, 6},
        "S5": {1, 6},
    }

    chosen, history = greedy_set_cover(U, F)
    render_solution(U, F, chosen, history)


if __name__ == "__main__":
    main()
