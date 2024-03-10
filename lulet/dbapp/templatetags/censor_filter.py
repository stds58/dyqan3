from datetime import datetime
from django import template


register = template.Library()


@register.filter()
def zamena(value):
    value = value.replace("Images:","zdfvdzgxvfsg")
    return f'{value}'


# <select name="images" required id="id_images" multiple>
# <option value="69"><img src="/media/images/45_lfmTsJk_NEDnbkc_W1pjnUk_0Pij0v4.jpg" width="100" height="100" alt=""></option>
# <option value="78"><img src="/media/images/1111.png" width="100" height="100" alt=""></option>
# </select>
#
#
# <script>
# function format(state) {
# var originalOption = state.element;
# return "<img class='flag' src='images/flags/" + state.id.toLowerCase() + ".png' alt='" + $(originalOption).data('foo') + "' />" + state.text;
# }
# </script>
# <select>
# <option value="AL" data-foo="bar">option one</option>
# <option value="1" data-foo="bar">option</option>
# <option value="3" data-foo="bar">option</option>
# </select>
