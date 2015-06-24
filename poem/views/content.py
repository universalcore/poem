from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from deform import ValidationFailure

from poem.content import TestContent
from poem.forms import ContentEditForm
from poem.views.base import ViewsBase


class ContentViews(ViewsBase):

    @view_config(route_name='create_content',
                 renderer='poem:templates/content/create_content.jinja2')
    def create_content(self):
        form = ContentEditForm(is_new=True)

        if 'save' in self.request.POST:
            try:
                data = form.validate(self.request.POST.items())
                content = TestContent(data['title'])
                return HTTPFound(
                    self.request.route_url('select_new_block', id=content.id))
            except ValidationFailure as e:
                form = e.render()
        else:
            form = form.render()

        return self.context(form=form)

    @view_config(route_name='edit_content',
                 renderer='poem:templates/content/edit_content.jinja2')
    def edit_content(self):
        content = TestContent(self.request.matchdict['id'])
        form = ContentEditForm(is_new=False)

        if self.request.method == 'POST':
            try:
                data = form.validate(self.request.POST.items())
                content.rename(data['title'])
                if 'save_edit' in self.request.POST:
                    return HTTPFound(
                        self.request.route_url('edit_blocks', id=content.id))
                # TODO save_finish
            except ValidationFailure as e:
                form = e.render()
        else:
            form = form.render({'title': content.id})

        return self.context(
            form=form,
            content=content)
