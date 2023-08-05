# Anaconda Catalogs client

A light client library for interfacing with the Anaconda catalogs service.

## Usage

Currently, the catalogs are referenced by their unique ID of the form `cid/09e802da-65b3-4ea0-b60d-642c88c7a541`.
A user can load a catalog with the following:

```python
import anaconda_catalogs

cat = anaconda_catalogs.open_catalog("cid/09e802da-65b3-4ea0-b60d-642c88c7a541")
```

Alternately, the native `intake` plugin can be used:

```python
import intake

cat = intake.open_anaconda_catalog("cid/09e802da-65b3-4ea0-b60d-642c88c7a541")
```

Or in an [Intake catalog file](https://intake.readthedocs.io/en/latest/catalog.html#yaml-format),

```yaml
## contents of catalog.yaml
sources:
  anaconda:
    driver: anaconda_catalog
    args:
      name: cid/09e802da-65b3-4ea0-b60d-642c88c7a541
```

which is opened in Intake as

```python
import intake

cat = intake.open_catalog('catalog.yaml')
```

# Development guide

A contributing guide can be found in [CONTRIBUTING.md](./CONTRIBUTING.md).
