class BassetIos < Formula
  desc "Converts vector images to PNG and puts them in xcassets"
  homepage "https://github.com/Polidea/basset-ios"
  url "https://github.com/Polidea/basset-ios/archive/1.4.2.tar.gz"
  sha256 "0893f09128a863218c3f0e66608b83bfe06cdf75cb4587761220e304ebdfca5c"

  depends_on :python if MacOS.version <= :snow_leopard
  depends_on "imagemagick@6" => "--with-librsvg"
  depends_on "ghostscript"

  resource "coloredlogs" do
    url "https://pypi.python.org/packages/source/c/coloredlogs/coloredlogs-1.0.tar.gz"
    sha256 "35e1e8a422b27d8c8e66eaa30d5dfff80d9c233bd52543e10b79688781b0510b"
  end

  resource "Wand" do
    url "https://github.com/rameshdharan/wand/archive/154e1d2ae42722efe17c4824562b4c40a36e87aa.zip"
    sha256 "fcc340145634644c784565a8feba7a02b24ae903aee633383d9df96313a438ff"
  end

  resource "PyYAML" do
    url "https://pypi.python.org/packages/source/P/PyYAML/PyYAML-3.11.tar.gz"
    sha256 "c36c938a872e5ff494938b33b14aaa156cb439ec67548fcab3535bb78b0846e8"
  end

  resource "humanfriendly" do
    url "https://pypi.python.org/packages/source/h/humanfriendly/humanfriendly-1.26.tar.gz"
    sha256 "0908b90298364e3335a03abcbb88ec571f95c7e4bc6728de0551806f636ef219"
  end

  def install
    ENV.prepend_create_path "PYTHONPATH", libexec/"vendor/lib/python2.7/site-packages"
    resources.each do |r|
      r.stage do
        system "python", *Language::Python.setup_install_args(libexec/"vendor")
      end
    end

    ENV.prepend_create_path "PYTHONPATH", libexec

    libexec.install "basset"
    bin.install "basset_ios"

    bin.env_script_all_files(libexec/"bin", :PYTHONPATH => ENV["PYTHONPATH"])
  end

  test do
    system "#{bin}/basset_ios", "-h"
  end
end
