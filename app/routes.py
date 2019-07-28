from app.views import (
    set_wh, del_wh, start_job, get_wh, run_wh, index
)


def setup_routes(app):
    app.router.add_route('*', '/', index)
    
    app.router.add_get('/get_wh', get_wh)
    app.router.add_get('/set_wh', set_wh)
    app.router.add_get('/del_wh', del_wh)

    app.router.add_post('/run_wh', run_wh)
    app.router.add_get('/start_job', start_job)
