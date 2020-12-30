# Local Templating Engine
**Author:** Gray

**License:** [MIT License](#License "MIT License")

**Description:** Incredibly simple local templating engine for HTML projects. While working on websites many pages tend to have common elements and modules such as navigation menus or head tags. When faced with this issue the developer is usually stuck with 2 options, maintain everything manually so that you don't compromise on performance, or use a backend pre-processor like php, or django templates. This application provides a third option allowing you to utilize templates in much the same ways as you would with a preprocessor by allowing you generate pre-processed versions of your website yourself.

## Installation
```sh
# Download the repository with
$ git clone https://github.com/GrayWasTaken/local-templating-engine.git
```

## Screenshots
![1](https://apoc.club/assets/portfolio/local-templating-engine/1.png "Help Screen")
![2](https://apoc.club/assets/portfolio/local-templating-engine/2.png "File processing")

## Features
- Variable support
- External module support
- Variable contexts expand recursively throughout the document

## Usage
***The help screen has all the information you'd need, but here are some hopefully useful examples:***

```py
# Prints help screen
$ ./main.py -h

# Process folder "./web-app/" and then output results to default folder ./output/
$ ./main.py -i web-app/

# Process folder "./web-app/" and then output results to folder ./custom/
$ ./main.py -i web-app/ -o custom/

# Process folder "./web-app/" and then output results to default folder ./output/ with verbose output
$ ./main.py -i web-app/ -v
```

### Template Format
***To see a more thorough case please check out the example input and output folders that are with this repository. These folders are called input and output respectively.***

Loads a module / template file from the templates folder, the default templates folder is the "templates" folder within the input folder.
```
{{mod:main.html}}
```

Assigns a variable called title the value of "Testing Site".
```
{{var:title=Testing Site}}
```

Invokes the template file "head.html" and embeds the contents of head.html at the position of the invocation.
```
{%head.html%}
```

Invokes the variable "title" and embeds the value of title at the position of the invocation.
```
{{title}}
```

## Todo List
- Implement minifier.
- Possibly better banner.


## License
MIT License

Copyright (c) 2020 Gray

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.