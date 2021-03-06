# Configuration file format

## Live examples

You can see our existing configurations [in this repo](../taas/config.d).

## Top level format

Our configuration is in [YAML](http://yaml.org/) format, and consists of a sequence of sources (spreadsheets we're reading from) along with a description how that this data should be transformed into JSON.

Each source can contain a number of exports, which would usually be version (`v1`, `v2`, etc), allowing for us to use the same data to generate different outputs. These directly translate to filenames on output.

### Version options

Each version has a human-friendly spreadsheet `url` (which we use to generate our own URL for data extraction in CSV), and a `mapping`, which describes how we map spreadsheet columns into JSON structures.

We'll cover the mapping in more detail momentarily, but it consists of JSON field names on the left, and Spreadsheet field names on the right. In the following config, we'd create a file named `beta-v1/function_roles.json` where each record has an `id` field and a `label` field, which came from the `ID` and `Preferred Term` columns in our spreadsheet.

```YAML
---
sources:
    functional_roles:
        beta-v1:
            url: https://docs.google.com/spreadsheets/d/1c9wehuauQAAegElIRI6vhWktKSI-PcPjHHiXdqASonk/edit#gid=0
            fragment_key: id
            mapping:
                id: ID
                label: Preferred Term
```

The `url` field *must* contain a URL complete with the `gid=` parameter at the end. For spreadsheets that consist of multiple sheets, the gid parameter specifies the individual sheet to be read. The `/edit` part of the URL is optional. In almost all cases a simple copy-and-paste will work correctly.

Permissions on the spreadsheet must allow 'Anyone with the link' to view it.

A source *may* contain a `fragment_key`. If set, JSON fragments (individual files containing only a single record each) will be emitted in addition to the main file, using the contents of the mapping field specified. For example, if we're using numeric IDs, the example above would create files named `beta-v1/functional_roles/1`, `beta-v1/function_roles/2`, etc.

To match how existing APIs present their records, fragments do not have the `.json` or any other extension.

A config file can contain multiple sources, and each source can contain multiple versions.

## Options block

Each source may have an optional `options` block, which changes how the source is processed.

The only valid option at this time is the `build_by_default`, which defaults to `True`. This can be set to `False` to disable the export of this entire taxonomy. In this case the source can still be exported explicitly with `gss2json <source-name>`.

The following example defines a `functional_roles` export, but not one that will be built by default.

```YAML
---
sources:
    functional_roles:
        options:
            build_by_default: False
        beta-v1:
            url: https://docs.google.com/spreadsheets/d/1c9wehuauQAAegElIRI6vhWktKSI-PcPjHHiXdqASonk/edit#gid=0
            mapping:
                id: ID
                label: Preferred Term
```

## Output keys

Output fields are generated exactly presented in the configuration file, with one exception. If the field contains a period (`.`) then it will be transformed into a JSON map. For example:

```YAML
mapping:
    id: ID
    label.i-default: Preferred Term
    label.en: Preferred Term
    label.fr: French Term
    label.de: German Term
```

would generate records that look like:

```JSON
{
    "id": "7",
    "label": {
        "de": "Schiggy",
        "en": "Squirtle",
        "fr": "Carapuce",
        "i-default": "Squirtle"
    }
}
```

## Mapping format

The mapping configuration allows for rich data transformations, and is implemented in the `mapping.py` class.

### Default mappings

The *default* form, copies data directly from a field. The data is trimmed of leading and trailing whitespace, and an error is generated if it is missing. We've already seen examples of default mappings:

```YAML
mapping:
    # Both of these maps use the default form
    id: ID
    label: Preferred Term
```

### Complex mappings

For anything more complex than a 1:1 mapping, we need to use a more complex configuration. Here each JSON output field is given a number of configuration parameters. For example:

```YAML
mapping:
    label.en:
        field: Preferred Term
        optional: False

    label.fr:
        field: French Term
        optional: True
```

It's permissible to mix default and extended formats. Since a term is required by default, we could have written the above as:

```YAML
mapping:
    label.en: Preferred Term

    label.fr:
        field: French Term
        optional: True
```

#### Using multiple fields

If multiple fields are provided, they are examined in order, and the *first* field that contains data will be used. If all are empty the `null` value will be emitted if the field is marked optional, or an error will be raised if the field is mandatory.

For example:

```YAML
mapping:
    preferred_name:
        field:
            - Preferred Name
            - Formal Title
            - Legal Name
```

This will use the "Preferred Name" field if populated, otherwise the "Formal Title" field, and finally the "Legal Name" field if no other options are available. If all fields are empty, an error is raised.

### Literals

A literal field is always the same. It has a mandatory `value` field that is emitted for each record. For example:

```YAML
mapping:
    "@context":
        type: literal
        value: https://example.com/context.jsonld
```

### Plain maps

The most common transform is a `map`, which is a basic 1:1 copy of a spreadsheet field to a JSON
field. Written out fully, our default map usage is equivalent to:

```YAML
mapping:
    id:
        type: map
        field: ID
        optional: False
        trim: True
    label:
        type: map
        field: Preferred Term
        optional: False
        trim: True
```

Any term which is using the defaults can be left out, so most often we'll see shorter configurations, like this:

```YAML
mapping:
    homepage:
        field: Homepage
        optional: True
```

### Concat

A `concat` field is a map which may have a `prefix` or `postfix` added to it. These are particularly useful in generating URLs and other links:

```YAML
mapping:
    self:
        type: concat
        field: ID
        prefix: https://example.com/v1/pokedex/
        postfix: .json
```

Given an input ID for `7`, this would would generate a URL of `https://example.com/v1/pokedex/7.json`.

A `concat` field may also take all the options the `map` field can take.

### Link

A `link` field expects our data to be in the form `id - human string`. The link removes everything after and including the ` - ` (space-hyphen-space) sequence, and then acts exactly like a `concat`.

For example, if we changed our example above to use a `link` field, we could have an input ID of `7 - Squirtle`:

```YAML
mapping:
    self:
        type: link
        field: ID
        prefix: https://example.com/v1/pokedex/
        postfix: .json
```

Link fields *must* contain the space-hyphen-space sequence, otherwise an error will be thrown. They are most useful for editors who must record a machine-readable numeric ID, but want a human-readable label to go with it.

## Config directories

While this document discusses our configuration as if it were a single file, the system also allows a config *directory* to be used, and the `taas/config.d` directory is used by default. Configuration files are read in sequential order and their contents *merged* to form a single configuration.

This means that finding and editing the configuration for a given sheet can be more straightforward, and results in fewer merge conflicts when many configurations are being changed.
