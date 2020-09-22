# Libify
Libify makes it easy to import notebooks in Databricks. Notebook imports can also be nested to create complex workflows easily. Supports Databricks Runtime Version 5.5 and above.

<details>
  <summary><strong>Installation</strong></summary>
  
1. Click the **Clusters** icon in the sidebar
2. Click a cluster name (make sure the cluster is running)
3. Click the **Libraries** tab
4. Click **Install New**
5. Under **Library Source**, choose **PyPI**
6. Under **Package**, write **libify**
7. Click **Install**

[![Capture.png](https://i.postimg.cc/4NsTMPXr/Capture.png)](https://postimg.cc/G97NTk8Q)

</details>

### Typical Usage

After installing the package, add the following code snippets to the notebooks:

1. In the **importee notebook** (the notebook to be imported), add the following cell at the **end** of the notebook. Make sure that `dbutils.notebook.exit` is not used anywhere in the notebook and that the last cell contains exactly the following snippet and nothing else:
    ``` python
    import libify
    libify.exporter(globals())
    ```


2. In the **importer notebook** (the notebook that imports other notebooks), first import `libify`:
    ``` python
    import libify
    ```
    and then use the following code to import the notebook(s) of your choice:
    ``` python
    mod1 = libify.importer(globals(), '/path/to/importee1')
    mod2 = libify.importer(globals(), '/path/to/importee2')
    ```
    Everything defined in `importee1` and `importee2` would now be contained in the namespaces `mod1` and `mod2` respectively, and can be accessed using the dot notation, e.g.
    ```python
    x = mod1.function_defined_in_importee1()
    ```


### Databricks Community Cloud Workaround
Databricks Community Cloud (https://community.cloud.databricks.com) does not allow calling one notebook from another notebook, but notebooks can still be imported using the following workaround. However, both of the following steps will have to be run each time a cluster is created/restarted.

1. Run step 1 from above (**Typical Usage**). Make a note of the output of the last cell (only the part marked below):
    [![Capture.png](https://i.postimg.cc/jdPr39V6/Capture.png)](https://postimg.cc/ppW7psLy)

2. In the **importer notebook**, call `libify.importer` with the `config` parameter as the dictionary obtained from the previous step:
    ``` python
    import libify
    mod1 = libify.importer(globals(), config={"key": "T5gRAUduh9uSbhHIrj2c9R4UbrXUt2WiA4aYIpl3gGo=", "file": "/tmp/tmpmcoypj24"})
    ```


---
![Build/Push Pipeline](https://github.com/vagrantism/libify/workflows/Build%20and%20Publish%20to%20PyPI%20and%20TestPyPI/badge.svg) ![GitHub issues](https://img.shields.io/github/issues/vagrantism/libify) ![PyPI - Format](https://img.shields.io/pypi/format/libify) ![PyPI version](https://badge.fury.io/py/libify.svg) ![GitHub last commit](https://img.shields.io/github/last-commit/vagrantism/libify) ![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/vagrantism/libify) ![visitors](https://visitor-badge.laobi.icu/badge?page_id=libify_main_ctr) ![Downloads](https://pepy.tech/badge/libify)
