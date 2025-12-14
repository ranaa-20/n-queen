import flet as ft
from time import sleep, time
from board import Board
from backtracking import solveNQueens
from hill_climbing import hill_climbing_solver
from cultural import cultural_algorithm_solver
from best_first import BestFirstSearch_H1, BestFirstSearch_H2
from plots import generate_time_plot
import matplotlib.pyplot as plt


def main(page: ft.Page):
    page.title = "N-Queens Solver"
    page.bgcolor = "#112138"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.padding = 20

    title = ft.Text("N-Queens Solver", size=32, weight="bold", color="#fff")
    entry = ft.TextField(label="Board Size (N)", width=220, text_align=ft.TextAlign.CENTER,
                         keyboard_type=ft.KeyboardType.NUMBER)
    algo_dropdown = ft.Dropdown(label="Select Algorithm", width=220,
                                options=[ft.dropdown.Option("Backtracking"),
                                         ft.dropdown.Option("Hill Climbing"),
                                         ft.dropdown.Option("Cultural"),
                                         ft.dropdown.Option("BFS H1"),
                                         ft.dropdown.Option("BFS H2")],
                                value="Backtracking")
    board_container = ft.Column(
    spacing=5,
    horizontal_alignment="center",
    scroll=ft.ScrollMode.AUTO,
    height=520   # تقدر تزودها أو تقللها
)

    result_text = ft.Text("", size=16, color="#ffcc00")
    results_all = []
    gui_cells = []

    def validate_n():
        try:
            value = int(entry.value)
        except:
            dialog = ft.AlertDialog(
                title="Invalid Input",
                content=ft.Text("Please enter a valid number"),
                actions=[ft.ElevatedButton("OK", on_click=lambda e: page.close(dialog))]
            )
            page.open(dialog)
            return None

        if value < 4:
            dialog = ft.AlertDialog(
                title="No Solution",
                content=ft.Text("No solution found\nN must be ≥ 4", size=16),
                actions=[ft.ElevatedButton("OK", on_click=lambda e: page.close(dialog),
                                        bgcolor=ft.Colors.RED, color=ft.Colors.WHITE)]
            )
            page.open(dialog)
            return None

        return value


    def update_gui(board_state):
        for r in range(n):
            for c in range(n):
                cell = gui_cells[r][c]
                if c < len(board_state) and r==board_state[c]:
                    cell.content = ft.Text("👸", size=30)
                else:
                    cell.content = None
        page.update()

    # ---------- Cultural Plot ----------
    def show_ca_plot(history):
        if not history:
            return
        plt.figure()
        plt.plot(range(len(history)), history, marker='o')
        plt.xlabel("Generation")
        plt.ylabel("Conflicts")
        plt.title("Cultural Algorithm Performance")
        path = "ca_plot.png"
        plt.savefig(path)
        plt.close()
        plot_dialog = ft.AlertDialog(
            title="Cultural Algorithm Plot",
            content=ft.Image(src=path, width=500),
            actions=[ft.ElevatedButton("Close", on_click=lambda e: page.close(plot_dialog))]
        )
        page.open(plot_dialog)

    def run_algorithm(algo_name, board_state=None):
        start_time = time()
        final_pos, steps, ca_perf = None, 0, None  # التعريف الافتراضي

        if algo_name=="Backtracking":
            final_pos, steps = solveNQueens(board_state, 0, n, update_gui)
        elif algo_name=="Hill Climbing":
            final_pos, steps = hill_climbing_solver(n, update_gui)
        elif algo_name=="Cultural":
            final_pos, steps, ca_perf = cultural_algorithm_solver(n, update_gui)
        elif algo_name=="BFS H1":
            final_pos, steps = BestFirstSearch_H1(n, gui_callback=update_gui)
        elif algo_name=="BFS H2":
            final_pos, steps = BestFirstSearch_H2(n, gui_callback=update_gui)

        duration = time() - start_time
        results_all.append((algo_name, final_pos, steps, duration))

        content = ft.Column([
            ft.Text(f"{algo_name}", weight=ft.FontWeight.BOLD, size=20),
            ft.Text(f"Steps: {steps}"),
            ft.Text(f"Time: {duration:.6f} s"),
            ft.Text(f"Solution: {final_pos}")
        ], alignment=ft.MainAxisAlignment.CENTER)

        # إعداد أزرار الـ AlertDialog
        actions_list = [
            ft.ElevatedButton("Next", on_click=lambda e: page.close(dialog),
                              bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE)
        ]

        # لو Cultural، نضيف زرار Show CA Plot
        if algo_name=="Cultural" and ca_perf:
            actions_list.append(
                ft.ElevatedButton("Show CA Plot", on_click=lambda e: show_ca_plot(ca_perf),
                                  bgcolor="#f39c12", color="white")
            )

        dialog = ft.AlertDialog(
            modal=True,
            title="Algorithm Result",
            content=content,
            actions=actions_list
        )
        page.open(dialog)
        while dialog.open:
            sleep(0.1)
            page.update()

        return final_pos, steps, duration

    # ---------- Results Table ----------
    def show_results_table_dialog():
        table_columns = [
            ft.DataColumn(ft.Text("Algorithm")),
            ft.DataColumn(ft.Text("Steps")),
            ft.DataColumn(ft.Text("Time (s)")),
            ft.DataColumn(ft.Text("Positions"))
        ]
        table_rows = []
        for algo_name, final_pos, steps, duration in results_all:
            table_rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(algo_name)),
                    ft.DataCell(ft.Text(str(steps))),
                    ft.DataCell(ft.Text(f"{duration:.6f}")),
                    ft.DataCell(ft.Text(str(final_pos)))
                ])
            )
        table = ft.DataTable(columns=table_columns, rows=table_rows, border=ft.border.all(1, ft.Colors.WHITE))

        def show_plots(e):
            img = generate_time_plot(results_all)
            plot_dialog = ft.AlertDialog(
                title="Time Comparison Plot",
                content=ft.Image(src=img, width=500),
                actions=[ft.ElevatedButton("Close", on_click=lambda e: page.close(plot_dialog))]
            )
            page.open(plot_dialog)

        dialog = ft.AlertDialog(
            modal=True,
            title="All Algorithms Comparison",
            content=ft.Column([table, ft.Divider(), ft.ElevatedButton("Show Plots", on_click=show_plots)]),
            actions=[ft.ElevatedButton("Close", on_click=lambda e: page.close(dialog),
                                       bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE)]
        )
        page.open(dialog)
        while dialog.open:
            sleep(0.1)
            page.update()

    # ---------- Board Setup ----------
    def setup_board():
        nonlocal gui_cells
        gui_cells = [[None]*n for _ in range(n)]
        grid = ft.Column(spacing=0, alignment="center")
        CELL_SIZE = 50
        LIGHT,DARK="#f5f5dc","#4b4b7f"

        for i in range(n):
            row = ft.Row(spacing=0, alignment="center")
            for j in range(n):
                bgcolor = LIGHT if (i+j)%2==0 else DARK
                cell = ft.Container(width=CELL_SIZE, height=CELL_SIZE, bgcolor=bgcolor,
                                    border=ft.border.all(2,"#000"), alignment=ft.alignment.center)
                gui_cells[i][j] = cell
                row.controls.append(cell)
            grid.controls.append(row)

        board_frame = ft.Container(
            padding=5,
            bgcolor="#000",
            border_radius=6,
            content=grid,
            alignment=ft.alignment.center
        )

        board_container.controls.clear()
        board_container.controls.append(board_frame)
        page.update()

    # ---------- Start Buttons ----------
    def start_single(e):
        board_container.controls.clear()
        result_text.value = ""
        page.update()

        global n
        n = validate_n()
        if n is None:
            return

        setup_board()
        algo_name = algo_dropdown.value
        board_state = Board(n)
        run_algorithm(algo_name, board_state)

        page.update()

    def start_all(e):
        board_container.controls.clear()
        result_text.value = ""
        page.update()

        global n
        n = validate_n()
        if n is None:
            return

        setup_board()
        results_all.clear()

        for algo_name in ["Backtracking", "Hill Climbing", "Cultural", "BFS H1", "BFS H2"]:
            board_state = Board(n)
            run_algorithm(algo_name, board_state)

        show_results_table_dialog()


    start_btn = ft.ElevatedButton("Start", on_click=start_single, bgcolor="#4a90e2", color="white", width=160)
    all_btn = ft.ElevatedButton("Run All", on_click=start_all, bgcolor="#4a90e2", color="white", width=160)

    page.add(title, entry, algo_dropdown, ft.Row([start_btn, all_btn], alignment="center"),
             board_container, result_text)

ft.app(target=main)