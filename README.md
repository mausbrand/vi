# ViUR Vi [![Build Status](https://travis-ci.org/viur-framework/vi.svg?branch=develop)](https://travis-ci.org/viur-framework/vi)

**Vi** is a web-based administration client for [ViUR-applications](https://github.com/viur-framework/).

## About

*Vi* (pronounced as "whee!") is an acronym for *visual interface*. It is a platform-independent HTML5-web-app that is written in Python and must be compiled into JavaScript using the [PyJS](https://github.com/pyjs/pyjs) transpiler.

It was tested and runs well with the latest versions of Chrome (Chromium), Firefox and Safari. Microsoft Edge and Internet Explorer >= 9 should also run it suitable as well.

Pre-compiled and packaged versions of the Vi can be obtained on the official [ViUR website](https://www.viur.is/download).

## Installation

The compiled web-app has to be put in a directory ``vi/`` within the ViUR application directory. The name of the directory can diverge when expressed so within the applications' ``app.yaml`` file.

Please check out the [ViUR documentation](https://docs.viur.is/latest) to get more information.

## Requirements

This software is implemented on top of the [PyJS framework](https://github.com/pyjs/pyjs) and uses the [html5 library](https://github.com/viur-framework/html5) to create DOM objects, which is also part of the ViUR open source project.

To build it on your own, [PyJS](https://github.com/pyjs/pyjs) and [{less}](http://lesscss.org/) is required.

## Building

Because Vi provides the ability to get easily customized and extended, this repository contains a simple Makefile for GNU make to get all compilation tasks and dependencies done.

By default, it builds into a directory called ``vi`` within the source root directory. In an advanced setup (project based setup), it builds into the folder ``../appengine/vi`` or ``../deploy/vi``, up one level of the working directory, which makes it suitable to use this repository as a submodule of an entire applications source repository.

After checking out vi, simply move into the working directory and type:

```
$ make
```

to create a deploy-able and speed-optimized version, run

```
$ make deploy
```

to remove all generated files and rebuild from scratch, type

```
$ make clean
$ make
```

## Contributing

We take a great interest in your opinion about ViUR. We appreciate your feedback and are looking forward to hear about your ideas. Share your visions or questions with us and participate in ongoing discussions.

- [ViUR on the web](https://www.viur.is)
- [#ViUR on freenode IRC](https://webchat.freenode.net/?channels=viur)
- [ViUR on Google Community](https://plus.google.com/communities/102034046048891029088)
- [ViUR on Twitter](https://twitter.com/weloveViUR)

## Credits

ViUR is developed and maintained by [Mausbrand Informationssysteme GmbH](https://www.mausbrand.de/en), from Dortmund in Germany. We are a software company consisting of young, enthusiastic software developers, designers and social media experts, working on exciting projects for different kinds of customers. All of our newer projects are implemented with ViUR, from tiny web-pages to huge company intranets with hundreds of users.

Help of any kind to extend and improve or enhance this project in any kind or way is always appreciated.

## License

ViUR is Copyright (C) 2012-2017 by Mausbrand Informationssysteme GmbH.

Mausbrand and ViUR are registered trademarks of Mausbrand Informationssysteme GmbH.

You may use, modify and distribute this software under the terms and conditions of the GNU Lesser General Public License (LGPL). See the file LICENSE provided within this package for more information.
