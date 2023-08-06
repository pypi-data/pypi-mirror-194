python-docx-2023
==========

Python library forked from  `python-docx <github.com/python-openxml/python-docx/>`_.

The main purpose of the fork was to add implementation for comments and footnotes to the library

Installation
------------

Use the package manager `pip <pypi.org/project/python-docx-2023/>`_ to install python-docx-2023.


`pip install python-docx-2023`

Usage
-----

::
    
    import docx
    
    document = docx.Document()

    paragraph1 = document.add_paragraph('text') # create new paragraph

    comment = paragraph.add_comment('comment',author='Obay Daba',initials= 'od') # add a comment on the entire paragraph

    paragraph2 = document.add_paragraph('text') # create another paragraph

    run = paragraph2.add_run('texty') add a run to the paragraph

    run.add_comment('comment') # add a comment only for the run text 

    run.add_comment('comment2')

    run_comments = run.comments

    paragraph1.add_footnote('footnote text') # add a footnote

    paragraph2.add_footnote('footnote text') # add a footnote

    fn_lst = document.footnotes # list of footnotes in the document
    
    fn_text = [fn.text for fn in fn_lst]


License
-------

`MIT <https://choosealicense.com/licenses/mit/>`_
