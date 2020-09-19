# Django Tutorial

## Views
- Django has two types of views; function-based views (FBVs), and class-based views (CBVs).
- Requirements
    1. **They are callable**. A view can be either function or a class-based view. CBVs inherit the method as_view() which uses a dispatch() method to call the appropriate method depending on the HTTP verb (get, post, etc)
    2. They must accept an HttpRequest object as its first positional argument
    3. They must return an HttpResponse object or raise an exception.
### Class-based view (CBV)
- Pros
> - Code reuseability — In CBV, a view class can be inherited by another view class and modified for a different use case.
> - DRY — Using CBVs help to reduce code duplication
Code extendability — CBV can be extended to include more functionalities using Mixins
> - Code structuring — In CBVs A class based view helps you respond to different http request with different class instance methods instead of conditional branching statements inside a single function based view.
> - Built-in generic class-based views
- Cons
> - Harder to read
> - Implicit code flow
> - Use of view decorators require extra import, or method override
### function-based view (FBV)
- Pros
> - Simple to implement
> - Easy to read
> - Explicit code flow
> - Straightforward usage of decorators
> - good for one-off or specialized functionality

- Cons
> - Hard to extend and reuse the code
> - Handling of HTTP methods via conditional branching

:::warning
**Function-based view v.s. Class-based view**
:::
---

## Templates
### Template filter


---

## Forms
- Form validation steps
    1. SomeField.to_python(self, value)
        - called for: each Field of myform
        - meaning: converts the string value to its Python target type (e.g. int)
        - takes input from: value
        - returns: value coerced into the proper Python type for SomeField
        - side effects: should have none
        - signals problems by: raise ValidationError
    2. SomeField.validate(self, value)

        - called for: each Field of myform
        - meaning: validates Field locally (just like a validator would)
        - takes input from: value
        - returns: None
        - side effects: should have none
        - signals problems by: raise ValidationError
    3. SomeField.run_validators(self, value)
        - called for: each Field of myform
        - meaning: executes all validators registered for myform.somefield
        - takes input from: value
        - returns: None
        - side effects: should have none
        - signals problems by: raise ValidationError combining all ValidationErrors from the validators into one
    4. SomeField.clean(self, value)
        - called for: each Field of myform
        - meaning: runs to_python, validate, and run_validators
        - takes input from: value
        - returns: the desired ("cleaned") value, usually the result of to_python
        - side effects: Django will insert the return value into myform.cleaned_data
        - signals problems by: not handling any ValidationError raised by the other operations
        -    note: **do not override**.
    5. MyForm.clean_somefield(self)
        - called for: each Field of myform with such a method
        - meaning: validate somefield locally
        - takes input from: self.cleaned_data **(no longer just strings now!)**
        - returns: the new or unchanged value for somefield
        - side effects: Django will insert the return value into myform.cleaned_data
        - signals problems by: raising ValidationError
        - note: This happens in the same loop as the Field.clean calls.
    6. MyForm.clean(self)
        - called for: myform once
        - meaning: **perform any cross-field validation**
        - takes input from: self.cleaned_data (no longer just strings now!)
        - returns: either None or a dict that will become cleaned_data
        - side effects: Django will assign a dict return value to myform.cleaned_data
        - signals problems by: calling self.add_error or raising ValidationError. The latter will end up in myform.non_field_errors().
        - note: Beware when accessing cleaned_data, as fields that did not validate will be missing.

- Extends for ModelForms
    7. myform.instance.full_clean()

- to_python() method on a Field - It coerces the value to a correct datatype and raises ValidationError if that is not possible
-
- class form field validation
    - clean_<field_name>
- validator

---

## Model


---

## Query
### Basic

- values(*fields, **expressions)
    - return list of queryset object as dictionary, which the keys corresponding to attribute names of model
```python=
# This list contains a Blog object.
>>> Blog.objects.filter(name__startswith='Beatles')
<QuerySet [<Blog: Beatles Blog>]>

# This list contains a dictionary.
>>> Blog.objects.filter(name__startswith='Beatles').values()
<QuerySet [{'id': 1, 'name': 'Beatles Blog'}]>
```
- value_list(*fields, flat=False, named=False)
```python=
>>> Entry.objects.values_list('id', 'headline')
<QuerySet [(1, 'First entry'), ...]>
```
:::info
**values**() and **values_list**() are both intended as optimizations for a specific use case: retrieving a subset of data without the overhead of creating a model instance. This metaphor falls apart when dealing with many-to-many and other multivalued relations (such as the one-to-many relation of a reverse foreign key) because the “one row, one object” assumption doesn’t hold.
:::

