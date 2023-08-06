
# Name Sanitizer

### _Motivation_

This package arises from the need to clean file and directory names to be able to include them in our different projects. Sometimes these files are usually many and are at different levels of depth, for example, google sources.
At other times we want to have an image repository but the names are very varied and / or contain special characters not supported for imports in some languages ... this package will help you with that.

Let's not forget the good android studio, surely you are already tired of manually renaming the files.

### Install
```` pip install name-sanitizer ````

### Simple usage
````python -m ns````

The package will work in the current path where the console is open. Remember that in Linux you can open the terminal contextually and in Windows, you can click on the breadcrumb in the folder, type cmd, press enter and the console will open in that path.

### Options

````--a```` => Replace the file or directory name with an anonymous one.

````--r```` => Run the sanitizer recursively from the current directory.

````--only_dir```` => Run the sanitizer for directories only

````--only_file```` => Run the sanitizer for files only

````--extensions```` => Defines the specific extensions where the sanitizer will act. (By default it includes directories)


### Options usage
All the parameters except the extensions work as a flag, if you set it, it will work.

###### Example:

````python -m ns --r --a````

This will run the sanitizer recursively anonymizing files for child directories

##### Extensions: 

You can define that the sanitizer only works on files with a certain extension. To do this, you must specify the extensions including the period, if there is more than one you must add them with a comma and without spaces.

###### Example:

````python -m ns --extension=.ttf,.mp3 --r --only_file````

This will run the sanitizer recursively only for files with the extension .ttf and .mp3 without renaming the directories.
