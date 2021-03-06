========
Glossary
========

..  glossary::
    :sorted:

    AMCP
        The *Advanced Media Control Protocol*, or AMCP, is :term:`CasparCG`'s primary way of communicating with clients.
        Command strings are issued over a TCP socket to a given port on a CasparCG Server. CasparCG then parses the command and returns a string over the same socket, informing the user of the validity of the given command and any information that the user has requested.
        AMCP can be used to load, play and stop media on the server, manipulate datasets, and get or set information about the server itself.

    CasparCG
    CCG
        Open-source software developed by SVT, designed to play video content to a number of outputs, but can also manipulate the video's colour and spatial properties, as well as playing Flash- and HTML-based templates out, so as to be able to create keyed graphics.
        See `CasparCG Server <http://casparcg.com>`_ for more details.

    Character generator
    Graphics machine
    CG
        Primarily used in TV, a character generator (CG) is a computer that creates on-screen graphics that can be keyed over an image. Some of the most common graphics that CGs create include lower-third straps (that might show the name of a TV presenter) or leaderboards in sports programmes.

    SVT
        *Sveriges Television*, the Swedish national broadcasting organisation, and developers of CasparCG. They use CasparCG to control the output of their 6 TV channels.

    UberCarrot
    UC
        This project, but including CasparCG, which is separately maintained and developed by the Swedish national broadcaster,
        SVT.