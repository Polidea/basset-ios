#Basset-ios

**Basset** is an image converting and organizing tool, that allows developers to take care of only vector versions of assets used in iOS projects.

Main features of **Basset** can be describd in two steps:

1. Converting vector images (.eps, .pdf, .psd, .svg) to PNG(s) with resolutions and names properly recognized by iOS apps (@2x, @3x etc.)
2. Copying assets from previous steps to selected .xcasset files

##Getting started

###Prerequisites

**Basset** requires:

* OSX (tested on Yosemite)
* Homebrew or docker installed 

###Installation

####Homebrew

```
TBD
```

####Docker

```
TBD
```

##Usage

In order to use **Basset** you need to tell which directory you're using to store vecotr images, where generated PNGs will be store etc. You can do this by following naming convention written below, or by specifying explicit configuration via command line parameters or dedicated configuration file.

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
  -c, --config CONFIG								path to config file
```                        


###License
Basset-ios is released under a MIT License. See LICENSE file for details.