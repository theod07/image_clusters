# image_clusters
## Setting up MongoDB
Find out the info of your machine. For Ubuntu:
```
$ lsb_release -a
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 14.04.3 LTS
Release:        14.04
Codename:       trusty
```
Instructions [here](https://docs.mongodb.org/master/tutorial/install-mongodb-on-ubuntu/)
1. Import the public key.
2. Create a list file for MongoDB
3. Reload local package database.
4. Install the latest stable version of MongoDB.
5. ( ** Pin a specific version of MongoDB ** )
```
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
sudo apt-get update
sudo apt-get install -y mongodb-org
echo "mongodb-org hold" | sudo dpkg --set-selections
echo "mongodb-org-server hold" | sudo dpkg --set-selections
echo "mongodb-org-shell hold" | sudo dpkg --set-selections
echo "mongodb-org-mongos hold" | sudo dpkg --set-selections
echo "mongodb-org-tools hold" | sudo dpkg --set-selections
```


<br>
Run MongoDB Community Edition
1. Start MongoDB

    sudo service mongod start

2. Verify that MongoDB has started successfully

    [initandlisten] waiting for connections on port <port>

3. Stop MongoDB

    sudo service mongod stop

4. Restart MongoDB

    sudo service mongod restart


<br>

## rendering images on EC2
AWS ec2 instances don't have capability to render images, which poses a problem while we're trying to load images. The popular/common packages that are used to load images (`PILLOW`, `matplotlib.pyplot`, `skimage.io`) seem to rely on image render-fication.
Let's see if we can figure out how to configure `matplotlib` to suit our needs..

learn about [matplotlib's backend](http://matplotlib.org/faq/usage_faq.html#what-is-a-backend)
renderer 'AGG' seems to be working okay for reading in images.
`Note`: it's not helpful to add the command into the script. I had to modify the matplotlibrc file to get it to run properly.

<br>

## scp
Examples

Copy the file "foobar.txt" from a remote host to the local host

    $ scp your_username@remotehost.edu:foobar.txt /some/local/directory
Copy the file "foobar.txt" from the local host to a remote host

    $ scp foobar.txt your_username@remotehost.edu:/some/remote/directory
Copy the directory "foo" from the local host to a remote host's directory "bar"

    $ scp -r foo your_username@remotehost.edu:/some/remote/directory/bar
Copy the file "foobar.txt" from remote host "rh1.edu" to remote host "rh2.edu"

    $ scp your_username@rh1.edu:/some/remote/directory/foobar.txt \
your_username@rh2.edu:/some/remote/directory/
Copying the files "foo.txt" and "bar.txt" from the local host to your home directory on the remote host

    $ scp foo.txt bar.txt your_username@remotehost.edu:~
Copy the file "foobar.txt" from the local host to a remote host using port 2264

    $ scp -P 2264 foobar.txt your_username@remotehost.edu:/some/remote/directory
Copy multiple files from the remote host to your current directory on the local host

    $ scp your_username@remotehost.edu:/some/remote/directory/\{a,b,c\} .
    $ scp your_username@remotehost.edu:~/\{foo.txt,bar.txt\} .


<br>

## tmux
start new:

    tmux

start new with session name:

    tmux new -s myname

attach:

    tmux a  #  (or at, or attach)

attach to named:

    tmux a -t myname

list sessions:

    tmux ls

<a name="killSessions"></a>kill session:

    tmux kill-session -t myname

<br>

## Scraping
open up the site, open up developer tools with `cmd+option+i` and look at the network tab. the request URL for each image should be listed.


<br>

## MongoDB Structure
Store data for each item in a nested dictionary.
Dictionary top level is keyed by users.
Level two is keyed by each img.
Level three is keyed by the information of the img.

```json
{ { "user1" :
      { "img1" :
          { "key" : "special hash string identifier",
            "src_url" : "url for full image",
            "vector" : "output vector from AlexNet",
            "cluster" : "result of cluster algorithm" } },
      { "img2" :
          { "key" : "special hash string identifier",
            "src_url" : "url for full image",
            "vector" : "output vector from AlexNet",
            "cluster" : "result of cluster algorithm" } } },
    { "user2" :
        { "img1" :
            { "key" : "special hash string identifier",
              "src_url" : "url for full image",
              "vector" : "output vector from AlexNet",
              "cluster" : "result of cluster algorithm" } },
        { "img2" :
            { "key" : "special hash string identifier",
              "src_url" : "url for full image",
              "vector" : "output vector from AlexNet",
              "cluster" : "result of cluster algorithm" } } }
}
```

<br>

## Setting up Lasagne

1.Verify you have Python2.7 or Python3.4
```python
```

2. Create new environment. Make sure you switch over to that environment.
```python
conda create --name lasagne_env python=2
source activate lasagne_env
```
3. Install C compiler for OSX via pip
```python
pip install clang
```
4. Update numpy to v1.6.2 or greater. Update scipy to v0.11 or greater.
```python
conda install numpy
conda install scipy
```
5. Run command below to get the latest known good version of Theano
```python
pip install -r https://raw.githubusercontent.com/Lasagne/Lasagne/v0.1/requirements.txt
```
6. Install Lasagne
```python
pip install Lasagne==0.1
```
7.

<br>

## Troubleshooting
Ran into an issue while going through the tutorial. running example/mnist.py gave the following error:
```python
$ python mnist.py
Loading data...
Downloading train-images-idx3-ubyte.gz
Downloading train-labels-idx1-ubyte.gz
Downloading t10k-images-idx3-ubyte.gz
Downloading t10k-labels-idx1-ubyte.gz
Building model and compiling functions...
Traceback (most recent call last):
  File "mnist.py", line 359, in <module>
    main(**kwargs)
  File "mnist.py", line 281, in main
    train_fn = theano.function([input_var, target_var], loss, updates=updates)
  File "/Users/wonder/anaconda/envs/lasagne_env/lib/python2.7/site-packages/theano/compile/function.py", line 316, in function
    output_keys=output_keys)
  File "/Users/wonder/anaconda/envs/lasagne_env/lib/python2.7/site-packages/theano/compile/pfunc.py", line 523, in pfunc
    output_keys=output_keys)
  File "/Users/wonder/anaconda/envs/lasagne_env/lib/python2.7/site-packages/theano/compile/function_module.py", line 1526, in orig_function
    defaults)
  File "/Users/wonder/anaconda/envs/lasagne_env/lib/python2.7/site-packages/theano/compile/function_module.py", line 1390, in create
    input_storage=input_storage_lists)
  File "/Users/wonder/anaconda/envs/lasagne_env/lib/python2.7/site-packages/theano/gof/link.py", line 607, in make_thunk
    output_storage=output_storage)[:3]
  File "/Users/wonder/anaconda/envs/lasagne_env/lib/python2.7/site-packages/theano/gof/vm.py", line 1025, in make_all
    no_recycling))
  File "/Users/wonder/anaconda/envs/lasagne_env/lib/python2.7/site-packages/theano/gof/op.py", line 807, in make_thunk
    no_recycling)
  File "/Users/wonder/anaconda/envs/lasagne_env/lib/python2.7/site-packages/theano/gof/op.py", line 733, in make_c_thunk
    output_storage=node_output_storage)
  File "/Users/wonder/anaconda/envs/lasagne_env/lib/python2.7/site-packages/theano/gof/cc.py", line 1065, in make_thunk
    keep_lock=keep_lock)
  File "/Users/wonder/anaconda/envs/lasagne_env/lib/python2.7/site-packages/theano/gof/cc.py", line 1007, in __compile__
    keep_lock=keep_lock)
  File "/Users/wonder/anaconda/envs/lasagne_env/lib/python2.7/site-packages/theano/gof/cc.py", line 1435, in cthunk_factory
    key=key, lnk=self, keep_lock=keep_lock)
  File "/Users/wonder/anaconda/envs/lasagne_env/lib/python2.7/site-packages/theano/gof/cmodule.py", line 1094, in module_from_key
    module = lnk.compile_cmodule(location)
  File "/Users/wonder/anaconda/envs/lasagne_env/lib/python2.7/site-packages/theano/gof/cc.py", line 1347, in compile_cmodule
    preargs=preargs)
  File "/Users/wonder/anaconda/envs/lasagne_env/lib/python2.7/site-packages/theano/gof/cmodule.py", line 2068, in compile_str
    return dlimport(lib_filename)
  File "/Users/wonder/anaconda/envs/lasagne_env/lib/python2.7/site-packages/theano/gof/cmodule.py", line 297, in dlimport
    rval = __import__(module_name, {}, {}, [module_name])
ImportError: ('The following error happened while compiling the node', Dot22(Flatten{2}.0, W), '\n', 'dlopen(/Users/wonder/.theano/compiledir_Darwin-14.5.0-x86_64-i386-64bit-i386-2.7.11-64/tmp5TsaA5/15357f4a51bff61fa945bea566107bed.so, 2): Library not loaded: libmkl_intel_lp64.dylib\n  Referenced from: /Users/wonder/.theano/compiledir_Darwin-14.5.0-x86_64-i386-64bit-i386-2.7.11-64/tmp5TsaA5/15357f4a51bff61fa945bea566107bed.so\n  Reason: image not found', '[Dot22(<TensorType(float64, matrix)>, W)]')
```

Recommendation from nouiz ([here](https://groups.google.com/forum/#!topic/theano-users/DcOZvOJqxUU)) is to use the bleeding edge versions.
```python
pip install --upgrade https://github.com/Theano/Theano/archive/master.zip
pip install --upgrade https://github.com/Lasagne/Lasagne/archive/master.zip
```

Ran mnist.py again after installation. Everything went well!
  | Hardware      | Train Time    |       |
  | ------------- |:-------------:| -----:|
  | MBP (12,1)    | ~15 sec/epoch |       |
  | AWS t2.micro  | ~25 sec/epoch |       |
  | AWS g2.8xlarge| ~1.5 sec/epoch|       |
