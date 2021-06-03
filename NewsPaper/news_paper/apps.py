from django.apps import AppConfig


class NewsPaperConfig(AppConfig):
    name = 'news_paper'

    def ready(self) -> None:
        import news_paper.signals

        return super().ready()