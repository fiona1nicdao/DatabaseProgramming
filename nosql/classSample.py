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

"""