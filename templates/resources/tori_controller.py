from tori.controller import Controller

class Home(Controller):
    def get(self):
        self.render('home.html', name = '{{ name }}')