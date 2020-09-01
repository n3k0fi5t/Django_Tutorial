# Django Tutorial

## Models
- To order by a field in a different model, use the same syntax as when you are querying across model relations. That is, the name of the field, followed by a double unders    core (__), followed by the name of the field in the new model, and so on for as many models as you want to join.

For example, the queryset object is retrieved by Blog's id field
```python=
Entry.objects.order_by('Blog__id')
```

