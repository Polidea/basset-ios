class BassetIos < Formula

    desc "Converting vector images to PNG(s) and organizes them in xcassets"
    homepage "https://github.com/Polidea/basset-ios"
    url "https://github.com/Polidea/basset-ios/archive/1.0.tar.gz"
    sha1 "18043152e4642e5baa5aad1c8bd2dda2546edefd"

    depends_on :python if MacOS.version <= :snow_leopard
    depends_on "imagemagick" => :build_from_source
    depends_on "ghostscript"

    resource "coloredlogs" do
        url "https://pypi.python.org/packages/source/c/coloredlogs/coloredlogs-1.0.tar.gz"
        sha1 "3ee63fac5640c9c8185814634f32656f837ee90d"
    end

    resource "Wand" do
        url "https://pypi.python.org/packages/source/W/Wand/Wand-0.4.0.tar.gz"
        sha1 "672c286e5202501f228145362db66a9a866b30d1"
    end

    resource "PyYAML" do
        url "https://pypi.python.org/packages/source/P/PyYAML/PyYAML-3.11.tar.gz"
        sha1 "1a2d5df8b31124573efb9598ec6d54767f3c4cd4"
    end

    resource "humanfriendly" do
        url "https://pypi.python.org/packages/source/h/humanfriendly/humanfriendly-1.26.tar.gz"
        sha1 "90bb0dec1be538f8b07764c15079eddc4d5dcfb6"
    end

    def install
        ENV.prepend_create_path "PYTHONPATH", libexec/"vendor/lib/python2.7/site-packages"
        resources.each do |r|
          r.stage do
            system "python", *Language::Python.setup_install_args(libexec/"vendor")
          end
        end

        ENV.prepend_create_path "PYTHONPATH", libexec

        libexec.install Dir["basset"]
        bin.install "basset_ios"

        bin.env_script_all_files(libexec/"bin", :PYTHONPATH => ENV["PYTHONPATH"])
    end

    test do
        system "#{bin}/basset_ios", "-h"
    end
end
