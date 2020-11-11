#import os
#app.run(host="0.0.0.0", debug=(os.environ.get("DEBUG", "0") == "1"))

from .app import app
from waitress import serve

serve(app, host='0.0.0.0', port=8080)
