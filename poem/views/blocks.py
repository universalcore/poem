from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from deform import ValidationFailure

from poem.forms import BlockEditForm, BlockPositionForm
from poem.content import TestContent
from poem.views.base import ViewsBase


class BlockViews(ViewsBase):

    def __init__(self, request):
        super(BlockViews, self).__init__(request)
        self.content = TestContent(self.request.matchdict['id'])

    def context(self, **kwargs):
        return super(BlockViews, self).context(content=self.content, **kwargs)

    @view_config(route_name='edit_blocks',
                 renderer='poem:templates/blocks/edit_blocks.jinja2')
    def edit_blocks(self):
        return self.context()

    @view_config(route_name='edit_block',
                 renderer='poem:templates/blocks/edit_block.jinja2')
    def edit_block(self):
        try:
            block = self.content.get_block(self.request.matchdict['block_id'])
        except ValueError:
            raise HTTPNotFound
        form = BlockEditForm(block=block)

        if 'save' in self.request.POST:
            try:
                data = form.validate(self.request.POST.items())
                data.pop('block_type')
                block.update(**data)
                self.content.save()
                return HTTPFound(
                    self.request.route_url('edit_blocks', id=self.content.id))
            except ValidationFailure as e:
                form = e.render()
        else:
            data = block.data.copy()
            data['block_type'] = block.type
            form = form.render(data)

        return self.context(
            form=form,
            block=block)

    @view_config(route_name='edit_block_position',
                 renderer='poem:templates/blocks/edit_block_position.jinja2')
    def edit_block_position(self):
        try:
            block = self.content.get_block(self.request.matchdict['block_id'])
        except ValueError:
            raise HTTPNotFound
        # position variables are 1-based for display
        current_pos = self.content.blocks.index(block) + 1
        max_pos = len(self.content.blocks)
        form = BlockPositionForm(max_pos=max_pos)

        def get_new_pos(form_data):
            if 'save' in self.request.POST:
                return form_data['position']
            if 'move_down' in self.request.POST:
                return min(current_pos + 1, max_pos)
            if 'move_up' in self.request.POST:
                return max(current_pos - 1, 1)

        if self.request.method == 'POST':
            try:
                data = form.validate(self.request.POST.items())
                new_pos = get_new_pos(data)
                self.content.move_block(current_pos - 1, new_pos - 1)
                self.content.save()
                return HTTPFound(
                    self.request.route_url('edit_blocks', id=self.content.id))
            except ValidationFailure as e:
                form = e.render()
        else:
            form = form.render({'position': current_pos})

        return self.context(
            form=form,
            block=block)

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
                form = e.render()
        else:
            form = form.render({'block_type': block_type})

        return self.context(
            form=form,
            block_type=block_type)

    @view_config(route_name='select_new_block',
                 renderer='poem:templates/blocks/select_new_block.jinja2')
    def select_new_block(self):
        return self.context()

    @view_config(
        route_name='select_new_heading_block',
        renderer='poem:templates/blocks/select_new_heading_block.jinja2')
    def select_new_heading_block(self):
        return self.context()

    @view_config(route_name='delete_block')
    def delete_block(self):
        block_id = self.request.matchdict['block_id']
        try:
            self.content.delete_block(block_id)
            self.content.save()
        except ValueError:
            raise HTTPNotFound
        return HTTPFound(
            location=self.request.route_url('edit_blocks', id=self.content.id))
