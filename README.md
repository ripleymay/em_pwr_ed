# Get ready to feel emPWRed.

## Technologies Used
* Python


## Looks like we're about to slay this whole project. #ijs

## GOING BEAST MODE 


class ActivityDetail(FormMixin, DetailView):
  model = Activity
  form_class = LogForm

  def get_success_url(self):
    return reverse('activity_detail', kwargs={'pk': self.object.pk})

  def post(self, request, *args, **kwargs):
    if not request.user.is_authenticated:
      return HttpResponseForbidden()
    self.object = self.get_object()
    form = self.get_form()
    if form.is_valid():
      return self.form_valid(form)
    else:
      return self.form_invalid(form)

  def form_valid(self, form):
        # Here, we would record the user's interest using the message
        # passed in form.cleaned_data['message']
        return super().form_valid(form)