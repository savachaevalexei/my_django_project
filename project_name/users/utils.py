class DataMixin:
    
    def get_mixin_context(self, context, **kwargs):
        context['foreign_languages'] = None
        context.update(kwargs)
        return context