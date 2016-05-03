import bbs


app = bbs.create_app()
app.run(host="0.0.0.0", port=6677, debug=True,threaded=True)

