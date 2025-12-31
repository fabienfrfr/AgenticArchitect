from nicegui import ui
from typing import Callable, Dict, Any


class ArchitectLayout:
    def __init__(self, on_start: Callable):
        self.on_start = on_start
        self.container = ui.column().classes("w-full items-center")
        self.setup_ui()

    def setup_ui(self):
        with ui.card().classes("w-2/3 q-pa-md mt-10"):
            ui.label("TheArchitect").classes("text-h4 mb-4")
            self.req_input = ui.textarea(
                label="Enter project requirements",
                placeholder="e.g. Build a Python API with Docker...",
            ).classes("w-full")

            ui.button(
                "START AGENTIC WORKFLOW",
                on_click=lambda: self.on_start(self.req_input.value),
            ).classes("w-full mt-4")

            self.spinner = ui.spinner(size="lg").classes("mt-4")
            self.spinner.set_visibility(False)

            self.results_area = ui.column().classes("w-full mt-6")

    def toggle_loader(self, visible: bool):
        self.spinner.set_visibility(visible)

    def display_results(self, result: Dict[str, Any]):
        self.results_area.clear()
        with self.results_area:
            ui.label("Analysis Results").classes("text-h6")
            ui.json_editor({"content": {"json": result}})
