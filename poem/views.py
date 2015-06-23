from pyramid.view import view_config


class BlockViews(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='edit_blocks',
                 renderer='poem:templates/blocks/edit_blocks.jinja2')
    def edit_blocks(self):
        return {}

    @view_config(route_name='create_block')
    def create_block(self):
        pass

    @view_config(route_name='edit_block')
    def edit_block(self):
        pass

    @view_config(route_name='edit_block_position')
    def edit_block_position(self):
        pass
