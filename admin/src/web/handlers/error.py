from dataclasses import dataclass
from flask import Flask, render_template

app = Flask(__name__)

@dataclass
class Error:
    code: int
    message: str
    description: str

def error_not_found(e):
    error = Error(404, "Not Found", "The Requested URL was not found on the server.")
    
    return render_template('error.html', error=error), 404

@app.errorhandler(403)
def forbidden(e):
    error_title = "Forbidden"
    error_msg = "You shouldn't be here!"
    return render_template('error.html',
                           error_title=error_title,error_msg=error_msg), 403
