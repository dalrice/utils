Python Grouper
===================

return groups of huge data to process in small chunk.

DynamicDjangoFilter
===================

it contains a function that returns dynamic args value to use as django filter.

here for example you have any objects of django model.

objs = YourModel.objects.all()

now you have post dict wich can be dynamic with list as value with containing None as to compare null values in database.

exa : 
  post_dict = {'category':['None', 4, 5], 'sub_category':[3,5]}
  
to apply for filter on post_dict :

 objs = objs.filter( *get_and_args(post_dict) )

Crawler a simple crawler for website.
===============================

need mysql.


yaml sorting
============================
to sort yaml file by having key value pair

