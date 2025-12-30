from nicegui import ui
from apps.architect.ui.layout import ArchitectLayout
from apps.architect.controller import ArchitectController


class TheArchitectApp:
    def __init__(self):
        self.controller = ArchitectController()
        self.view = ArchitectLayout(on_start=self.handle_analysis)

    async def handle_analysis(self, requirements: str):
        self.view.toggle_loader(True)
        try:
            result = await self.controller.run_full_pipeline(requirements)
            self.view.display_results(result)
        except Exception as e:
            ui.notify(f"Error: {str(e)}", type="negative")
        finally:
            self.view.toggle_loader(False)


if __name__ in {"__main__", "__mp_main__"}:
    app = TheArchitectApp()
    ui.run(title="TheArchitect", native=True, window_size=(1200, 800))
