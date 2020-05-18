# coding=utf-8

from wsgiref.simple_server import make_server


def demo_app(environ, start_response):
    from StringIO import StringIO
    stdout = StringIO()

    print >> stdout, "Hello %s!" % environ["PATH_INFO"]
    print >> stdout, "你好 %s！ 我使用了wsgi" % environ["PATH_INFO"]

    start_response("200 OK", [("Content-Type", "text/plain")])
    return [stdout.getvalue()]


httpd = make_server("", 801, demo_app)
sa = httpd.socket.getsockname()
print("Serving HTTP on %s port %s" % (sa[0], sa[1]))
# import webbrowser
#
# webbrowser.open("http://localhost:80/xyz?abc")
httpd.serve_forever()
