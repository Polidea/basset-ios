class Basset_ios < Formula
    homepage "https://github.com/Polidea/basset-ios"
    url "https://github.com/Polidea/basset-ios/releases/download/0.1/basset_ios.zip"
    sha1 "5d914431966449af7a7aa85f091f161d4a3c2fa8"
    version "0.1"
    
    depends_on :python if MacOS.version <= :snow_leopard
    
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
        %w[coloredlogs Wand PyYAML`].each do |r|
            resource(r).stage do
                system "python", *Language::Python.setup_install_args(libexec/"vendor")
            end
        end
        ENV.prepend_create_path "PYTHONPATH", libexec/"lib/python2.7/site-packages"
        system "python", *Language::Python.setup_install_args(libexec)
        bin.install Dir[libexec/"bin/*"]
        bin.env_script_all_files(libexec/"bin", :PYTHONPATH => ENV["PYTHONPATH"])
    end

    test do
        system "#{bin}/basset_ios", "-h"
    end
end
