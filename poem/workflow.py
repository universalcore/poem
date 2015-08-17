from zope.interface import Interface, Attribute

from repoze.workflow import Workflow


class IContent(Interface):

    wf_state = Attribute('The workflow state that the object is currently in')


content_creation_wf = Workflow(
    name='create content',
    description='Create a new content object',
    state_attr='state',
    initial_state='new')
# NOTE: has callback argument
content_creation_wf.add_state('new')
content_creation_wf.add_state('empty')
content_creation_wf.add_state('ready')
