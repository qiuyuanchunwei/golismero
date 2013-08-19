What's GoLismero 2.0?
=====================

GoLismero is an open source framework for security testing. It's currently geared towards web security, but it can easily be expanded to other kinds of scans.

The most interesting features of the framework are:

- Real platform independence. Tested on Windows, Linux, *BSD and OS X.
- No native library dependencies. All of the framework has been written in pure Python.
- Good performance when compared with other frameworks written in Python and other scripting languages.
- Very easy to use.
- Plugin development is extremely simple.
- The framework also collects and unifies the results of well known tools: sqlmap, xsser, openvas, dnsrecon, theharvester...
- Integration with standards: CWE, CVE and OWASP.
- Designed for cluster deployment in mind (not available yet).

Quick help
==========

Using GoLismero 2.0 is very easy. Below are some basic commands to start to using it:

Installing
----------

Currently GoLismero 2.0 is under active development so it isn't in the main branch of the github project. To download it, you must write the following:

```git clone -b 2.0.0 https://github.com/cr0hn/golismero.git golismero-2.0```

Basic usage
-----------

This command will launch GoLismero with all default options and show the report on standard output:

```python golismero.py <target>```

You can also set a name for your audit with --audit-name:

```python golismero.py <target> --audit-name <name>```

And you can produce reports in different file formats. The format is guessed from the file extension, and you can write as many files as you want:

```python golismero.py <target> -o <output file name>```

![Run example](https://raw.github.com/cr0hn/golismero/gh-pages/images/run_mac_2.png "Run example")

Additionally, you can import results from other tools with the -i option. You can use -i several times to import multiple files. This example shows how to parse the results from a Nikto scan and produce a report. To keep GoLismero from re-scanning the target, we'll disable all plugins:

```python golismero.py www.example.com -i nikto_output.csv -o report.html -d all```

![Import export example](https://raw.github.com/cr0hn/golismero/gh-pages/images/import_export_win.png "Import export example")

All results are automatically stored in a database file. You can prevent this with the -nd option:

```python golismero.py <target> -nd```

![No database example](https://raw.github.com/cr0hn/golismero/gh-pages/images/no_db_mint.png "No database example")

This allows you to scan the target in one step, and generating the report later. For example, to scan without generating a report:

```python golismero.py <target> -db database.db -no```

And then generate the report from the database at a later time (or from a different machine!):

```python golismero.py -db database.db -d all -o report.html```

Available plugins
-----------------

To display the list of available plugins:

```python golismero.py --plugin-list```

![Plugin list example](https://raw.github.com/cr0hn/golismero/gh-pages/images/plugin_list_mac_2.png "Plugin list example")

You can also query more information about specific plugins:

```python golismero.py --plugin-info <plugin name>```

![Plugin info example](https://raw.github.com/cr0hn/golismero/gh-pages/images/plugin_info_mint.png "Plugin list example")

Select a specific plugin
------------------------

Use the -e option to enable only some specific plugins, and -d to disable plugins (you can use -e and -d many times):

```python golismero.py <target> -e <plugin id>```

![Run plugin example](https://raw.github.com/cr0hn/golismero/gh-pages/images/run_plugin_mac_2.png "Run plugin example")

What will be the next features?
===============================

The next features of golismero will be:

- Integration with Nmap, SQLMap, Metasploit and many other tools.
- Web UI. We all know true h4xx0rs only use the console, but sometimes drag&drop does come in handy. ;)
- Export results in PDF format.
- And more plugins of course!

Need help? Found a bug?
=======================

If you have found a bug, you can report it using the Github issues system. You can also drop us an email (golismero.project@gmail.com) or find us on Twitter (@golismero_pro).
