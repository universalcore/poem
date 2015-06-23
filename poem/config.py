def includeme(config):
    config.add_static_view(
        'static', 'poem:static', cache_max_age=3600)
    config.add_route(
        'edit_blocks', '/content/{id}/blocks/')
    config.add_route(
        'edit_block', '/content/{id}/blocks/{block_id}/')
    config.add_route(
        'edit_block_position', '/content/{id}/blocks/{block_id}/position/')
    config.add_route(
        'create_block', '/content/{id}/new_block/')
    config.scan('.views')
