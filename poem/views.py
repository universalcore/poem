from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from deform import ValidationFailure

from poem.forms import BlockEditForm
from poem.content import TestContent


class BlockViews(object):

    def __init__(self, request):
        self.request = request
        self.content = TestContent(self.request.matchdict['id'])

    def context(self, **kwargs):
        defaults = {
            'request': self.request,
            'content': self.content
        }
        defaults.update(kwargs)
        return defaults

    @view_config(route_name='edit_blocks',
                 renderer='poem:templates/blocks/edit_blocks.jinja2')
    def edit_blocks(self):
        return self.context()

    @view_config(route_name='edit_block')
    def edit_block(self):
        pass

    @view_config(route_name='edit_block_position')
    def edit_block_position(self):
        pass

    @view_config(route_name='create_block',
                 renderer='poem:templates/blocks/edit_block.jinja2')
    def create_block(self):
        block_type = self.request.GET.get('t', 'paragraph')
        form = BlockEditForm(block_type=block_type)

        if 'save' in self.request.POST:
            try:
                data = form.validate(self.request.POST.items())
                data['type'] = data.pop('block_type')
                self.content.add_block(**data)
                self.content.save()
                return HTTPFound(
                    self.request.route_url('edit_blocks', id=self.content.id))
            except ValidationFailure as e:
                form = e

        return self.context(
            form=form.render(),
            block_type=block_type)

    @view_config(route_name='select_new_block',
                 renderer='poem:templates/blocks/select_new_block.jinja2')
    def select_new_block(self):
        return self.context()

    @view_config(route_name='select_new_heading_block',
                 renderer='poem:templates/blocks/select_new_heading_block.jinja2')
    def select_new_heading_block(self):
        return self.context()

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
