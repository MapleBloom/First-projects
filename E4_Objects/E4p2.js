function stringInObj(string, obj) {
    return string in obj;
} 

some_obj = {a: 10, 1: '123'};

console.log(stringInObj('a', some_obj));