from django.template.response import TemplateResponse

class KojaxResponse(TemplateResponse):
    def __init__(self, request, template, context,
        parent_kojax='kojax.xml', parent_nokojax='nokojax.html',
        *args, **kwargs
    ):
        self.request = request
        if request.kojax:
            self.parent = parent_kojax
            kwargs['content_type'] = 'application/x-kojax'
        else:
            self.parent = parent_nokojax
        super(KojaxResponse, self).__init__(request, template, context,
            *args, **kwargs)

    @property
    def rendered_content(self):
        """Returns the freshly rendered content for the template and context
        described by the TemplateResponse.

        This *does not* set the final content of the response. To set the
        response content, you must either call render(), or set the
        content explicitly using the value of this property.
        """
        template = self.resolve_template(self.template_name)
        context = self.resolve_context(self.context_data)
        if self.request.kojax:
            context['kojax'] = {
                'parent': self.parent,
            }
        content = template.render(context)
        return content