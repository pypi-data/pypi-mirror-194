class Group:
    def __init__(self, group_name: str, background_color: str):
        self.group_name = group_name
        self.background_color = background_color

    def __repr__(self):
        p = []
        p.append(f'group_name={self.group_name}')
        p.append(f'background_color={self.background_color}')
        parameters = ', '.join(p)
        return f'Group({parameters})'
