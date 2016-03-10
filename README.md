# image_clusters

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
