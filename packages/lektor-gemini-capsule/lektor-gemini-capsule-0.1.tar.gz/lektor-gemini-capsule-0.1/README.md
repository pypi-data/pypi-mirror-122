# Lektor Gemini capsule

This plugin for Lektor adds support for dual-generation of web and [Gemini][gmi]
content.


## Using this


### Steps

1. Install `lektor-gemini-capsule`
2. Create your templates under `templates/MODEL.gmi`
3. `lektor build` and profit!

Note that if your web server is the same as your Gemini server, you may be able
to copy the whole site once and serve both protocols from the same resulting
directory.
Check your server's documentation.

### Details

In order to install the plugin you can add following to your `.lektorproject`
file:

    [packages]
    lektor-git-src-publisher = 0.3

Or follow the [official plugin instructions][lektorplugins].


## How it works

This plugin generates a corresponding `index.gmi` whenever Lektor generates an
`index.html` file.

It does so by reusing the one model <--> one template concept, so you will have
to create a template for each model.


## Disabling Gemini for specific models

If you would like to skip Gemini generation for a specific model, you can use
following in your model's `.ini`:

    [fields._skip_gemini]
    type = boolean
    default = True


## The `md2gemini` Jinja filter

This plugin defines an `md2gemini` Jinja filter, but by default it just passes
the text as it is defined.

This limitation is due to an incompatibility between md2gemini and Lektor when
it comes to a common dependency called mistune (the Markdown parser).

This filter is defined and its use is encouraged in the hope that this
incompatibility is solved soon and the resulting Gemini capsules are more
Gemini-friendly without any added effort.

[lektorplugins]: https://www.getlektor.com/docs/plugins/
[gmi]: https://gemini.circumlunar.space/
