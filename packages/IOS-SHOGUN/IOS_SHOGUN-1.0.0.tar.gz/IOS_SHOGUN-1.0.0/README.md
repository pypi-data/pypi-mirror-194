# IOS_SHOGUN-Model

shogun-python3 module 1.0 - updated: blocking byte buffers --+console logs + console_colors Reset the terminal color font + bufferState hunger state
[Github-flavored Java version](https://github.com/Atomicntege/IOS_SHOGUN/)
If you are interested, you can take a look

shogun.modul content-BufferByte:

    "The byte-buffered queue, suitable for multithreaded operations and use, is a basic buffered queue
    His basic functions are divided into: queue,push, pop, query, persist, get, persist_put, BufferSpace,
    GetBufferSpace, QueryBufferSpace, detailed features, see details
    author£ºios_shogun-Atomic¾ý
    date:2023-2-24
    self:IOS_SHOGUN_studio"

shogun.modul content-console_colors:

        "console_color" class:reset all colors with colors.reset; two
        subclasses foreground for foreground
        and background for background; use as colors.subclass.colorname.
        i.e. colors.foreground.red or colors.background.green also, the generic bold, disable,
        underline, reverse, strike through,
        and invisible work with the main class i.e. colors.bold
        author£ºios_shogun-Atomic¾ý
        date:2023-2-24
        self:IOS_SHOGUN_studio"

shogun.modul content-console:
        
        "The 'console' micro-logging system carries its own 'BufferByte' when using the console,
        which can be used for multithreaded operation processing, which is divided into 5 levels - error,
        warning, message. Debugging, correct, each level has a different effect,
        of course you can go through the 'disposition' configuration of it,
        Export can drive IO logs Of course, you can also configure the log name,
        and whether it is continuous,Configure via 'Continuity'
        In a continuous state, each 'debug...' debug will drive the IO log generation and
        the emptying of 'bufferByte', 'bufferByte' it is in unlimited mode - you can set the same log path,
        I have introduced simple information, please go down for information
        author£ºios_shogun-Atomic¾ý
        date:2023-2-24
        self:IOS_SHOGUN_studio"