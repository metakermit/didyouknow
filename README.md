Prerequirements:

 - create a group for all users

        sudo adduser --group focweb

To add a new user called john:

 - set his/her main group to focweb:

        sudo usermod -g focweb john

 - append the following command to the end of his/her ~/.bashrc file:

        umask 003

To push to the server simply push to this branch from your client machine:

        bzr+ssh://john@lis.irb.hr//home/dlucanin/projekti/lp/foc

On the server side do a:

        bzr update

(or install the push-and-update plugin as explained [here][http://wiki.bazaar.canonical.com/BazaarForWebDevs])

Old location, unused atm:

        bzr+ssh://john@lis.irb.hr//var/www/foc/

This is unused, as /var/www/ is stated as an unsafe location [here][https://docs.djangoproject.com/en/1.4/intro/tutorial01/] to store Django code, as it can be browsed on some web servers and publicly reveal the application's source code.

If you don't like entering your password every time, you can copy your ssh keys from the Linux client you are using for submitting changes:

        ssh-copy-id john@lis.irb.hr


Installing Django
-----------------

        sudo apt-get install python-django

or to run a dev version:

        git clone git://github.com/django/django.git django-trunk
        sudo pip install -e django-trunk/