#!/usr/bin/env python2
from btnfemcol import create_app
app = create_app(debug=True)
app.run(host='0.0.0.0')