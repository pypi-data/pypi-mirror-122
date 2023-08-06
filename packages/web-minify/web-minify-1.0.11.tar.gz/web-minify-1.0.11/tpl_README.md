[![pipeline status](https://gitlab.com/octomy/web-minify/badges/production/pipeline.svg)](https://gitlab.com/octomy/web-minify/-/commits/production)
[//] # ${README_TEMPLATE_WARNING}
# About web-minify (version ${FK_VERSION})

<img src="https://gitlab.com/octomy/web-minify/-/raw/production/design/logo-1024.png" width="20%"/>

__web-minify__ is the all-in-one just-works-out-of-the-box does-what-you-want highly-opinionated web minifier&trade;

- web-minify is [available on gitlab](https://gitlab.com/octomy/web-minify).

One day I was looking for a thoroughbred Python KISS tool that would optimize the static files of my web app. I was in a hurry and didn't want to fiddle around.

I was super happy when I found [css-html-js-minify](https://github.com/juancarlospaco/css-html-js-minify), which aaaalmost checked all my boxes.

__Aaaaalmost.....__

Turns out a few important pieces were missing;
1. Support for image formats such as [.png](https://en.wikipedia.org/wiki/Portable_Network_Graphics)/[.jpeg](https://en.wikipedia.org/wiki/JPEG)
2. Support for [.svg](https://en.wikipedia.org/wiki/Scalable_Vector_Graphics)
3. Support for [.sass](https://en.wikipedia.org/wiki/Sass_(stylesheet_language))
4. A command line tool that was smart enough to do what I expected most of the time, and humble enough to be coerced otherwise.

I tried to incorporate the tool in my workflow as it was, but I soon gave up and ended up copying the full tool source into my project and adding the features I needed out of sheer frustration. Fast worward a few months and here we are. I am polishing it into a standalone open source tool for the world to enjoy. And the rest is as they say history!


## Goals of this tool:

> NOTE: We have not reached all these goals yet, please see next sections.

| Goal   |      Status |
|--------|-------------|
| All-in-one compressor/obfuscator/minifier/cruncher for most of the common static web formats | See [list of supported formats](#supported-formats). |
| Does what you hoped by default (i.e. highly opinionated) | ✅ |
| Can be tweaked to do what you didn't want (i.e. flexible) | ✅ |
| Small and dependency free (i.e. implemented in pure python if possible) | Only tested/used on Linux. There is hope for OSX/BSD/Posix but YMMV on Windows. |
| Available as library as well as command-line tool | ✅ |
| Easily extensible; adding another backend can be done by writing one function | ✅ |
| Cross platform, supports many Python 3.x versions | Only tested on Python 3.7 |


# Getting started

__web-minify__ can be used and hacked on in a myriad of different ways. 

## Use web-minify as a module from your code

web-minify is [available in PyPI](https://pypi.org/project/web-minify/).

```shell
# Install web-minify into your current Python environment
pip install web-minify

```

Now you can access it's features from your code:

<details>

```Python
import web_minify

settings = {
    "input": "my_originals_dir/",
    "output": "my_processed_dir/",
}

# Instanciate processor with settings we want to use
p = web_minify.processor.Processor(settings)


# Process files as per settings (this is equivalent to the commandline mode)
p. process_file()


# Process a list of files relative to input, and output them depending on settings
p. process_files_list(["input_file.svg", "input_file.html"])


# Process a single file (disregard input/output from settings
p.process_file("some_input_file.svg", "some_output_file.svg")

```

</details>


## Use web-minify as a command line tool

web-minify is [available in PyPI](https://pypi.org/project/web-minify/).

```shell
# Install web-minify into your current Python environment
pip install web-minify

```

```shell
# Run the web-minify cli tool with help argument to see detailed usage
web-minify --help

```


The output looks like this:

<details>

```shell
$ ./web-minify.py --help

${README_CMD_OUTPUT}

```

</details>

## Developing web-minify

web-minify is [available on gitlab](https://gitlab.com/octomy/web-minify).

__web-minify welcomes PRs!__ If you want to contribute we welcome your code contriburtions! We are proud of the fact that this project is a true meritocracy.

Example: extending web-minify to support additional formats is done by a very simple interface:

1. Put a module under `web-minify/web_minify/handlers/your_format`. This can either be a module folder or python module source file. See [css/](web_minify/handlers/css) or [html.py](web_minify/handlers/html.py) for example implementations.
2. Include the new function in `__all__` in `web-minify/web_minify/handlers/__init__.py`
3. Register the new function in `self.processor_map` in `web-minify/web_minify/processor.py`

Easy as 🥧!


### Supported formats
Already supported Formats:


| Format   |       | minify | beautify | Tests|
|----------|-------|--------|----------|------|
| *.html, *htm, *.tpl |  Hypertext Markup Language | ✅ | ❌ | ❌ |
| *.css | Cascading Style Sheets | ✅ | ❌ | ❌ |
| *.js | JavaScript | ✅✝ | ✅ | ❌ |
| *.sass | Syntactically Awesome Style Sheets | ✅ | ❌ | ❌ |
| *.scss | Syntactically Awesome Style Sheets (modern syntax) | ✅ | ❌ | ❌ |
| *.png | Portable Network Graphics | ✅ | ❌ | ❌ |
| *.jpg, *.jpeg | Joint Photographic Experts Group | ✅ | ❌ | ❌ |
| *.svg | Scalable Vector Graphics | ✅ | ❌ | ❌ |
| *.your_file | web-minify is made to be [extensible](#Developing-web-minify) | ✅✝✝ | ✅✝✝ | ✅✝✝ |

_✝Buggy for modern syntax features_
_✝✝Submit your PR!_


# License

Complete license is in the file [LICENSE](LICENSE) in the root of the git repo.

> GNU GPL and GNU LGPL or MIT.
> This work is free software: You can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. This work is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; Without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this work.



# Other Notable Features

1. Supports recursive scanning of directories
2. Supports spitting out .gz versions of files to speed up serving of static files
3. Supports some controls over each format's processing
4. Supports change detection and watch mode
5. Made to be somewhat [extensible](#extending-web-minify)

# Known Limitations and Problems:

1. Compression of modern .js haves some bugs. We welcome PRs!
2. Some of the usage patterns of the command line tool are not implemented yet. We welcome PRs!
3. Codebase has ZERO tests. We welcome PRs!
