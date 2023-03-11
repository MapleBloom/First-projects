function Device(name) {
    this.volt = '220',
    this.name = name,
    this.watts = undefined,
    this.turn = false
}

Device.prototype.getWatts = function() {
    let power = this.turn ? this.watts : 0;
    console.log(`${this.name} power consumption ${power} watts`);
    return power;
}

Device.prototype.printAllProp = function() {
    console.log(`${this.name.toUpperCase()} :`);
    for (let key in this) {
        if (typeof this[key] != 'function') {
            console.log(`${key} : ${this[key]}`);
        }
    }
}

Device.prototype.turnOn = function() {
    this.turn = true;
    console.log(`\n${this.name.toUpperCase()} turned on`);
}

Device.prototype.turnOff = function() {
    this.turn = false;
    console.log(`\n${this.name.toUpperCase()} turned off`);
}

function registry(objs) {
    console.log(`\n   Devices: `);
    for (let obj in objs) {
        console.log();
        objs[obj].printAllProp();
    }
    console.log('___');
}

function powerConsumption(objs) {
    let power_consumption = 0;
    console.log(`\n   Power Consumption:\n`);
    for (let obj in objs) {
        power_consumption += objs[obj].getWatts();
    }
    console.log(`___\n   Total current power consumption: ${power_consumption} watts`);
}

function Comp(name, watts, os) {
    this.name = name,
    this.watts = watts,
    this.os = os,
    this.sleep = true
}

function Lamp(name, watts, light) {
    this.name = name,
    this.watts = watts,
    this.light = light
}

Comp.prototype = new Device();
Lamp.prototype = new Device();

Comp.prototype.sleepOn = function() {
    this.sleep = true;
    console.log(`\n${this.name.toUpperCase()} comp sleeps`);
}

Comp.prototype.turnOn = function() {
    this.sleep = false;
    this.turn = true;
    console.log(`\n${this.name.toUpperCase()} comp turned on`);
}

Comp.prototype.turnOff = function() {
    this.sleep = false;
    this.turn = false;
    console.log(`\n${this.name.toUpperCase()} comp turned off`);
}

Comp.prototype.getWatts = function() {
    let power = this.turn ? this.watts : 0;
    power = this.sleep ? Math.round(power * 0.2, -1) : power;
    console.log(`${this.name} power consumption ${power} watts`);
    return power;
}


const devices = {};
devices.asus = new Comp('asus', 19, 'Windows');
devices.deskLamp = new Lamp('deskLamp', 7, 'cold');
devices.bedLamp = new Lamp('bedLamp', 4, 'hot');

devices.asus.turnOn();
devices.deskLamp.turnOn();

registry(devices);
powerConsumption(devices);

devices.asus.sleepOn();
powerConsumption(devices);

devices.asus.turnOff();
devices.bedLamp.turnOn();
powerConsumption(devices);
