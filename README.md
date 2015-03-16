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


Beyond all the smooth magic above, you're also capable of creating and using separate cursors.

```python
aNewCursor = myDB.CreateCursor('DictsAreAwesome', type=db.cursors.DictCursor)
charData = db.Query(<query>, [<args>], cursor = aNewCursor)
```

By default four cursor types are available directly via WrapItUp, these being - 
- Cursor (default)
- DictCursor
- SSCursor
- SSDictCursor

Any other pymysql cursors can be passed instead if required. 


You're even able to specify a callback function if required for your data, which will pass your returned data as a parameter!

```python
mySingleData = myDB.Query(<query>,[<args>], callbackFunction=myFunctionHere)
```

##Finally..

> This doesn't seem so good for x project of mine...

The truth of it is, this is meant to get things off the ground incredibly quickly. For fine-grain control or situations where you need to validate your input to the database for committing, you're better off writing your own library or using the standard controls.

> This doesn't seem to fit with \<insert design spec here\>

For the most part, it comes down to personal preference and Python throwing warnings as opposed to errors. In the age-old 
argument of spaces vs tabs, I prefer tabs. Likewise I don't mind my code >75 chars per line.

> Can I contribute to try and somehow make this better?

By all means! Any change is good change if that means getting things off the ground quicker (in a nice way of course)!

