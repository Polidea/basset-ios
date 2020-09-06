<p align="center" >
<img src="./readme_resources/basset_bg.png" alt="basset" title="basset"/>
</p>

[![Build Status](https://travis-ci.org/Polidea/basset-ios.svg)](https://travis-ci.org/Polidea/basset-ios)

**Basset** is an image converting and organizing tool, that allows developers to take care of only vector versions of assets used in iOS projects.

Main features of **Basset** can be described in two steps:

1. Converting vector images (.svg, .eps, .pdf, .psd) to PNG(s) with resolutions and names properly recognized by iOS apps (`@2x`, `@3x`, etc.)
2. Copying assets from previous steps to selected .xcasset files and creating proper JSONs there.


#### Why just don't use Xcode's PDF support?

1. Each PDF that is drag-and-dropped into Xcode is assigned a `@1x` dimension in the xcasset, by default. You need to update each of them to "Single Scale", which's really painful when you're using hundreds of assets in your projects.
2. It's easier to manage ordinary directory of assets than .xcassets. You don't have to use Xcode to do that. So even non-developers can add resources to the project.
3. Must-read: [http://bjango.com/articles/idontusepdfs/](http://bjango.com/articles/idontusepdfs/)

## Getting started

### Prerequisites

**Basset** requires:

* macOS
* [Homebrew](https://brew.sh)

It should also work on other [Unix-like](https://en.wikipedia.org/wiki/Unix-like) systems, but it wasn't tested anywhere but macOS Catalina.

### Installation

On your Terminal, run:

```javascript
brew tap Polidea/tap
curl -s https://raw.githubusercontent.com/rogerluan/basset-ios/master/patched_basset_ios.rb > /usr/local/Homebrew/Library/Taps/polidea/homebrew-tap/basset_ios.rb
brew install imagemagick
brew install basset_ios
```

Add this to your `~/.zshrc` file (or your bash profile file, depending on your shell environment):
```javascript
# The last part of the path should be whatever version of imagemagic@6 you have installed. Type in until the imagemagic@6 part and then press Tab to let it auto-complete with the version it has installed.
export MAGICK_HOME=/usr/local/Cellar/imagemagick@6/6.9.11-28/
```

After adding the `export` line, close Terminal and reopen it. Alternatively, you can run that same line as a command in Terminal.

#### Upgrading

To upgrade **Basset**, type:

```javascript
brew update
brew upgrade basset_ios
```

#### Adobe Illustrator save to .SVG options

In order to export assets form Adobe Illustrator to SVG files that are supported by **Basset**, you need to select "CSS Properties" set as "Style Attributes".

Also keep in mind to convert all fonts in the artboards to outlines (you can also use "Convert to outline" option during saving).

<img src="./readme_resources/illustrator.png" style="width: 400px;"/>

#### Troubleshooting

#### Incorrect gradients when using SVG files

In order to convert SVGs with gradients to PNGs, we're using *librsvg*. The problem is that this library installed incorrectly by Homebrew. To fix this, we need to reinstall it:

```javascript
brew uninstall librsvg
brew uninstall basset_ios
brew install basset_ios
```

## Usage

**Basset** can be used either by passing command line arguments, or by passing a config yaml file.

SVG is the recommended vector file format for **Basset**.

Remember you'll have to create .xcassets directory that you want to use **on your own**, and if you have more than one .xcassets in your project, you'll need to specify which one you want **Basset** to operate on.

### Config file

```yaml
# The xcasset directory to operate on.
xcassets_dir: Assets.xcassets

# Where vector images are kept.
raw_assets: VectorAssets

# Where generated PNG(s) will be kept.
generated_assets_dir: GeneratedAssets

# Whether the script should generated PNG(s) be merged to xcassets folder.
merge_with_xcassets: true

# Whether the script should convert all assets every time.
force_convert: false
```

#### Example

You can run **Basset** with configuration file by providing path to it as `-c` parameter, such as:

```javascript
basset_ios -c "Assets/config.yml"
```

### Command line

```javascript
usage: basset_ios [-h] [-r RAW_ASSETS_DIR] [-x XCASSETS_DIR]
                  [-g GENERATED_ASSETS_DIR] [-f FORCE_CONVERT]
                  [-m MERGE_WITH_XCASSETS] [-e EXTRACT_PATH] [-c CONFIG]

Converts raw assets to proper PNG(s).

optional arguments:
  -h, --help            Show this help message and exit
  -r RAW_ASSETS_DIR, --raw_assets_dir RAW_ASSETS_DIR
                        Path to directory with raw, vector based graphics.
                        Defaults to `VectorAssets`.

Main arguments:
  Assets converting and merging with xcassets

  -x XCASSETS_DIR, --xcassets_dir XCASSETS_DIR
                        Path to directory with default xcassets directory.
                        Defaults to `Assets.xcassets`.
  -g GENERATED_ASSETS_DIR, --generated_assets_dir GENERATED_ASSETS_DIR
                        Path to directory where generated PNGs will be stored.
                        Defaults to `GeneratedAssets`.
  -f FORCE_CONVERT, --force_convert FORCE_CONVERT
                        Whether the script should convert all assets every time.
                        Defaults to `false`.
  -m MERGE_WITH_XCASSETS, --merge_with_xcassets MERGE_WITH_XCASSETS
                        Whether the script should generated PNG(s) be merged to xcassets folder.
                        Defaults to `true`.
  -c CONFIG, --config CONFIG
                        path to config file

Extract arguments:
  Extracting assets from existing .xcassets

  -e EXTRACT_PATH, --extract_path EXTRACT_PATH
                        if set to existing xcassets directory, will extract
                        all assets from it to `raw_assets_dir`
```

## Extracting Assets From Existing .xcassets

If you have an existing project with PDFs, you can extract them to a separate directory, making them available for future use. To do that, run:

```javascript
basset_ios -e <path_to_xcassets_dir> -r <path_to_vector_assets_dir>
```

## Example

1. First of all create new iOS project. Make sure it contains *xcassets* folder inside.

<img width="200" src="readme_resources/1.png">

2. Create Assets folder, and put all your vector images in there.

<img width="200" src="readme_resources/2.png">

3. Create a `config.yml` file:

```yaml
xcassets_dir: test_basset/Images.xcassets
raw_assets: Assets
generated_assets_dir: GeneratedAssets
merge_with_xcassets: true
force_convert: false
```

and save it as `config.yml` in project root folder:

<img width="200" src="readme_resources/3.png">

4. Open terminal, change your current directory to your iOS project, and run:

```javascript
basset_ios -c config.yml
```

Done!

Now all images should be visible in Xcode:

<img width="600" src="readme_resources/4.png">

And all vector images should be converted to PNGs and put into the specified `xcassets` folder:

<img width="600" src="readme_resources/5.png">

## License

**Basset-ios** is released under a MIT License. See LICENSE file for details.
