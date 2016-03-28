# standard library

# 3rd party libraries

# project libraries

class Terms:
  api_to_new = {
  
    }

  @classmethod
  def get_reverse(self, new_term):
    result = new_term
    for api, new in Terms.api_to_new.items():
      if new == new_term:
        result = api

    return result

  @classmethod
  def get(self, api_term):
    """
    Return the translation of the specified API term
    """
    if Terms.api_to_new.has_key(api_term):
      return self.api_to_new[api_term]
    else:
      return api_term