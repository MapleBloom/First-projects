function printOwnProp(obj) {
    console.log(`\n   Only own properties: `);
    for (let key in obj) {
        if (obj.hasOwnProperty(key)) {
            console.log(`key ${key} , value ${obj[key]}`);
        }
    }
} 

function printAllProp(obj) {
    console.log(`\n   Own and proto properties: `);
    for (let key in obj) {
        console.log(`key ${key} , value ${obj[key]}`);
        console.log(`key type ${typeof key} , value type ${typeof obj[key]}`);
    }
} 

const parent_obj = {parent: 'parent'};
const some_obj = Object.create(parent_obj);
some_obj.a = 10;
some_obj[1] = '123'

// only own properties
console.log(some_obj);

// only own properties
printOwnProp(some_obj);
// own and proto properties
printAllProp(some_obj);
