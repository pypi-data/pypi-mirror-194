import os


class SampleUtils:

    def __init__(self, project_path: str) -> None:
        self.project_path = project_path

    def remove_sample(self):
        shared_common_main_path = f"{self.project_path}/shared/src/commonMain/kotlin/com/sharpyx/kmm_template"
        features = f"{shared_common_main_path}/features/pokemons"
        os.system(f'rm -r {features}')
