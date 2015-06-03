class BassetIos < Formula
    homepage "https://github.com/Polidea/basset-ios"
    url "https://github.com/Polidea/basset-ios/archive/0.1.tar.gz"
    sha1 "054fbb255c9a1daf7666466132469528f685b623"

    depends_on :python if MacOS.version <= :snow_leopard
    depends_on "imagemagick"

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
