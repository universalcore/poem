from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from poem.content import TestContent


class BlockViews(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='edit_blocks',
                 renderer='poem:templates/blocks/edit_blocks.jinja2')
    def edit_blocks(self):
        content = TestContent(self.request.matchdict['id'])
        return {'content': content}

    @view_config(route_name='create_block')
    def create_block(self):
        pass

    @view_config(route_name='delete_block')
    def delete_block(self):
        content = TestContent(self.request.matchdict['id'])
        block_id = self.request.matchdict['block_id']
        try:
            content.delete_block(block_id)
            content.save()
        except ValueError:
            raise HTTPNotFound
        return HTTPFound(
            location=self.request.route_url('edit_blocks', id=content.id))

    @view_config(route_name='edit_block')
    def edit_block(self):
        pass

    @view_config(route_name='edit_block_position')
    def edit_block_position(self):
        pass
