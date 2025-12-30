from typing import Callable, Dict, Any
from nicegui import ui


class ArchitectLayout:
    def __init__(self, on_start: Callable):
        self.on_start = on_start
        self.setup_ui()

    def setup_ui(self):
        ui.query("body").classes("bg-slate-950 text-slate-100")

        # Header (Styled with Tailwind)
        with ui.header().classes("bg-slate-900 border-b border-indigo-500/50"):
            ui.label("AgenticArchitect").classes("text-xl font-bold text-indigo-400")
            ui.badge("v1.0 - Local Engine").props("color=indigo-9")

        # Main Input
        with ui.column().classes("w-full max-w-4xl mx-auto p-10 gap-6"):
            with ui.card().classes(
                "w-full bg-slate-900 border border-slate-800 p-6 shadow-2xl"
            ):
                ui.markdown("#### 📝 Project Specifications")
                self.input_field = (
                    ui.textarea(placeholder="Enter your software requirements here...")
                    .props("dark outlined")
                    .classes("w-full")
                )

                with ui.row().classes("w-full justify-end mt-4"):
                    self.spinner = ui.spinner(size="md").classes("hidden mr-4")
                    self.btn = ui.button(
                        "LAUNCH AGENTS", on_click=self.trigger_click
                    ).props("color=indigo-7 rounded")

            self.results_zone = ui.column().classes("w-full gap-4")

    async def trigger_click(self):
        await self.on_start(self.input_field.value)

    def toggle_loader(self, visible: bool):
        self.spinner.set_visibility(visible)
        self.btn.set_enabled(not visible)

    def display_results(self, state: Dict[str, Any]):
        with self.results_zone:
            # Displaying PM Agent output
            pm_data = state.get("charter_data", {})
            with ui.card().classes("w-full border-l-4 border-emerald-500 bg-slate-900"):
                ui.label("PM Analysis").classes("text-lg font-bold text-emerald-400")
                ui.json(pm_data)

            # Displaying C4 Diagram if available
            if "architecture_specs" in state:
                with ui.card().classes("w-full bg-slate-900"):
                    ui.mermaid(state["architecture_specs"]["diagram"])
