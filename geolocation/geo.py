#!/bin/python

from geopy.distance import great_circle
from geopy.distance import vincenty
from geopy.geocoders import Nominatim

class GeoLocationException(Exception): pass

class GeoLocator(Object):
  """
  Class for Geo location
  """


  def __init__(self):
    """
    :constructor:
    "param self
    """
    self.geolocator = Nominatim()


  def getCoordinatesByAddress(address):
    """
    :param address
    query to an address and coordinates
    """
    _location = self.geolocator.geocode(address)
    if _location is None:
      raise GeoLocationException("Address not found")
    return _location.raw


  def getCoordinatesByLonLat(latitude, longitude):
    """
    :param latitude, lonitude
    address corresponding to a set of coordinates
    """
    _location = self.geolocator.reverse(latitude, longitude)
    if _location is None:
      raise GeoLocationException("Coordinates not found")
    return _location.raw


  def getDistanceByVincenty(pointA, pointB):
    """
    :param (latitude, longitude) of A, (latitude, longitude) of B
    Caculate distance based on Vincenty distance in miles
    """
    if isinstance(pointA, tuple) and isinstance(pointB, tuple)
      _distance = vincenty(pointA, pointB)
      return _distance.miles
    else:
      raise GeoLocationException("Require a tuple of Latitude and Longtitude of the location")


  def getDistanceByCircle(pointA, pointB):
    """
    :param (latitude, longitude) of A, (latitude, longitude) of B
    Calculate distance based on great-circle distance in miles
    """
    if isinstance(pointA, tuple) and isinstance(pointB, tuple)
      _distance = great_circle(pointA, pointB)
      return _distance.miles
    else:
      raise GeoLocationException("Require a tuple of Latitude and Longtitude of the location")
   
