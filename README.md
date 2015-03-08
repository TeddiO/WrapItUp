# WrapItUp
WrapItUp is a wrapper for the (Python 3) library pyMySQL to quickly get queries rolling.

At the moment there are two often used mysql libraries often used, the generic one provided by Oracle (which is fairly terrible) and
pyMySQL which is a pure python implementation, which is actually quite lovely. The only downside is it's a little elaborate and explcit
(in true Python form!) so quickly rolling out code quickly can be troublesome.

###Heres where WrapItUp comes in to play!

The main power behind WrapItUp comes from the fact you just the following:

```Python
myDB = WrapItUp(username='test',password='test', ip='Localhost', database='test_schema')
myData = myDB.Query(<query>,[<args>])
```

And boom! you have your data returned in a Tuple.

Wait! I hear you say, what about if I don't want multple sets of data, but just one?!
Well, the solution is simple! Using the database from before - 

```python
mySingleData = myDB.Query(<query>,[<args>], single=True)
```
And voila! A single row of returned data!


Beyond all the smooth magic above, you're also capable of creating and using separate cursors by using the 'cursor=<cursorObject> parameter.

You're even able to specify a callback function if required for your data, which will pass your returned data as a parameter!

```python
mySingleData = myDB.Query(<query>,[<args>], callbackFunction=myFunctionHere)
```

