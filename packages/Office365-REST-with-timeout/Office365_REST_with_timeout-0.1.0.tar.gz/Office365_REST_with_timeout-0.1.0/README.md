This is the same project as Office365-REST (https://github.com/vgrem/Office365-REST-Python-Client), but with the addition of a timeout_ variable in execute_query(), which gets passed down to requests.get. This prevents the execution from hanging indefinitely.

To execute a query with a timeout, simply add the following argument at the end:

```
>>> TIMEOUT=10
>>> my_query.execute_query(timeout_=TIMEOUT)
```
<br />
or 
<br />
```
>>> my_query.execute_query_retry(timeout_=TIMEOUT)
```

Remember to do `$ python3 -m pip uninstall office365-rest-python-client` first if you have the original module installed, since both modules have the same name.

Under the MIT License, as the original Office365-REST-Python-Client. <br />
And I take no credit for this module, sine 99.99% of the code comes from the original project.