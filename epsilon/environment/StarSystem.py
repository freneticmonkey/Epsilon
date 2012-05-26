
from Utilities import Random

import Star
import Planet

class StarSystem:
    
    def __init__(self, seed):
        self._seed = seed
        self._planetRand = Random.Random(1000000, self._seed)
        self._star = None
        self._planets = [] 
        
    def _generateSystem(self):
        # Generate Star
        
        
        #Generate Planets
        self._numberOfPlanets = Random.Random(100, self._seed)._generateNumber()
        
        pCount = 0
        while pCount < self._numberOfPlanets:
            _generatePlanetInfo()
            
    def _generateStarInfo(self):
        classType = Random.Random(7, self._seed)._generateNumber()
        self._star = Star(classType)         
            
    def _generatePlanetInfo(self):
        
        #Generate an ID/seed for the planet
        planetID = self._planetRand._generateNumber()
        
        orbitDist, radius, gravity, hasOrbitors
        
        #generate an orbitDist in AU
        
        #generate a radius 
        
        newPlanet = Planet(planetID)
        
        
            
        
        
        