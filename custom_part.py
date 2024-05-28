from object import Object


class CustomPart:
    def __init__(self, title, text, **kwargs):
        self.title = title
        self.text = text

        if 'mass_value' in kwargs and 'mass_calculation' in kwargs:
            self.mass_value = kwargs.get('mass_value')
            self.mass_calculation = kwargs.get('mass_calculation')

        if 'radius_value' in kwargs and 'radius_calculation' in kwargs:
            self.radius_value = kwargs.get('radius_value')
            self.radius_calculation = kwargs.get('radius_calculation')

        if 'improve_decay_value' in kwargs:
            self.improve_decay_value = kwargs.get('improve_decay_value')

    def update(self, object):
        update_object = Object(object.mass, object.radius, object.decay, object.restitution)

        if hasattr(self, 'mass_value') and hasattr(self, 'mass_calculation'):
            if self.mass_calculation == 'multiple':
                update_object.mass *= self.mass_value

        if hasattr(self, 'radius_value') and hasattr(self, 'radius_calculation'):
            if self.radius_calculation == 'multiple':
                update_object.radius *= self.radius_value

        if hasattr(self, 'improve_decay_value'):
            update_object.decay = 1 - (1 - object.decay) * (1 - self.improve_decay_value)

        if hasattr(self, 'restitution_value') and hasattr(self, 'restitution_calculation'):
            if self.restitution_calculation == 'add':
                update_object.restitution += self.restitution_value

        return update_object
