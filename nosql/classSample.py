"""
{year: {$gt:1893}}
{countries: ["Germany","USA"]}

$all : will check if the attribute is included, even though it was not the only attribute 
        if multiple attributes then order does not matter 
$lt :  selects the documents where the value of the field is less than (i.e. <) the specified value.
$or : or  symbol 
documentname.subattribute : attribute 


https://jsonviewer.stack.hu/


group agg 
{
    _id:{ID : "$imdb.rating"},
    NumMovies: {
        $count:{}
    }
}

OR use the code below to work 

{
    _id: "$imdb.rating",
    NumMovies: {
        $count:{}
    }
}
 {year: {$gt:2000}}

 {year: {$gt:1893}, runtime:{$lt:20}}
 
 {countries: ["Germany", "USA"] } //search entries that have exactly these two values in the exact same order

 {countries: { $all: ["USA"] } }   //search entries that include USA

 {countries: { $all: ["USA", "Germany"] } } //search for entries that satisfy both conditions in any order

 {$or: [{countries: { $all: ["USA"] } }, {countries: { $all: ["Germany"] } }] }   //entries that include either Germany OR USA (or both) 

 {cast: { $all: ["Meg Ryan"] } }

 { "imdb.rating":5.2 }

 { "imdb.rating": {$gt:8} }
 
 { "imdb.rating": {$gt:8, $lt:10}}

 {$or: [{countries: ["Germany", "USA"]}, {countries: ["USA", "Germany"]}]  }  //Search for movies that were recorded in Germany and USA but not in any other place. 

Aggregation Example: 
{
  _id: { x : "$imdb.rating" },
  NumMovies: {
   $count: { }
  }
}
"""