### Query across model relations
- To order by a field in a different model, use the same syntax as when you are querying across model relations. That is, the name of the field, followed by a double unders    core (__), followed by the name of the field in the new model, and so on for as many models as you want to join.

For example, the queryset object is retrieved by **Blog**'s id field
```python=
Entry.objects.get('Blog__id')
```

### field lookup
- Field lookups are how you specify the meat of an SQL WHERE clause. They’re specified as keyword arguments to the QuerySet methods **filter**(), **exclude**() and **get**().
-
1. **exact**
- case-**sensitive** match
```python=
Entry_objects.get(id__exact=14)
Entry_objects.get(id=14) # implicit
```
```sql=
SELECT * WHERE id = 14;
```
3. **inexact**
- case-**insensitive** match
```python=
Blog.objects.get(name__iexact='beatles blog')
Blog.objects.get(name__iexact=None)
```
```sql=
SELECT * WHERE name <> 'beatles blog';
```
5. **contain**
> Case-sensitive containment test
```python=
Entry.objects.get(headline__contains='Lennon')
```
```sql=
SELECT * WHERE headline LIKE '%Lennon%';
```
6. **in**
```python=
Entry.objects.filter(id__in=[1, 3, 4])
Entry.objects.filter(headline__in='abc')
```
```sql=
SELECT * WHERE id IN (1, 3, 4);
SELECT * WHERE headline IN ('a', 'b', 'c');
```
> Advanced
```python=
inner_qs = Blog.objects.filter(name__contains='Cheddar')
entries = Entry.objects.filter(blog__in=inner_qs)
```
```sql=
SELECT ... WHERE blog.id IN (SELECT id FROM ... WHERE NAME LIKE '%Cheddar%')
```
7. **gt**
```python=
Entry.objects.filter(id__gt=4)
```
```sql=
SELECT * WHERE id > 4
```
8. **gte**
```python=
Entry.objects.filter(id__gte=4)
```
```sql=
SELECT * WHERE id >= 4
```
9. **lt**
```python=
Entry.objects.filter(id__lt=4)
```
```sql=
SELECT * WHERE id < 4
```
11. **gte**
```python=
Entry.objects.filter(id__lte=4)
```
```sql=
SELECT * WHERE id <= 4
```
13. **startwith**
```python=
Entry.objects.filter(headline__startswith='Lennon')
```
```sql
SELECT * WHERE headline LIKE 'Lennon%'
```
14. **istartwith**
- case-insensitive **startwith**

15. **endwith**
```python=
Entry.objects.filter(headline__endwith='Lennon')
```
```sql
SELECT * WHERE headline LIKE '%Lennon'
```
16. **iendwith**
- case-insensitive **endwith**
17. **isnull**
```python=
Entry.objects.filter(pub_date__isnull=True)
```
```sql
SELECT * WHERE pub_date IS NULL
```
18. **regex**
- case-sensitive regular expression match
```python=
Entry.objects.get(title__regex=r'^(An?|The) +')
```
```sql=
SELECT ... WHERE title REGEXP BINARY '^(An?|The) +'; -- MySQL

SELECT ... WHERE REGEXP_LIKE(title, '^(An?|The) +', 'c'); -- Oracle

SELECT ... WHERE title ~ '^(An?|The) +'; -- PostgreSQL

SELECT ... WHERE title REGEXP '^(An?|The) +'; -- SQLite
```
19. **range**
```python=
import datetime
start_date = datetime.date(2005, 1, 1)
end_date = datetime.date(2005, 3, 31)
Entry.objects.filter(pub_date__range=(start_date, end_date))
```
```sql=
SELECT * WHERE pub_date BETWEEN '2005-01-01' and '2005-03-31';
```
20. **date**
- cast value as date
21. **year**
22. **month**
23. **week**
24. **day**
25. **week_day**
26. **quarter**
27. **time**
- cast value as time
28. **hour**
29. **minute**
30. **second**

#### aggregation function
1. **filter**
2. **avg**
3. coubt

## Notes
### Http GET parameter
![](https://i.imgur.com/iOgAVnc.png)
