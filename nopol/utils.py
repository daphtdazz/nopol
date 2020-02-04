class ParamReprMixin:
    def __repr__(self):
        pstr = ', '.join(
            f'{pname}={pval!r}'
            for pname, pval in self.__dict__.items()
            if (
                not pname.startswith('_')
                and pname not in getattr(self, 'omitted_repr_params', set())
            )
        )

        return f'{type(self).__name__}({pstr})'
