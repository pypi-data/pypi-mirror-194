# DFPermission

### Attributes

superuser uchun dostup beriladimi

- `df_method`
  - Method of action
  - Valid values are `create`, `update`, `retrieve`, `list`, `destroy`
```pycon
class MyView(CreateAPIView):
    permission_classes = [DFPermission]
    df_method = 'create'
    ...
```

or

```pycon
class MyView(CreateAPIView):
    permission_classes = [DFPermission]
    df_method = DFMethods.CREATE
    ...
```

- `df_model`
  - model
```pycon
class MyView(CreateAPIView):
    permission_classes = [DFPermission]
    df_model = MyModel
    ...
```

- `df_fields`
  - Fields
```pycon
class MyView(CreateAPIView):
    permission_classes = [DFPermission]
    df_fields = ['field1', 'field2', ...]
    ...
```

- `df_permissions`
  - Permissions
```pycon
class MyView(CreateAPIView):
    permission_classes = [DFPermission]
    df_permissions = ['permission1', 'permission2', ...]
    ...
```

- `df_object_permission`
  - Object permission tekshirilishi
  - type: `Boolean`
  - default: `False`

### Methods

- `get_df_permissions`
  - Get df permissions
```pycon
class MyView(CreateAPIView):
    permission_classes = [DFPermission]
    
    def get_df_permissions(self):
        # write your logic code
        return # perms list
```