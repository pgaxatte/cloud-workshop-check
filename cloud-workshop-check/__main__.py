import os
from .app import app

app.run(debug=(os.environ.get("DEBUG", "0") == "1"))
