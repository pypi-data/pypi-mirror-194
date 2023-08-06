import textformats
import importlib.resources
_data = importlib.resources.files("fardes").joinpath("data")
_specfile = _data.joinpath("fardes.tf.yaml")
SPEC = textformats.Specification(str(_specfile))

def _validate_elements(elements):
  # the first element shall have "unit" type
  if elements[0]['type'] != "unit":
    return "the first element shall be an unit ID"
  # the last element shall have "unit_id" type
  elif elements[-1]['type'] != "unit":
    return "the last element shall be an unit ID"
  # no two consecutive elements shall have "interval" type
  for i in range(len(elements)-1):
    if elements[i]['type'] == "interval" and \
       elements[i+1]['type'] == "interval":
      return "an interval specifier cannot follow another interval specifier"
  # the first element cannot include a prefix
  if elements[0]['prefix'] != "":
    return "the first unit cannot include a prefix"
  return None

def _normalize_elements(elements):
  for element in elements:
    if element['type'] == "interval" and 'special' not in element:
      if 'max_excl' in element['n_features']:
        element['n_features']['max'] = element['n_features']['max_excl'] - 1
        del element['n_features']['max_excl']
      if 'min_excl' in element['n_features']:
        element['n_features']['min'] = element['n_features']['min_excl'] + 1
        del element['n_features']['min_excl']
      if 'max' not in element['n_features']:
        element['n_features']['max'] = element['n_features']['min']
      if element['n_features']['max'] is not None and \
          element['n_features']['min'] > element['n_features']['max']:
        raise ValueError(
            "invalid interval specifier for number of features: {}-{}".
              format(element['n_features']['min'],element['n_features']['max']))
      if not "length" in element:
        element['length'] = {'min': 0, 'max': None}
      else:
        # apply multiplier to min, max, min_excl, max_excl:
        for key in ['min', 'max', 'min_excl', 'max_excl', 'approx']:
          if key in element['length'] and element['length'][key] is not None:
            element['length'][key] = \
                element['length'][key]['multiplier'] * \
                element['length'][key]['value']
        if 'max_excl' in element['length']:
          element['length']['max'] = element['length']['max_excl'] - 1
          del element['length']['max_excl']
        if 'min_excl' in element['length']:
          element['length']['min'] = element['length']['min_excl'] + 1
          del element['length']['min_excl']
        if 'approx' not in element['length']:
          if 'max' not in element['length']:
            element['length']['max'] = element['length']['min']
          if element['length']['max'] is not None and \
               element['length']['min'] > element['length']['max']:
            raise ValueError(
                "invalid interval specifier for length: {}-{}".
                 format(element['length']['min'],element['length']['max']))
  # if two elements are unit without interval in between, then add
  # an interval with n_features min=0, max=0 and length min=0, max=None
  to_insert = []
  for i in range(len(elements)-1):
    if elements[i]['type'] == "unit" and \
       elements[i+1]['type'] == "unit":
      to_insert.append((i+1, {
        'type': 'interval',
        'n_features': {'min': 0, 'max': 0},
        'length': {'min': 0, 'max': None}
      }))
  for i, element in reversed(to_insert):
    elements.insert(i, element)

def parse(s):
  elements = SPEC["default"].decode(s)
  validation_error = _validate_elements(elements)
  if validation_error is not None:
    raise ValueError("Invalid arrangement format: {}".format(validation_error))
  _normalize_elements(elements)
  return elements
