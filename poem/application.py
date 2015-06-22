from pyramid.config import Configurator


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('poem.config')
    return config.make_wsgi_app()
