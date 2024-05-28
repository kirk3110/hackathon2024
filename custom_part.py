class CustomPart:
    def __init__(self, title, text, **kwargs):
        self.title = title
        self.text = text
        self.update_methods = {
            'mass_value': self.update_mass,
            'radius_value': self.update_radius,
            'improve_decay_value': self.update_decay,
            'restitution_value': self.update_restitution
        }

        for key, value in kwargs.items():
            setattr(self, key, value)

    def update_mass(self, object_):
        if self.mass_calculation == 'multiple':
            object_.mass *= self.mass_value

    def update_radius(self, object_):
        if self.radius_calculation == 'multiple':
            object_.radius *= self.radius_value

    def update_decay(self, object_):
        object_.decay = 1 - (1 - object_.decay) * (1 - self.improve_decay_value)

    def update_restitution(self, object_):
        if self.restitution_calculation == 'add':
            object_.restitution += self.restitution_value

    def update(self, object_):
        for attribute, update_method in self.update_methods.items():
            if hasattr(self, attribute):
                update_method(object_)