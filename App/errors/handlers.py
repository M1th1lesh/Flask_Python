#error handler pages 

from flask import Blueprint ,render_template

errors = Blueprint('errors',__name__)

# app_errorhandler this is used so that our errror handles is active across the application
# if we use errohandler then it will be active only for this ble print

#decoratr
@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404
    #by default the second arguement is 200 but we can return our values too

@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500
