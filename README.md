LightDM greeter using WebKit presentation layer.

# Installation

    $ sudo apt-get install python-stdeb lightdm python-gobject gir1.2-gtk-3.0 gir1.2-webkit-3.0 gir1.2-lightdm-1 liblightdm-gobject-1-0
    $ make deb
    $ sudo dpkg -i deb_dist/<package.deb>


# Test run

Create test configuration for LightDM:

    [SeatDefaults]
    greeter-session=lightdm-pywebkit-greeter

    $ lightdm --test-mode -c <test.conf> --debug


# System install

    $ sudo /usr/lib/lightdm/lightdm-set-defaults --greeter=lightdm-pywebkit-greeter


# Developers

The JavaScript is generated from CoffeeScript, CSS from SCSS. You can autogenerate these in the background using Guard.

    $ gem install bundler
    $ bundle install
    $ bundle exec guard

