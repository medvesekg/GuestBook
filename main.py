#!/usr/bin/env python
import os
import jinja2
import webapp2
import cgi

from models import Post


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):

        seznam = Post.query(Post.deleted == False).order(-Post.date).fetch()
        params = {"seznam": seznam}
        return self.render_template("hello.html", params=params)
    def post(self):
        name = cgi.escape(self.request.get("name"))
        email = cgi.escape(self.request.get("email"))
        message = cgi.escape(self.request.get("message"))

        if not name:
            name = "Anonymous"

        if not message:
            error = "Message cannot be empty."
            seznam = Post.query().order(-Post.date).fetch()
            params = {"seznam": seznam, "error": error}
            return self.render_template("hello.html", params=params)

        new_post = Post(name=name, email=email, message=message)
        new_post.put()

        seznam = Post.query(Post.deleted == False).order(-Post.date).fetch()
        params = {"seznam": seznam}
        return self.render_template("hello.html", params=params)

class DeleteHandler(BaseHandler):
    def post(self):
        post_id = self.request.get("post-id")
        post = Post.get_by_id(int(post_id))
        post.deleted = True;
        post.put()
        return self.redirect("/")

class EditHandler(BaseHandler):
    def post(self):
        post_id = self.request.get("post_id")
        new_name = cgi.escape(self.request.get("new_name"))
        new_email = cgi.escape(self.request.get("new_email"))
        new_content = cgi.escape(self.request.get("new_content"))

        post = Post.get_by_id(int(post_id))
        post.name = new_name
        post.email = new_email
        post.message = new_content
        post.put()

        return self.redirect("/")

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/delete', DeleteHandler),
    webapp2.Route('/edit', EditHandler),
], debug=True)
