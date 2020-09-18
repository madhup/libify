# Libify
![Hits](https://hitcounter.pythonanywhere.com/count/tag.svg?url=libify)
---
##### (Does not work with Databricks Community)

### Usage
After installing the package, add the following code snippets to the notebooks:

+ In the **importee notebook** (the notebook to be imported), add the following cell at the **end** of the notebook. Make sure that `dbutils.notebook.exit` is not used anywhere in the notebook and that the last cell contains exactly the following snippet and nothing else:
  ``` python
  import libify
  libify.exporter(globals())
  ```


+ In the **importer notebook** (the notebook that imports other notebooks), first import `libify`:
  ``` python
  import libify
  ```
  and then use the following code to import the notebook of your choice:
  ``` python
  mod1 = libify.importer(globals(), '/path/to/importee1')
  mod2 = libify.importer(globals(), '/path/to/importee2')
  ```
  Everything defined in `importee1` and `importee2` would now be contained in the namespaces `mod1` and `mod2` respectively, and can be accessed using the dot notation, e.g.
  ```python
  x = mod1.function_defined_in_importee1()
  ```
