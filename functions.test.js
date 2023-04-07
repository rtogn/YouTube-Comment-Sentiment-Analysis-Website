const { spawnSync } = require('child_process');
const { mock, it } = require('node:test');
const { describe } = require('yargs');
const LoginFunctions = require('./static/functions');

let spy;
beforeEach (() => {
    spy = jest.spyOn(document, 'getElementById');
});

describe ("All login and register popup tests", () => {
    describe('with new item', () => {
        let mockElement;
        beforeEach( () => {
            mockElement = document.createElement();
            spy.mockReturnValue(mockElement);
        });
    
        it('id of pop-up box should change to display', () => {
            spy.mockElement.LoginFunctions.openLog(mockElement);
            expect(mockElement.style.display).toBe('none');
        });
                
        it('id of register-up box should change to display', () => {
            spy.mockElement.LoginFunctions.openReg(mockElement);
            expect(mockElement.style.display).toBe('none');
        });

    });
});