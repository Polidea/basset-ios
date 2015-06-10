#Basset-ios

[![Build Status](https://travis-ci.org/Polidea/basset-ios.svg?branch=master)](https://travis-ci.org/Polidea/basset-ios)

**Basset** is an image converting and organizing tool, that allows developers to take care of only vector versions of assets used in iOS projects.

Main features of **Basset** can be describd in two steps:

1. Converting vector images (.eps, .pdf, .psd, .svg) to PNG(s) with resolutions and names properly recognized by iOS apps (@2x, @3x etc.)
2. Copying assets from previous steps to selected .xcasset files and creating proper JSONs there.


####Why just don't use XCode's PDF support?

1. Each PDF what is drag-and-dropped to XCode is assigned to @1x category in xcassets. For each of them you need to drag them again to "All" category, what is really painful when you're using hundreads of images in your projects.
2. Check of this link: [http://bjango.com/articles/idontusepdfs/](http://bjango.com/articles/idontusepdfs/)

##Getting started

###Prerequisites

**Basset** requires:

* OSX (tested on Yosemite)
* Homebrew or docker installed 

It should also work on other Unix-like system, but it wasn't tested there.


###Installation

####Homebrew

Open your terminal and type

```
brew tap Polidea/tap
brew install basset_ios
```

####Known issues

in case you've recieved this error:

```
Error: undefined method `desc' for ...
```

please make sure you've newest version of homebrew. You can update it by running ```brew update``` command

####Docker

```
TBD
```

##Usage

In order to use **Basset** you need to tell which directory you're using to store vector images, where generated PNGs will be store etc. You can do this by following naming convention written below, or by specifying explicit configuration via command line parameters or dedicated configuration file.

Remember that you'll have to create .xcassets directory that you want to use **on your own**. If you'll have more than one .xcassets in your project, you'll need to specify which one you want **Basset** to operate on.

### Naming convention

In order to use **Basset** you need to place:

* All vector images used in the project needs to be stored in ```Resources/Assets``` directory
* Default *xcassets* directory needs to be in ```Resources/Images.xcassets```
* Generated PNG(s) will be stored in ```Resources/GeneratedAssets``` directory


If you'll follow this convention, you can can run **Basset** in root directory of your iOS project, and all vector images will be processed, and stored in proper xcassets directory.

If you'd like to use different settings, you need to provide configuration file, or override default settings in command line.


###Config file

```
# Default xcasset dir
xcassets_dir: Resources/Images.xcassets

# Where vector images are kept
raw_assets: Assets

# Where generated PNG(s) will be kept
generated_assets_dir: GeneratedAssets

# Should generated PNG(s) be merged to xcassets folder
merge_with_xcassets: True

# Should convert all assets every time
force_convert: False
```

#### Example

You can run **Basset** with configuration file by providing path to it as ```-c``` parameter, for example:

```
basset-ios -c "Assets/config.yml"
```

###Command line
```
basset-ios [-h] [-d XCASSETS_DIR] [-a RAW_ASSETS_DIR]
                 [-g GENERATED_ASSETS_DIR] [-m MERGE_WITH_XCASSETS]
                 [-c CONFIG]

optional arguments:
  -h, --help										show help message and exit
  -x, --xcassets_dir XCASSETS_DIR					path to directory with default xcassets directory
  -r, --raw_assets_dir RAW_ASSETS_DIR				path to directory with raw, vector based graphics
  -g, --generated_assets_dir GENERATED_ASSETS_DIR	path to directory where generated PNGs will be stored
  -m, --merge_with_xcassets MERGE_WITH_XCASSETS		will script process xcassets directories
  -f, --force_convert FORCE_CONVERT					should regenerate assets even when they were generated before
  -c, --config CONFIG								path to config file
```                        

## Example

1) First of all create new iOS project. Make sure it contains *xcassets* folder inside.

<img src="./readme_resources/1.png" style="width: 300px;"/>

2) Create Assets folder, and put all your vector images in there.

<img src="./readme_resources/2.png" style="width: 200px;"/>

3) Create config file:

```
xcassets_dir: test_basset/Images.xcassets
raw_assets: Assets
generated_assets_dir: GeneratedAssets
merge_with_xcassets: True
force_convert: False
``` 

and save it as config.yml in project root folder:

<img src="./readme_resources/3.png" style="width: 200px;"/>

4) Open terminal, change current directory to your iOS project, and type:

```
basset_ios -c config.yml
```

5) All vector images should be converted to PNGs and put into selected ```xcassets``` folder.

<img src="./readme_resources/5.png" style="width: 600px;"/>

All images are now visible in XCode:

<img src="./readme_resources/4.png" style="width: 600px;"/>

##License
Basset-ios is released under a MIT License. See LICENSE file for details.
