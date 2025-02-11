# Methods of seting up dependencies between tasks

1. **Bitshit Operators (>>, <<)**

```python
task1 >> task2 >> task3
```

2. **set_upstream and set_downstream function**

```python
task1.set_upstream(task2)
task3.set_upstream(task2)
```

3. **TaskFlow API**

Dependencies are automatically inferred based on the sequence of task functions calls.

```python
task1()
task2()
task3()
```
