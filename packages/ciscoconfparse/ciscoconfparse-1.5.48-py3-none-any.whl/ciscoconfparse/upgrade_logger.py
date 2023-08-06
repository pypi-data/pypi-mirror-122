

from .ciscoconfparse import CiscoConfParse

parse = CiscoConfParse("ciscoconfparse.py")
for obj in parse.find_objects("^\s+def"):
    tmp_before = obj.text
    tmp_after = obj.text.lstrip()
    num_spaces = len(tmp_before) - len(tmp_after)
    obj.insert_before(" "*num_spaces + "@logger.catch('WARNING')", atomic=True)

parse.commit()
parse.save_as()
