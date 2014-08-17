How to setup cxxtags on cygwin
--------------

### List of dependent libraries

* libclang
* leveldb
* Plyvel
* boost

### How to setup libraries

* libclang
    * Easiest way to install libclang is to use cygwin package.
        * Install using setup.exe
        * Or use apt-cyg

                $ apt-cyg install libclang-devel

* leveldb
    * Install from source package
    * You need add some modification to original source package to build leveldb on cygwin.
      Refer this site for more detail
        * http://www.ideawu.com/blog/2012/11/compiling-leveldb-on-windows-cygwin.html

                wget https://leveldb.googlecode.com/files/leveldb-1.15.0.tar.gz
                tar zxvf leveldb-1.15.0.tar.gz
                cd leveldb-1.15.0
                # edit some files
                make
                mkdir -p /pkg/leveldb/lib/
                cp libleveldb* /pkg/leveldb/lib
                cp -a include /pkg/leveldb/


* Plyvel
    * Refer this site.
        * https://plyvel.readthedocs.org/en/latest/installation.html#build-and-install-plyvel

* boost
    * Most easiest way to install boost is to use cygwin package.
        * install using setup.exe
        * or use apt-cyg

                $ apt-cyg install libboost-devel

### And then build cxxtags

        git clone https://github.com/katonori/cxxtags.git
        cd cxxtags/src/
        mkdir build && cd build
        cmake -DLLVM_HOME=/usr/ -DLEVELDB_HOME=/pkg/leveldb/ -DBOOST_HOME=/usr/ ../
        make install

