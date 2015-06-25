def includeme(config):
    config.add_static_view(
        'static', 'poem:static', cache_max_age=3600)
    # Content
    config.add_route(
        'create_content', '/new_content/')
    config.add_route(
        'edit_content', '/content/{id}/')
    config.add_route(
        'list_content', '/content/')
    config.add_route(
        'preview_content', '/content/{id}/preview/')
    # Blocks
    config.add_route(
        'edit_blocks', '/content/{id}/blocks/')
    config.add_route(
        'edit_block', '/content/{id}/blocks/{block_id}/')
    config.add_route(
        'edit_block_position', '/content/{id}/blocks/{block_id}/position/')
    config.add_route(
        'delete_block', '/content/{id}/blocks/{block_id}/delete/')
    config.add_route(
        'create_block', '/content/{id}/new_block/')
    config.add_route(
        'select_new_block', '/content/{id}/select_new_block/')
    config.add_route(
        'select_new_heading_block', '/content/{id}/select_new_heading_block/')
    config.scan('.views')
