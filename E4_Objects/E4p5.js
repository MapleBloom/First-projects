class Device {
    constructor(name) {
        this.volt = '220';
        this.name = name;
        this.watts = undefined;
        this.turn = false;
    }

    getWatts() {
        let power = this.turn ? this.watts : 0;
        console.log(`${this.name} power consumption ${power} watts`);
        return power;
    }

    printAllProp() {
        console.log(`${this.name.toUpperCase()} :`);
        for (let key in this) {
            if (typeof this[key] != 'function') {
                console.log(`${key} : ${this[key]}`);
            }
        }
    }

    turnOn() {
        this.turn = true;
        console.log(`\n${this.name.toUpperCase()} turned on`);
    }

    turnOff() {
        this.turn = false;
        console.log(`\n${this.name.toUpperCase()} turned off`);
    }
}

class ObjectRegistry {
    constructor() {}

    registry() {
        console.log(`\n   Devices: `);
        for (let obj in this) {
            console.log();
            this[obj].printAllProp();
        }
        console.log('___');
    }

    powerConsumption() {
        let power_consumption = 0;
        console.log(`\n   Power Consumption:\n`);
        for (let obj in this) {
            power_consumption += this[obj].getWatts();
        }
        console.log(`___\n   Total current power consumption: ${power_consumption} watts`);
    }
}

class Comp extends Device {
    constructor(name, watts, os) {
        super(name, watts);
        this.watts = watts;
        this.os = os;
        this.sleep = true;
    }

    sleepOn() {
        this.sleep = true;
        console.log(`\n${this.name.toUpperCase()} comp sleeps`);
    }

    turnOn() {
        super.turnOn();
        this.sleep = false;
    }

    turnOff() {
        super.turnOff();
        this.sleep = false;
    }

    getWatts() {
        let power = this.turn ? this.watts : 0;
        power = this.sleep ? Math.round(power * 0.1) : power;
        console.log(`${this.name} power consumption ${power} watts`);
        return power;
    }
}

class Lamp extends Device {
    constructor(name, watts, light) {
        super(name, watts);
        this.watts = watts;
        this.light = light;
    }
}


const devices = new ObjectRegistry();
devices.asus = new Comp('asus', 19, 'Windows');
devices.deskLamp = new Lamp('deskLamp', 7, 'cold');
devices.bedLamp = new Lamp('bedLamp', 4, 'hot');

devices.asus.turnOn();
devices.deskLamp.turnOn();

devices.registry();
devices.powerConsumption();

devices.asus.sleepOn();
devices.powerConsumption();

devices.asus.turnOff();
devices.bedLamp.turnOn();
devices.powerConsumption();
