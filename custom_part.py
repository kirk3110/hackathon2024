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

