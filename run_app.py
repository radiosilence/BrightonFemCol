#!/usr/bin/env python
from btnfemcol import create_app, db
app = create_app(debug=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

