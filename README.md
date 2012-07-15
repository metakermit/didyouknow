Prerequirements:

 - create a group for all users

        sudo adduser --group focweb

To add a new user called john:

 - set his/her main group to focweb:
        sudo usermod -g focweb john
 - append the following command to the end of his/her ~/.bashrc file:

        umask 003

To push to the server simply push to this branch:

        bzr+ssh://john@lis.irb.hr//var/www/foc/

On the server side do a:

        bzr update

(or install the push-and-update plugin as explained [here][http://wiki.bazaar.canonical.com/BazaarForWebDevs])
