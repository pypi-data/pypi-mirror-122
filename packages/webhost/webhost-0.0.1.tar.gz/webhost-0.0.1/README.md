WebHost is a very basic python webframework.

Example Code:

	from webhost.api import init, server

	app = init()

	settings = {'Http404': '404, Page not found!'}  # 404 page error.

	app.config(settings)

	def views(app):

		@app.route('/')
		def home(request, response):
			response.text = Hello, This is the Home page"

	server.run(app)