# This file is part of ACC Setup Parse.
# 
# This file may be used under the terms of the GNU General Public License
# version 3.0 as published by the Free Software Foundation and appearing in
# the file LICENSE included in the packaging of this file.  Please review the
# following information to ensure the GNU General Public License version 3.0
# requirements will be met: http://www.gnu.org/copyleft/gpl.html.
# 
# For more information contact
# jurs.slovinac2@gmail.com.
# 
# This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
# WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

class McLaren720S:
    """
    Class for converting and storing McLaren 720S GT3 setup from json file
    Use McLaren720S("<parsed json into list>")
    """
    def __init__(self, setup):

        #Saving setup into real values
        self.car = setup["carName"]
        self.carTitle = "McLaren 720S GT3"
        #Tyres
        self.tyreType = self._getTyreType(setup)
        self.tyrePressure = self._getTyrePressure(setup)
        self.tyreToe = self._getTyreToe(setup)
        self.tyreCamber = self._getTyreCamber(setup)
        self.tyreCaster = self._getTyreCaster(setup)
        #Electronics
        self.tc = setup['basicSetup']['electronics']['tC1']
        self.abs = setup['basicSetup']['electronics']['abs']
        self.ecu = setup['basicSetup']['electronics']['eCUMap'] + 1
        #Strategy
        self.fuel = setup['basicSetup']['strategy']['fuel']
        self.tyreSet = setup['basicSetup']['strategy']['tyreSet']
        self.frontBrakePad = setup['basicSetup']['strategy']['frontBrakePadCompound'] + 1
        self.rearBrakePad = setup['basicSetup']['strategy']['rearBrakePadCompound'] + 1
        #Mecanical settings
        self.frontARB = setup['advancedSetup']['mechanicalBalance']['aRBFront']
        self.rearARB = setup['advancedSetup']['mechanicalBalance']['aRBRear']
        self.wheelRate = self._getWheelRate(setup)
        self.bumpStopRate = self._getBumpStopRate(setup)
        self.bumpStopRange = setup['advancedSetup']['mechanicalBalance']['bumpStopWindow']
        self.brakePower = setup['advancedSetup']['mechanicalBalance']['brakeTorque'] + 80
        self.brakeBias = self._getBrakeBias(setup)
        self.preload = 20 + setup['advancedSetup']['drivetrain']['preload'] * 10
        #Dampers
        self.bumpSlow = setup['advancedSetup']['dampers']['bumpSlow']
        self.bumpFast = setup['advancedSetup']['dampers']['bumpFast']
        self.reboundSlow = setup['advancedSetup']['dampers']['reboundSlow']
        self.reboundFast = setup['advancedSetup']['dampers']['reboundFast']
        #Aero
        self.rideHeight = self._getRideHeight(setup)
        self.frontSpliter = 0
        self.rearWing = setup['advancedSetup']['aeroBalance']['rearWing'] + 1
        self.brakeDucts = setup['advancedSetup']['aeroBalance']['brakeDuct']


    def _getTyreType(self, setup): #Function for returning tyre compound
        if setup['basicSetup']['tyres']['tyreCompound'] == 0:
            return "Dry"
        else:
            return "Wet"
        
    def _getTyrePressure(self, setup): #Function returns real tyre pressure numbers
        pressures = []
        for p in setup['basicSetup']['tyres']['tyrePressure']:
            pressures.append(round(20.3 + p * 0.1, 1))

        return pressures
        
    def _getTyreToe(self, setup): #Function returns list of real toe vaules
        toe = []
        for t in range(0, 2): #Front toe
            toe.append(round(-0.48 + setup['basicSetup']['alignment']['toe'][t] * 0.01, 2))

        for t in range(2, 4): #Front toe
            toe.append(round(-0.1 + setup['basicSetup']['alignment']['toe'][t] * 0.01, 2))

        return toe
    
    def _getTyreCamber(self, setup): #Function return list of real camber values
        camber = []
        for c in range(0, 2): #Front camber
            camber.append(round(-4 + setup['basicSetup']['alignment']['camber'][c] * 0.1, 1))

        for c in range(2, 4): #Rear camber
            camber.append(round(-3.5 + setup['basicSetup']['alignment']['camber'][c] * 0.1, 1))

        return camber

    def _getTyreCaster(self, setup): #Function returns list of real caster values
        casterValues = [5.3, 5.6, 5.8, 6.0, 6.3, 6.5, 6.8, 7.0, 7.3, 7.5, 7.8, 8.0] #Possible vaules in-game
        caster = []
        caster.append(casterValues[setup['basicSetup']['alignment']['casterLF']])
        caster.append(casterValues[setup['basicSetup']['alignment']['casterRF']])

        return caster
    
    def _getWheelRate(self, setup): #Returns list of real wheel rate vaules
        rates = []
        for r in range(0, 2): #Front springs
            rates.append(118000 + setup['advancedSetup']['mechanicalBalance']['wheelRate'][r] * 16000)

        for r in range(2, 4): #Rear springs
            rates.append(114000 + setup['advancedSetup']['mechanicalBalance']['wheelRate'][r] * 14000)

        return rates
    
    def _getBumpStopRate(self, setup): #Returns list of real bumpstop rates
        rates = []
        for r in setup['advancedSetup']['mechanicalBalance']['bumpStopRateUp']:
            rates.append(300 + r * 100)

        return rates
    
    def _getBrakeBias(self, setup): #Returns real brake bias value in %
        return (47.0 + setup['advancedSetup']['mechanicalBalance']['brakeBias'] * 0.2)
    
    def _getRideHeight(self, setup): #Returns list of real ride height values [front, rear]
        height = []
        height.append(50 + setup['advancedSetup']['aeroBalance']['rideHeight'][0]) #Front
        height.append(64 + setup['advancedSetup']['aeroBalance']['rideHeight'][2]) #Rear

        return height